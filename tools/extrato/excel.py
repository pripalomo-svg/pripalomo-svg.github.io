#!/usr/bin/env python3
"""Gera extrato-2026.xlsx a partir de assets/extrato-2026.data.js.

A coluna amarela Seu nome é o lugar para nomear cada valor.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "assets" / "extrato-2026.data.js"
OUT = ROOT / "extrato-2026.xlsx"

SETORES = {
    "salario_priscila": "Salário da Priscila",
    "aporte_priscila": "Transferência da Priscila",
    "salario_luisa": "Salário da Luísa (McKinsey)",
    "outras_entradas": "Outras entradas",
    "estorno": "Estorno",
    "rendimento": "Rendimento",
    "cartao_black": "Cartão Black",
    "moradia": "Moradia",
    "educacao": "Educação",
    "pessoas": "Pessoas",
    "para_priscila": "Enviado à Priscila",
    "saude": "Saúde",
    "alimentacao": "Alimentação",
    "transporte": "Transporte",
    "compras": "Compras",
    "viagem": "Viagem",
    "lazer": "Lazer",
    "assinaturas": "Assinaturas",
    "impostos": "Impostos",
    "boletos": "Boletos",
    "investimentos": "Investimentos",
    "transferencia_banco": "Outro banco",
    "outros": "Outros",
    "cofrinho": "Cofrinho",
    "cdb": "CDB",
    "tbi": "Mesma conta",
}

MESES = [
    ("2026-01", "janeiro"),
    ("2026-02", "fevereiro"),
    ("2026-03", "março"),
    ("2026-04", "abril"),
    ("2026-05", "maio"),
    ("2026-06", "junho"),
    ("2026-07", "julho"),
    ("2026-08", "agosto"),
    ("2026-09", "setembro (até o dia 25)"),
]

PETROLEO = "0E4A57"
AMARELO = "FFF3B0"
CINZA = "F4F1EA"
LINHA = "D9D3C7"
VERDE = "E5F6D8"
ROSA = "FDE4F3"

fill_header = PatternFill("solid", fgColor=PETROLEO)
fill_nome = PatternFill("solid", fgColor=AMARELO)
fill_cinza = PatternFill("solid", fgColor=CINZA)
fill_verde = PatternFill("solid", fgColor=VERDE)
fill_rosa = PatternFill("solid", fgColor=ROSA)
font_header = Font(name="Calibri", bold=True, color="FFFFFF", size=12)
font_body = Font(name="Calibri", size=12, color="1A1A1A")
font_titulo = Font(name="Calibri", bold=True, size=18, color=PETROLEO)
font_texto = Font(name="Calibri", size=13, color="1A1A1A")
thin = Border(
    left=Side(style="thin", color=LINHA),
    right=Side(style="thin", color=LINHA),
    top=Side(style="thin", color=LINHA),
    bottom=Side(style="thin", color=LINHA),
)
center = Alignment(vertical="center", wrap_text=True)
left = Alignment(vertical="center", wrap_text=True, horizontal="left")
money = 'R$ #,##0.00'
date_fmt = "DD/MM/YYYY"


def carregar() -> dict:
    raw = DATA.read_text(encoding="utf-8")
    return json.loads(raw[raw.index("{") : raw.rindex("}") + 1])


def tipo_de(tx: dict) -> str:
    if tx["setor"] == "cofrinho" and tx["valor"] < 0:
        return "Cofrinho (entrada)"
    if tx["setor"] in ("cofrinho", "cdb", "tbi"):
        return "Entre contas"
    if tx["valor"] > 0:
        return "Entrada"
    return "Saída"


def recorrencia(tx: dict) -> str:
    if tx.get("papel") == "assinatura":
        return "Assinatura"
    if tx.get("papel") == "conta_fixa":
        return "Conta fixa"
    return ""


def origem(tx: dict) -> str:
    if tx.get("origem") == "fatura_black":
        return "Fatura do cartão"
    if tx.get("origem") == "tarifa_black":
        return "Tarifa do cartão"
    return ""


def iso_date(iso: str) -> date:
    ano, mes, dia = iso.split("-")
    return date(int(ano), int(mes), int(dia))


def cabecalho(ws, colunas: list[str]) -> None:
    for col, nome in enumerate(colunas, start=1):
        cell = ws.cell(1, col, nome)
        cell.fill = fill_header
        cell.font = font_header
        cell.alignment = Alignment(vertical="center", wrap_text=True, horizontal="left")
        cell.border = thin
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(colunas))}1"
    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddHeader.left.text = "Extrato 2026"
    ws.print_title_rows = "1:1"


def pintar(cell, fill=None) -> None:
    cell.font = font_body
    cell.alignment = left
    cell.border = thin
    if fill is not None:
        cell.fill = fill


def larguras(ws, pares: list[tuple[str, float]]) -> None:
    for letra, largura in pares:
        ws.column_dimensions[letra].width = largura


def main() -> None:
    dados = carregar()
    lancamentos = dados["lancamentos"]
    for tx in lancamentos:
        texto = f"{tx['desc']} {tx['contraparte']}"
        if "3767" in texto or "313.050" in texto or "313050718" in texto:
            raise SystemExit("O Excel vazaria dado da conta")

    grupos: dict[str, dict] = {}
    meses = {ym: {"entradas": 0.0, "cofrinho": 0.0, "saidas": 0.0} for ym, _ in MESES}
    for tx in lancamentos:
        nome = tx["contraparte"]
        grupo = grupos.setdefault(
            nome,
            {"n": 0, "entrou": 0.0, "saiu": 0.0, "entre": 0.0, "categorias": defaultdict(int)},
        )
        grupo["n"] += 1
        grupo["categorias"][SETORES.get(tx["setor"], tx["setor"])] += 1
        tipo = tipo_de(tx)
        ym = tx["data"][:7]
        abs_valor = abs(tx["valor"])
        if tipo == "Entrada":
            grupo["entrou"] += tx["valor"]
            if ym in meses:
                meses[ym]["entradas"] += tx["valor"]
        elif tipo == "Cofrinho (entrada)":
            grupo["entrou"] += abs_valor
            if ym in meses:
                meses[ym]["entradas"] += abs_valor
                meses[ym]["cofrinho"] += abs_valor
        elif tipo == "Saída":
            grupo["saiu"] += abs_valor
            if ym in meses:
                meses[ym]["saidas"] += abs_valor
        else:
            grupo["entre"] += abs_valor

    entrou = round(sum(m["entradas"] for m in meses.values()), 2)
    saiu = round(sum(m["saidas"] for m in meses.values()), 2)
    cofrinho = round(sum(m["cofrinho"] for m in meses.values()), 2)
    if len(lancamentos) != 634 or entrou != 439794.35 or saiu != 384738.21 or cofrinho != 88720.0:
        raise SystemExit(f"Totais inesperados: n={len(lancamentos)} entrou={entrou} saiu={saiu} cofrinho={cofrinho}")

    wb = Workbook()
    como = wb.active
    como.title = "Como usar"
    escrever_instrucoes(como, dados, entrou, saiu, cofrinho)

    nomes = wb.create_sheet("Nomes")
    escrever_nomes(nomes, grupos)

    movs = wb.create_sheet("Lançamentos")
    escrever_lancamentos(movs, lancamentos, len(grupos))

    aba_meses = wb.create_sheet("Meses")
    escrever_meses(aba_meses, meses)

    saldos = wb.create_sheet("Saldos")
    escrever_saldos(saldos, dados)

    wb.properties.title = "Extrato 2026"
    wb.properties.creator = "Priscila Palomo"
    wb.active = nomes
    wb.save(OUT)
    print(f"{OUT} · {len(lancamentos)} lançamentos · {len(grupos)} nomes")


def escrever_instrucoes(ws, dados, entrou, saiu, cofrinho) -> None:
    ws.sheet_view.showGridLines = False
    ws["A1"] = "Extrato 2026"
    ws["A1"].font = font_titulo
    linhas = [
        "1 jan a 25 set 2026. Todos os lançamentos estão na aba Lançamentos.",
        "Para nomear um valor, abra a aba Nomes e escreva na coluna amarela Seu nome.",
        "O mesmo nome vale para todos os movimentos daquele grupo. A aba Lançamentos mostra o nome ao lado de cada valor.",
        "Se um movimento precisar de um nome só dele, substitua a fórmula da coluna Seu nome nessa linha.",
        "No dashboard, use Trazer nomes do Excel e escolha este arquivo. O nome passa a aparecer nas barras.",
        "Não apague a coluna Id. Ela liga o movimento ao extrato.",
        f"Entrou R$ {entrou:,.2f}, já com R$ {cofrinho:,.2f} de transferências para cofrinhos. Saiu R$ {saiu:,.2f}.",
        f"Saldo em {dados['saldoInicialData']}: R$ {dados['saldoInicial']:,.2f}. Saldo em {dados['periodo']['fim']}: R$ {dados['saldoFinal']:,.2f}.",
    ]
    for i, texto in enumerate(linhas, start=3):
        ws.cell(i, 1, texto).font = font_texto
        ws.row_dimensions[i].height = 22
    ws.column_dimensions["A"].width = 120
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddHeader.left.text = "Extrato 2026"


def escrever_nomes(ws, grupos: dict) -> None:
    colunas = ["Nome no extrato", "Seu nome", "Lançamentos", "Entrou", "Saiu", "Entre contas", "Categoria"]
    cabecalho(ws, colunas)
    ws["B1"].comment = Comment(
        "Escreva aqui o nome que você quer ver. Deixe em branco para manter o nome do extrato.",
        "Extrato",
        width=240,
        height=50,
    )
    ordem = sorted(grupos, key=lambda nome: grupos[nome]["entrou"] + grupos[nome]["saiu"], reverse=True)
    for linha, nome in enumerate(ordem, start=2):
        grupo = grupos[nome]
        categoria = max(grupo["categorias"], key=grupo["categorias"].get)
        valores = [nome, None, grupo["n"], round(grupo["entrou"], 2), round(grupo["saiu"], 2), round(grupo["entre"], 2), categoria]
        for col, valor in enumerate(valores, start=1):
            cell = ws.cell(linha, col, valor)
            pintar(cell, fill_nome if col == 2 else None)
            if col in (4, 5, 6):
                cell.number_format = money
                cell.alignment = Alignment(vertical="center", horizontal="right")
            if col == 3:
                cell.alignment = Alignment(vertical="center", horizontal="right")
        ws.row_dimensions[linha].height = 20
    ultima = 1 + len(ordem)
    ws.auto_filter.ref = f"A1:G{ultima}"
    larguras(ws, [("A", 36), ("B", 36), ("C", 16), ("D", 18), ("E", 18), ("F", 18), ("G", 32)])
    ws.auto_filter.add_sort_condition("D2:D2")


def escrever_lancamentos(ws, lancamentos: list[dict], n_nomes: int) -> None:
    colunas = [
        "Data",
        "Descrição",
        "Valor",
        "Tipo",
        "Categoria",
        "Nome no extrato",
        "Seu nome",
        "Recorrência",
        "Origem",
        "Id",
    ]
    cabecalho(ws, colunas)
    ws["G1"].comment = Comment(
        "Esta célula repete o nome da aba Nomes. Substitua a fórmula só quando este movimento tiver um nome diferente.",
        "Extrato",
        width=260,
        height=60,
    )
    fim_nomes = max(2, n_nomes + 1)
    for i, tx in enumerate(lancamentos, start=2):
        data = iso_date(tx["data"])
        tipo = tipo_de(tx)
        valores = [
            data,
            tx["desc"],
            tx["valor"],
            tipo,
            SETORES.get(tx["setor"], tx["setor"]),
            tx["contraparte"],
            f'=IFERROR(VLOOKUP(F{i},Nomes!$A$2:$B${fim_nomes},2,FALSE),"")',
            recorrencia(tx),
            origem(tx),
            tx["id"],
        ]
        for col, valor in enumerate(valores, start=1):
            cell = ws.cell(i, col, valor)
            pintar(cell, fill_nome if col == 7 else None)
        ws.cell(i, 1).number_format = date_fmt
        ws.cell(i, 3).number_format = money
        ws.cell(i, 3).alignment = Alignment(vertical="center", horizontal="right")
        if tipo == "Entrada" or tipo.startswith("Cofrinho"):
            ws.cell(i, 4).fill = fill_verde
        elif tipo == "Saída":
            ws.cell(i, 4).fill = fill_rosa
        ws.row_dimensions[i].height = 18
    ultima = 1 + len(lancamentos)
    ws.auto_filter.ref = f"A1:J{ultima}"
    larguras(
        ws,
        [
            ("A", 14),
            ("B", 42),
            ("C", 16),
            ("D", 22),
            ("E", 28),
            ("F", 32),
            ("G", 32),
            ("H", 16),
            ("I", 20),
            ("J", 16),
        ],
    )
    tipos = DataValidation(type="list", formula1='"Entrada,Saída,Cofrinho (entrada),Entre contas"', allow_blank=True)
    tipos.error = "Escolha um tipo da lista"
    tipos.errorTitle = "Tipo"
    tipos.add(f"D2:D{ultima}")
    ws.add_data_validation(tipos)


def escrever_meses(ws, meses: dict) -> None:
    colunas = ["Mês", "Entradas", "Das quais cofrinho", "Saídas", "Resultado"]
    cabecalho(ws, colunas)
    total_e = total_c = total_s = 0.0
    for i, (ym, nome) in enumerate(MESES, start=2):
        ent = round(meses[ym]["entradas"], 2)
        cof = round(meses[ym]["cofrinho"], 2)
        sai = round(meses[ym]["saidas"], 2)
        total_e += ent
        total_c += cof
        total_s += sai
        for col, valor in enumerate([nome, ent, cof, sai, round(ent - sai, 2)], start=1):
            cell = ws.cell(i, col, valor)
            pintar(cell)
            if col > 1:
                cell.number_format = money
                cell.alignment = Alignment(vertical="center", horizontal="right")
    rodape = 2 + len(MESES)
    for col, valor in enumerate(["Ano", round(total_e, 2), round(total_c, 2), round(total_s, 2), round(total_e - total_s, 2)], start=1):
        cell = ws.cell(rodape, col, valor)
        pintar(cell, fill_cinza)
        cell.font = Font(name="Calibri", bold=True, size=12)
        if col > 1:
            cell.number_format = money
    ws.auto_filter.ref = f"A1:E{rodape - 1}"
    larguras(ws, [("A", 28), ("B", 18), ("C", 24), ("D", 18), ("E", 18)])


def escrever_saldos(ws, dados: dict) -> None:
    colunas = ["Data", "Saldo"]
    cabecalho(ws, colunas)
    inicio = datetime.strptime(dados["saldoInicialData"], "%Y-%m-%d").date()
    cell = ws.cell(2, 1, inicio)
    pintar(cell, fill_cinza)
    cell.number_format = date_fmt
    cell = ws.cell(2, 2, dados["saldoInicial"])
    pintar(cell, fill_cinza)
    cell.number_format = money
    ws.cell(2, 1).comment = Comment("Saldo do dia anterior ao período.", "Extrato", width=180, height=30)
    for i, ponto in enumerate(dados["saldoDiario"], start=3):
        cell = ws.cell(i, 1, iso_date(ponto["data"]))
        pintar(cell)
        cell.number_format = date_fmt
        cell = ws.cell(i, 2, ponto["saldo"])
        pintar(cell)
        cell.number_format = money
    ultima = 2 + len(dados["saldoDiario"])
    ws.auto_filter.ref = f"A1:B{ultima}"
    larguras(ws, [("A", 16), ("B", 18)])


if __name__ == "__main__":
    main()

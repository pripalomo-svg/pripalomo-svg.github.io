#!/usr/bin/env python3
"""Monta assets/extrato-2026.data.js a partir dos extratos Itaú em texto.

Os PDFs não entram no repositório. Rode este script depois de extrair o texto
(pdftotext ou pypdf) para os dois períodos:

  python3 tools/extrato/montar.py extrato-jan-jun.txt extrato-jun-set.txt

O primeiro arquivo é 01/01/2026–30/06/2026. O segundo é o período seguinte
(no extrato usado aqui, 27/06/2026–25/09/2026). Junho fica só no primeiro.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

AMT_RE = re.compile(r"(-?\d{1,3}(?:\.\d{3})*,\d{2})$")
DATE_RE = re.compile(r"^(\d{2}/\d{2}/\d{4})\s+(.*)$")
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "extrato-2026.data.js"


def parse_amount(raw: str) -> float:
    return round(float(raw.replace(".", "").replace(",", ".")), 2)


def parse_lines(text: str) -> list[dict]:
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        matched = DATE_RE.match(line)
        if not matched:
            continue
        date_br, rest = matched.group(1), matched.group(2).strip()
        amount = AMT_RE.search(rest)
        if not amount:
            continue
        desc = rest[: amount.start()].strip()
        day, month, year = date_br.split("/")
        out.append(
            {
                "date": f"{year}-{month}-{day}",
                "desc": desc,
                "value": parse_amount(amount.group(1)),
            }
        )
    return out


def norm(desc: str) -> str:
    cleaned = re.sub(r"\s*\d{2}/\d{2}$", "", desc.upper()).strip()
    cleaned = cleaned.replace("3767.29709-0", "CONTA PROPRIA")
    cleaned = cleaned.replace("3767.29709", "CONTA PROPRIA")
    return re.sub(r"\s+", " ", cleaned)


def public_desc(desc: str) -> str:
    return (
        desc.replace("3767.29709-0", "conta própria")
        .replace("3767.29709", "conta própria")
        .strip()
    )


def title_name(raw: str) -> str:
    special = {
        "PRISCIL": "Priscila",
        "PRISCILA": "Priscila",
        "PRISCILA D": "Priscila",
        "PALOMO": "Priscila",
        "LUISA": "Luísa",
        "LUISA G": "Luísa",
        "MCKINSEY": "McKinsey",
        "MCKINSEY C": "McKinsey",
    }
    key = re.sub(r"\s+", " ", raw).strip(" .")
    if key in special:
        return special[key]
    return " ".join(part.capitalize() for part in key.split())


def classify(desc: str, value: float) -> dict | None:
    raw = norm(desc)
    if raw.startswith("SALDO DO DIA"):
        return None

    def pack(setor, contraparte, papel="", origem=""):
        return {
            "setor": setor,
            "contraparte": contraparte,
            "papel": papel,
            "origem": origem,
        }

    if raw.startswith("APLICACAO COFRINHOS"):
        return pack("cofrinho", "Cofrinho")
    if raw.startswith("RESGATE COFRINHOS"):
        return pack("cofrinho", "Cofrinho")
    if "RESGATE CDB" in raw or raw.startswith("COF RESGATE"):
        return pack("cdb", "CDB")
    if raw.startswith("TBI "):
        return pack("tbi", "Mesma conta")
    if raw.startswith("REND PAGO"):
        return pack("rendimento", "Rendimento da aplicação")

    if "MCKINSEY" in raw:
        return pack("salario_luisa", "Luísa · McKinsey")
    if "REMUNERACAO" in raw or raw == "SALARIO":
        return pack("salario_priscila", "Priscila · salário")
    if any(token in raw for token in ("PRISCIL", "PALOMO", "PRISCILA")):
        if value >= 0:
            return pack("aporte_priscila", "Priscila")
        return pack("para_priscila", "Priscila")

    if raw.startswith("DEV PIX") or raw.startswith("DEV "):
        rest = re.sub(r"^DEV PIX\s+", "", raw)
        rest = re.sub(r"^DEV\s+", "", rest)
        return pack("estorno", title_name(rest) if rest else "Estorno")

    if "PERS BLACK" in raw:
        return pack("cartao_black", "Fatura Cartão Black", origem="fatura_black")
    if "FATURA PAGA PERSON" in raw:
        return pack("cartao_black", "Fatura Cartão Black", origem="fatura_black")
    if "CARTAO PERSON" in raw:
        return pack("cartao_black", "Tarifa Personnalité", origem="tarifa_black")

    if "FINANC IMOB" in raw or raw.startswith("LANCAMENTO A DEBITO"):
        return pack("moradia", "Financiamento imobiliário", papel="conta_fixa")
    if "CONDOMINIO" in raw:
        return pack("moradia", "Condomínio Verana", papel="conta_fixa")
    if "ELETROPAULO" in raw:
        return pack("moradia", "Energia elétrica", papel="conta_fixa")
    if "DIRETORIA" in raw:
        return pack("moradia", "Diretoria do prédio")

    if "PORTO SEG" in raw:
        return pack("assinaturas", "Porto Seguro Vida", papel="assinatura")
    if "VGBL" in raw:
        return pack("assinaturas", "VGBL", papel="assinatura")
    if "CLARO" in raw:
        return pack("assinaturas", "Claro", papel="assinatura")
    if "TELEFONICA" in raw:
        return pack("assinaturas", "Telefônica", papel="assinatura")
    if "VIVO" in raw:
        return pack("assinaturas", "Vivo", papel="assinatura")
    if "CONSELHO" in raw:
        return pack("assinaturas", "Conselho profissional", papel="assinatura")

    if "CIRANDA" in raw:
        return pack("educacao", "Ciranda", papel="conta_fixa")
    if re.search(r"\bESCOLA\b", raw):
        return pack("educacao", "Escola")
    if "PSICOSABER" in raw:
        return pack("educacao", "PsicoSaber")
    if "PRINCIPIA" in raw:
        return pack("educacao", "Principia")
    if "IMPULSO" in raw:
        return pack("educacao", "Impulso")

    if "SECRETARIA" in raw or "PM SAO PAU" in raw or "SECR." in raw:
        if value < 0:
            return pack("impostos", "Prefeitura / IPTU", papel="conta_fixa")
        return pack("outras_entradas", "Prefeitura / IPTU")
    if "RECEITA FED" in raw:
        return pack("impostos", "Receita Federal")

    if "CRIPTO COMPRA USDC" in raw:
        return pack("investimentos", "Compra de USDC", papel="conta_fixa")
    if "CRIPTO" in raw:
        name = "Compra de BTC" if "BTC" in raw else "Cripto"
        return pack("investimentos", name)
    if "INTE" in raw and raw.startswith("TED"):
        return pack("transferencia_banco", "Banco Inter")

    if "DECOLAR" in raw:
        return pack("viagem", "Decolar")
    if "POUSADA" in raw:
        return pack("viagem", "Pousada")

    if "UBER" in raw:
        return pack("transporte", "Uber")
    if "AUTOPASS" in raw:
        return pack("transporte", "Autopass")
    if "ESTACION" in raw:
        return pack("transporte", "Estacionamento")

    if any(token in raw for token in ("DROGARIA", "FARMACIA", "RAIA", "RD SAUDE")):
        if "RD SAUDE" in raw:
            name = "RD Saúde"
        elif "RAIA" in raw:
            name = "Raia"
        else:
            name = "Farmácia"
        return pack("saude", name)
    if re.search(r"\bDROGA\b", raw):
        return pack("saude", "Farmácia")

    if "AMAZON" in raw:
        return pack("compras", "Amazon")
    if "SHPP" in raw or "SHOPEE" in raw:
        return pack("compras", "Shopee")
    if "LEROY" in raw:
        return pack("compras", "Leroy Merlin")
    if any(token in raw for token in ("PAGALEVE", "PIX MARKET", "MARKETP", "PAGAR.ME", "PAGAR ME", "SAFE2PAY", "TUNA PAGA", "ZOOP")):
        names = (
            ("PAGALEVE", "Pagaleve"),
            ("SAFE2PAY", "Safe2Pay"),
            ("TUNA", "Tuna"),
            ("ZOOP", "Zoop"),
            ("PAGAR", "Pagar.me"),
            ("MARKET", "Mercado Pago"),
        )
        name = next(label for token, label in names if token in raw)
        return pack("compras", name)

    if any(token in raw for token in ("MAMBO", "SUPERMERCAD", "AKI MERCADO", "PIZZAR", "DELICIA", "BRASIL ALIM")):
        names = (
            ("MAMBO", "Mambo"),
            ("SUPERMERCAD", "Supermercado"),
            ("AKI MERCADO", "Mercado"),
            ("PIZZAR", "Pizzaria"),
            ("DELICIA", "Delícia"),
            ("BRASIL ALIM", "Brasil Alimentação"),
        )
        name = next(label for token, label in names if token in raw)
        return pack("alimentacao", name)
    if "CINEM" in raw or " BELEZA" in f" {raw}" or raw.startswith("PAY ZIG") or "ZIG " in raw or "ZIG E" in raw or "ZIG F" in raw:
        if "CINEM" in raw:
            return pack("lazer", "Cinema")
        if "BELEZA" in raw:
            return pack("lazer", "Beleza")
        return pack("lazer", "Zig")

    if "444986947" in raw:
        return pack("boletos", "Boleto recorrente", papel="conta_fixa")
    if re.search(r"\b237\b", raw) and ("PAG TIT" in raw or "INT PAG" in raw):
        return pack("boletos", "Boleto 237")
    if "BRADESCO" in raw or raw.startswith("PAG BOLETO") or "PAG TIT" in raw or "INT PAG" in raw:
        return pack("boletos", "Boleto")

    if "CAIXA ECON" in raw:
        return pack("outras_entradas" if value >= 0 else "outros", "Caixa Econômica")
    if "TAM L" in raw:
        return pack("outras_entradas" if value >= 0 else "outros", "TAM")

    if raw.startswith("PIX TRANSF") or raw.startswith("PIX QRS") or raw.startswith("PAY ") or raw.startswith("PAY-"):
        body = raw
        for prefix in ("PIX TRANSF ", "PIX QRS ", "PAY -", "PAY "):
            if body.startswith(prefix):
                body = body[len(prefix) :]
                break
        body = body.strip(" -.")
        if "LUISA" in body:
            return pack("outras_entradas" if value >= 0 else "pessoas", "Luísa")
        if body.startswith("PRINCIP"):
            return pack("educacao", "Principia")
        if body.startswith("INSTITU"):
            return pack("outros", "Instituição")
        if body.startswith("FULLTEC"):
            return pack("compras", "Fulltec")
        if re.match(r"^\d", body):
            return pack("outros", f"Transferência {title_name(body)}")
        if raw.startswith("PAY ") or raw.startswith("PAY-"):
            return pack("compras" if value < 0 else "outras_entradas", title_name(body) if body else "Débito")
        # PIX com nome só de letras costuma ser pessoa; código ou CNPJ fica em compras.
        if raw.startswith("PIX QRS") and re.search(r"\d", body):
            return pack("compras", title_name(body) if body else "Pix")
        return pack("pessoas" if value < 0 else "outras_entradas", title_name(body) if body else "Pix")

    return pack("outros" if value < 0 else "outras_entradas", title_name(raw[:42]))


def load_transactions(first_half: str, second_half: str) -> tuple[dict, list[dict], list[dict]]:
    first = parse_lines(first_half)
    second = parse_lines(second_half)
    opening = next(
        item for item in first if item["date"] == "2025-12-31" and item["desc"].startswith("SALDO")
    )
    chosen = [item for item in first if "2026-01-01" <= item["date"] <= "2026-06-30"]
    chosen += [item for item in second if "2026-07-01" <= item["date"] <= "2026-09-25"]
    # Extratos vêm do dia mais novo para o mais antigo.
    chosen.reverse()
    return opening, chosen, first + second


def build(opening: dict, chosen: list[dict]) -> dict:
    ocurrences: dict[str, int] = defaultdict(int)
    lancamentos = []
    stated_balances: dict[str, float] = {}
    movements = defaultdict(list)

    for item in chosen:
        if item["desc"].startswith("SALDO"):
            stated_balances[item["date"]] = item["value"]
            continue
        classified = classify(item["desc"], item["value"])
        if classified is None:
            continue
        key = f"{item['date']}|{item['desc']}|{item['value']:.2f}"
        ocurrences[key] += 1
        digest = hashlib.sha1(f"{key}|{ocurrences[key]}".encode()).hexdigest()[:12]
        lancamentos.append(
            {
                "id": digest,
                "data": item["date"],
                "desc": public_desc(item["desc"]),
                "valor": item["value"],
                **classified,
            }
        )
        movements[item["date"]].append(item["value"])

    balance = opening["value"]
    daily = []
    from datetime import date, timedelta

    current = date.fromisoformat("2026-01-01")
    last = date.fromisoformat("2026-09-25")
    adjustments = []
    while current <= last:
        iso = current.isoformat()
        balance = round(balance + sum(movements.get(iso, [])), 2)
        stated = stated_balances.get(iso)
        if stated is not None and abs(balance - stated) > 0.001:
            # O extrato de 25/09 imprime 592,57; 371,26 + 221,30 fecha em 592,56.
            adjustments.append({"data": iso, "calculado": balance, "extrato": stated})
            if abs(balance - stated) > 0.02:
                raise SystemExit(f"Saldo não fecha em {iso}: calculado {balance}, extrato {stated}")
            balance = stated
        daily.append({"data": iso, "saldo": balance})
        current += timedelta(days=1)

    if abs(balance - 592.57) > 0.001:
        raise SystemExit(f"Saldo final inesperado: {balance}")

    ids = [item["id"] for item in lancamentos]
    if len(ids) != len(set(ids)):
        raise SystemExit("Há ids de lançamento repetidos")

    return {
        "periodo": {"inicio": "2026-01-01", "fim": "2026-09-25"},
        "saldoInicial": opening["value"],
        "saldoInicialData": opening["date"],
        "saldoFinal": balance,
        "lancamentos": lancamentos,
        "saldoDiario": daily,
    }


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("uso: montar.py extrato-jan-jun.txt extrato-jun-set.txt")
    first = Path(sys.argv[1]).read_text()
    second = Path(sys.argv[2]).read_text()
    opening, chosen, _ = load_transactions(first, second)
    payload = build(opening, chosen)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "/* Gerado por tools/extrato/montar.py — não edite à mão. */\n"
        "window.EXTRATO = "
        + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"lancamentos {len(payload['lancamentos'])}")
    print(f"saldo {payload['saldoInicial']} -> {payload['saldoFinal']}")
    print(f"arquivo {OUT}")


if __name__ == "__main__":
    main()

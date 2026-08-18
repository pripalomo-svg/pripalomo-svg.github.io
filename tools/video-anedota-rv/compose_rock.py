#!/usr/bin/env python3
"""Compõe uma trilha instrumental própria, alegre e vibrante (pop-rock),
usando numpy — sem depender de soundfonts. Uso:

    python3 compose_rock.py <duracao_segundos> <arquivo_saida.wav>

Progressão animada I–V–vi–IV em Mi maior (E–B–C#m–A), com power chords,
baixo pulsante e uma bateria simples (bumbo, caixa e chimbal).
"""
import sys, wave
import numpy as np

SR = 44100

def _sig(freq, dur, kind="saw"):
    t = np.linspace(0, dur, int(SR*dur), endpoint=False)
    if kind == "saw":
        x = 2*(t*freq - np.floor(0.5 + t*freq))
    elif kind == "square":
        x = np.sign(np.sin(2*np.pi*freq*t))
    elif kind == "tri":
        x = 2*np.abs(2*(t*freq - np.floor(0.5 + t*freq))) - 1
    else:
        x = np.sin(2*np.pi*freq*t)
    return x

def _env(n, a=0.006, d=0.10, s=0.6, r=0.10):
    """envelope ADSR simples (em amostras a partir de segundos)"""
    A, D, R = int(SR*a), int(SR*d), int(SR*r)
    A, D, R = max(1, A), max(1, D), max(1, R)
    sus = max(1, n - A - D - R)
    env = np.concatenate([
        np.linspace(0, 1, A),
        np.linspace(1, s, D),
        np.full(sus, s),
        np.linspace(s, 0, R),
    ])
    if len(env) < n:
        env = np.pad(env, (0, n-len(env)), constant_values=0)
    return env[:n]

def chord(freqs, dur, kind="saw", gain=0.5):
    n = int(SR*dur)
    out = np.zeros(n)
    for f in freqs:
        s = _sig(f, dur, kind)[:n]
        out[:len(s)] += s
    out /= max(1, len(freqs))
    return out * _env(n) * gain

def kick(dur=0.18):
    n = int(SR*dur); t = np.linspace(0, dur, n, endpoint=False)
    f = np.linspace(120, 45, n)
    x = np.sin(2*np.pi*np.cumsum(f)/SR)
    return x * np.exp(-t*22) * 0.9

def snare(dur=0.16):
    n = int(SR*dur); t = np.linspace(0, dur, n, endpoint=False)
    noise = np.random.uniform(-1, 1, n)
    # realce de médios/agudos (diferença = filtro passa-alta simples)
    noise = np.concatenate([[0], np.diff(noise)])
    tone = np.sin(2*np.pi*180*t)
    return (noise*0.8 + tone*0.3) * np.exp(-t*26) * 0.7

def hat(dur=0.05):
    n = int(SR*dur); t = np.linspace(0, dur, n, endpoint=False)
    noise = np.random.uniform(-1, 1, n)
    noise = np.concatenate([[0], np.diff(noise)])
    return noise * np.exp(-t*90) * 0.35

def add(buf, sample, at):
    i = int(at*SR)
    j = min(len(buf), i+len(sample))
    if i < len(buf):
        buf[i:j] += sample[:j-i]

def main():
    total = float(sys.argv[1]); out_path = sys.argv[2]
    bpm = 132.0
    beat = 60.0/bpm
    bar = beat*4
    # power chords (raiz, quinta, oitava) — E, B, C#m, A
    ROOTS = {"E":82.41, "B":123.47, "C#":138.59, "A":110.00}
    PROG = ["E", "B", "C#", "A"]
    def power(root):
        return [root, root*1.5, root*2.0]

    n_total = int(SR*total) + SR
    guitar = np.zeros(n_total)
    bass   = np.zeros(n_total)
    drums  = np.zeros(n_total)

    n_bars = int(total/bar) + 2
    for b in range(n_bars):
        name = PROG[b % len(PROG)]
        root = ROOTS[name]
        t0 = b*bar
        # violão/guitarra em colcheias (8 por compasso), acento nos tempos
        for e in range(8):
            at = t0 + e*(beat/2)
            accent = 0.62 if e % 2 == 0 else 0.4
            g = chord(power(root), beat*0.46, kind="saw", gain=accent)
            add(guitar, g, at)
        # baixo pulsante em colcheias
        for e in range(8):
            at = t0 + e*(beat/2)
            bs = _sig(root/2, beat*0.45, "tri")[:int(SR*beat*0.45)]
            bs = bs * _env(len(bs), a=0.004, d=0.06, s=0.7, r=0.05) * 0.6
            add(bass, bs, at)
        # bateria: bumbo 1 e 3, caixa 2 e 4, chimbal nas colcheias
        add(drums, kick(),  t0 + 0*beat)
        add(drums, kick(),  t0 + 2*beat)
        add(drums, snare(), t0 + 1*beat)
        add(drums, snare(), t0 + 3*beat)
        for e in range(8):
            add(drums, hat(), t0 + e*(beat/2))

    mix = guitar*0.55 + bass*0.7 + drums*0.8
    mix = mix[:int(SR*total)]
    # leve saturação (calor) + normalização
    mix = np.tanh(mix*1.4)
    peak = np.max(np.abs(mix)) or 1.0
    mix = mix/peak*0.9
    # fade in/out
    fi = int(SR*1.5); fo = int(SR*2.5)
    if len(mix) > fi+fo:
        mix[:fi] *= np.linspace(0, 1, fi)
        mix[-fo:] *= np.linspace(1, 0, fo)
    pcm = (mix*32767).astype(np.int16)
    with wave.open(out_path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"trilha rock gerada: {out_path} ({total:.1f}s)")

if __name__ == "__main__":
    main()

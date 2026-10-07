#!/usr/bin/env python3
"""Trilha ambiente institucional (pad suave + notas pontuais), gerada com numpy.

    python3 compose_ambient.py <duracao_segundos> <saida.wav>

Progressão Am – F – C – G em andamento lento (um acorde a cada 4 s),
timbre de pad (senos desafinados + triângulo filtrado) e um arpejo
discreto. Sem samples externos.
"""
import sys, wave
import numpy as np

SR = 44100

def note(n):  # n = semitons a partir de A4 (440 Hz)
    return 440.0 * 2 ** (n / 12)

A3, C4, E4 = note(-12), note(-9), note(-5)
F3, G3, B3, D4, G4 = note(-16), note(-14), note(-10), note(-7), note(-2)
CHORDS = [
    [A3, C4, E4],
    [F3, A3, C4],
    [C4, E4, G4],
    [G3, B3, D4],
]
CHORD_S = 4.0

def lowpass(x, cutoff=1800.0):
    rc = 1.0 / (2 * np.pi * cutoff)
    a = (1 / SR) / (rc + 1 / SR)
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc); y[i] = acc
    return y

def pad_chord(freqs, dur):
    n = int(SR * dur); t = np.arange(n) / SR
    out = np.zeros(n)
    for f in freqs:
        for det in (-0.6, 0.0, 0.6):  # leve desafinação para encorpar
            ff = f * 2 ** (det / 1200)
            out += 0.55 * np.sin(2 * np.pi * ff * t)
            tri = 2 * np.abs(2 * (t * ff - np.floor(0.5 + t * ff))) - 1
            out += 0.18 * tri
    out /= len(freqs) * 3
    att = int(SR * 1.4); rel = int(SR * 1.6)
    env = np.ones(n)
    env[:att] = np.linspace(0, 1, att)
    env[-rel:] *= np.linspace(1, 0, rel)
    return out * env

def pluck(f, dur=1.6):
    n = int(SR * dur); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
    return x * np.exp(-t * 3.2) * 0.22

def main():
    total = float(sys.argv[1]); out_path = sys.argv[2]
    n_total = int(SR * total) + SR
    mix = np.zeros(n_total)
    t = 0.0; i = 0
    while t < total + CHORD_S:
        ch = CHORDS[i % 4]
        seg = pad_chord(ch, CHORD_S + 1.2)  # sobreposição para transição suave
        s = int(SR * t); e = min(n_total, s + len(seg))
        mix[s:e] += seg[: e - s]
        # arpejo discreto: uma nota por tempo (a cada 1 s), uma oitava acima
        for b in range(4):
            f = ch[b % 3] * 2
            p = pluck(f)
            ps = int(SR * (t + b * 1.0 + 0.5)); pe = min(n_total, ps + len(p))
            if ps < n_total: mix[ps:pe] += p[: pe - ps] * (0.9 if b == 0 else 0.6)
        t += CHORD_S; i += 1
    mix = mix[: int(SR * total)]
    mix = lowpass(mix, 2200.0)
    mix /= (np.max(np.abs(mix)) + 1e-9)
    mix *= 0.8
    # estéreo: canal direito com atraso curto para largura
    d = int(SR * 0.012)
    left = mix
    right = np.concatenate([np.zeros(d), mix[:-d]])
    st = np.stack([left, right], axis=1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(out_path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print('trilha', out_path, f'{total:.1f}s')

if __name__ == '__main__':
    main()

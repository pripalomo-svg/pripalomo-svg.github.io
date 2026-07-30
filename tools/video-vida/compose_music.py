"""
Compõe uma trilha instrumental original (piano + cordas suaves) para o vídeo,
usando uma progressão de acordes emotiva e nostálgica. Sem letra, sem
direitos autorais de terceiros -- composição original simples.
"""
import json
from pathlib import Path
from midiutil import MIDIFile

ROOT = Path(__file__).parent
timeline = json.loads((ROOT / "timeline.json").read_text())
total_s = timeline["totalDurationMs"] / 1000

TEMPO = 66  # bpm, andamento calmo
BEATS_PER_BAR = 4
# Progressão em Fá maior: F - C/E - Dm - Bb  (I - V/3 - vi - IV), quente e nostálgica
CHORDS = [
    [53, 60, 65],   # F3  A3(->F,C,A) -- usaremos tríades simples abaixo
]
# Tríades reais (nota raiz, terça, quinta) em oitava média
PROGRESSION = [
    (53, 57, 60),  # F3  A3  C4   (F maior)
    (48, 55, 60),  # C3  G3  C4   (C maior, 1ª inversão em baixo C)
    (50, 53, 57),  # D3  F3  A3   (D menor)
    (46, 53, 58),  # Bb2 F3  Bb3  (Bb maior)
]
BASS_ROOT = [41, 36, 38, 34]  # F2 C2 D2 Bb1

seconds_per_beat = 60.0 / TEMPO
bar_seconds = seconds_per_beat * BEATS_PER_BAR
n_bars = int(total_s / bar_seconds) + 2

midi = MIDIFile(3)
PIANO, PAD, BASS = 0, 1, 2
for track, name, program in [(PIANO, "Piano", 0), (PAD, "Pad", 89), (BASS, "Bass", 48)]:
    midi.addTrackName(track, 0, name)
    midi.addTempo(track, 0, TEMPO)
    midi.addProgramChange(track, 0, 0, program)

time = 0.0
for bar in range(n_bars):
    chord = PROGRESSION[bar % len(PROGRESSION)]
    bass_note = BASS_ROOT[bar % len(BASS_ROOT)]

    # Pad: acorde sustentado, uma nota longa por compasso, volume baixo
    for note in chord:
        midi.addNote(PAD, 0, note, time, bar_seconds * 0.98, 42)

    # Baixo: uma nota longa por compasso
    midi.addNote(BASS, 0, bass_note, time, bar_seconds * 0.95, 50)

    # Piano: arpejo suave subindo e descendo dentro do compasso
    arpeggio = list(chord) + [chord[0] + 12] + list(reversed(chord))
    step = bar_seconds / len(arpeggio)
    for i, note in enumerate(arpeggio):
        vel = 48 if i % 2 == 0 else 40
        midi.addNote(PIANO, 0, note, time + i * step, step * 0.9, vel)

    time += bar_seconds

midi_path = ROOT / "musica.mid"
with open(midi_path, "wb") as f:
    midi.writeFile(f)
print("wrote", midi_path, "duration ~", n_bars * bar_seconds, "s")

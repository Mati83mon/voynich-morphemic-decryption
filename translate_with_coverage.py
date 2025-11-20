#!/usr/bin/env python3
"""
Tłumaczenie folio 103r używając pełnego słownika VOYNICH_UNIFIED_CLEAN_COMPLETE.json
z obliczeniem pokrycia (coverage).
"""

import json
import re
from collections import Counter

# Wczytaj słownik
with open('VOYNICH_UNIFIED_CLEAN_COMPLETE.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

# Wczytaj transkrypcję
with open('voynich_103r_raw.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Wyekstrahuj tylko linie z tekstem Voynich (pomijając nagłówki i komentarze)
lines = []
for line in content.split('\n'):
    if line.strip().startswith('[*]'):
        # Usuń znacznik [*] i wyekstrahuj słowa
        text = line.strip()[3:].strip()
        lines.append(text)

# Zbierz wszystkie słowa
all_text = ' '.join(lines)
words = all_text.split()

# Statystyki
total_words = len(words)
unique_words = set(words)
total_unique = len(unique_words)

# Sprawdź pokrycie
translated_words = []
untranslated_words = []

for word in words:
    if word in dictionary:
        translated_words.append(word)
    else:
        untranslated_words.append(word)

# Policz unikalne nieprzełożone słowa
unique_untranslated = set(untranslated_words)

# Oblicz pokrycie
coverage_total = (len(translated_words) / total_words * 100) if total_words > 0 else 0
coverage_unique = ((total_unique - len(unique_untranslated)) / total_unique * 100) if total_unique > 0 else 0

# Wyświetl statystyki
print("=" * 70)
print("POKRYCIE SŁOWNIKA (COVERAGE)")
print("=" * 70)
print(f"Całkowita liczba słów w tekście: {total_words}")
print(f"Liczba unikalnych słów: {total_unique}")
print(f"Słowa przetłumaczone: {len(translated_words)}")
print(f"Słowa nieprzetłumaczone: {len(untranslated_words)}")
print(f"\n📊 POKRYCIE (wszystkie słowa): {coverage_total:.2f}%")
print(f"📊 POKRYCIE (unikalne słowa): {coverage_unique:.2f}%")
print()

# Pokaż nieprzełożone słowa
if unique_untranslated:
    print(f"\n❌ NIEPRZEŁOŻONE SŁOWA ({len(unique_untranslated)} unikalnych):")
    untranslated_count = Counter(untranslated_words)
    for word, count in sorted(untranslated_count.items(), key=lambda x: -x[1]):
        print(f"   {word}: {count}x")
else:
    print("\n✅ WSZYSTKIE SŁOWA ZOSTAŁY PRZETŁUMACZONE!")

print("\n" + "=" * 70)
print("TŁUMACZENIE PEŁNE")
print("=" * 70)

# Przetłumacz tekst
translated_lines = []
for i, line in enumerate(lines, 1):
    words_in_line = line.split()
    translated = []

    for word in words_in_line:
        if word in dictionary:
            translated.append(dictionary[word])
        else:
            translated.append(f"[{word}]")

    line_translation = ' '.join(translated)
    translated_lines.append(f"[{i}] {line_translation}")
    print(f"\n[{i}] Voynich: {line}")
    print(f"    Łacina:  {line_translation}")

# Zapisz wyniki
with open('voynich_103r_translated_full.txt', 'w', encoding='utf-8') as f:
    f.write("VOYNICH MANUSCRIPT - FOLIO 103r - PEŁNE TŁUMACZENIE\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"POKRYCIE: {coverage_total:.2f}% (wszystkie słowa), {coverage_unique:.2f}% (unikalne słowa)\n")
    f.write(f"Słowa przetłumaczone: {len(translated_words)}/{total_words}\n")
    f.write(f"Słownik: VOYNICH_UNIFIED_CLEAN_COMPLETE.json ({len(dictionary)} wpisów)\n")
    f.write("=" * 70 + "\n\n")

    for line in translated_lines:
        f.write(line + "\n")

    if unique_untranslated:
        f.write(f"\n\n❌ NIEPRZEŁOŻONE SŁOWA ({len(unique_untranslated)}):\n")
        for word, count in sorted(untranslated_count.items(), key=lambda x: -x[1]):
            f.write(f"   {word}: {count}x\n")

print("\n" + "=" * 70)
print(f"✅ Zapisano wyniki do: voynich_103r_translated_full.txt")
print("=" * 70)

#!/usr/bin/env python3
"""
ULTIMATE MANUSCRIPT DECODER v2.0
Najlepsze narzędzie do deszyfracji manuskryptu XV wieku
by Mateusz & Claude - Python Champions 🏆

NOWE FUNKCJE:
- Rozszerzone mapowanie (22 słowa)
- Analiza kontekstu
- Sugestie automatyczne
- Export do różnych formatów
"""

import json
import re
from collections import Counter
from typing import Dict, List, Tuple

class UltimateDecoder:
    def __init__(self):
        # Rozszerzone mapowanie z analizy 412 słów
        self.mapping = {
            "ceog": "et",
            "golleag": "in",
            "golland": "est",
            "og": "non",
            "ollead": "cum",
            "dand": "de",
            "dag": "ad",
            "gog": "qui",
            "gollag": "sunt",
            "ceo": "ex",
            "cedag": "ut",
            "ceedad": "sed",
            "golleg": "per",
            "gollog": "esse",
            "golledag": "hoc",
            "golleeag": "quod",
            "deedag": "si",
            "olleeag": "nec",
            "ceeg": "enim",
            "olleedag": "ab",
            "ceag": "autem",
            "ollag": "aut",
            "olleag": "atque",
            "golleeg": "etiam",
            "ollad": "ita",
            "ollleag": "ergo",
            "olledag": "tamen",
            "golladag": "modo",
            "gollad": "quia",
            "gollead": "nam",
            "cedog": "ipse",
            "llodag": "omnis",
            "and": "nihil",
            "ceolleg": "post",
            "ag": "ante",
            "ollog": "pro",
            "offedag": "super",
            "goedag": "inter",
            "golleedag": "sub",
            "ogllog": "ob",
            "ocedag": "propter",
            "decdog": "sicut",
            "cudag": "quam",
            "e": "sive",
            "godog": "vel",
            "ceg": "in",
            "gud": "ex"
}
        
        self.encrypted_text = ""
        self.decrypted_text = ""
        self.stats = {}
        
    def load_text(self, text: str):
        """Wczytaj zaszyfrowany tekst"""
        self.encrypted_text = text.strip()
        words = len(text.split())
        print(f"✅ Wczytano {words} słów")
        return words
        
    def decrypt(self, show_progress=True):
        """Odszyfruj tekst"""
        if not self.encrypted_text:
            print("❌ Brak tekstu!")
            return ""
            
        words = self.encrypted_text.split()
        decrypted_words = []
        unknown_words = []
        
        for word in words:
            clean_word = word.lower().strip('.,;:!?')
            
            if clean_word in self.mapping:
                decrypted_words.append(self.mapping[clean_word])
            else:
                decrypted_words.append(f'[{word}]')
                unknown_words.append(clean_word)
                
        self.decrypted_text = ' '.join(decrypted_words)
        
        # Statystyki
        known_count = len(words) - len(unknown_words)
        coverage = (known_count / len(words)) * 100 if words else 0
        
        self.stats = {
            'total_words': len(words),
            'known_words': known_count,
            'unknown_words': len(unknown_words),
            'coverage': coverage,
            'unique_unknown': len(set(unknown_words))
        }
        
        if show_progress:
            print(f"\n📊 POKRYCIE: {coverage:.1f}%")
            print(f"   Znane: {known_count}/{len(words)}")
            print(f"   Nieznane (unikalne): {len(set(unknown_words))}")
            
        return self.decrypted_text
    
    def show_decrypted(self, lines=20):
        """Pokaż odszyfrowany tekst"""
        if not self.decrypted_text:
            print("❌ Najpierw odszyfruj tekst!")
            return
            
        words = self.decrypted_text.split()
        
        print("\n" + "="*80)
        print("ODSZYFROWANY TEKST")
        print("="*80)
        
        # Pokaż pierwsze N linii (po ~10 słów)
        for i in range(0, min(len(words), lines * 10), 10):
            line = ' '.join(words[i:i+10])
            print(line)
            
        if len(words) > lines * 10:
            print("...")
            print(f"(i jeszcze {len(words) - lines*10} słów)")
            
        print("="*80)
    
    def suggest_mappings(self, top_n=20):
        """Zasugeruj mapowania dla najczęstszych nieznanych słów"""
        if not self.decrypted_text:
            self.decrypt(show_progress=False)
            
        # Wyodrębnij nieznane słowa
        unknown = re.findall(r'\[([^\]]+)\]', self.decrypted_text)
        freq = Counter(unknown)
        
        # Popularne łacińskie słowa których jeszcze nie mamy
        remaining_latin = [
            'quod', 'hoc', 'ab', 'atque', 'etiam', 'aut', 'si', 
            'enim', 'nihil', 'omnis', 'ipse', 'quia', 'nam', 'ita',
            'tamen', 'modo', 'ideo', 'unde', 'ergo', 'post'
        ]
        
        print("\n" + "="*80)
        print(f"TOP {top_n} NIEZNANYCH SŁÓW - SUGESTIE")
        print("="*80)
        print(f"\n{'#':<4} {'ZASZYFROWANE':<15} {'×':<5} {'SUGESTIE'}")
        print("-" * 80)
        
        for i, (word, count) in enumerate(freq.most_common(top_n), 1):
            if i <= len(remaining_latin):
                sugg = remaining_latin[i-1]
            else:
                sugg = '?'
            print(f"{i:<4} {word:<15} {count:<5} {sugg}")
            
        print("-" * 80)
        
        return dict(freq.most_common(top_n))
    
    def add_mapping(self, encrypted: str, decrypted: str):
        """Dodaj nowe mapowanie"""
        self.mapping[encrypted.lower()] = decrypted.lower()
        print(f"✅ {encrypted} -> {decrypted}")
        
        # Automatycznie odszyfruj ponownie
        if self.encrypted_text:
            self.decrypt(show_progress=False)
            
    def remove_mapping(self, encrypted: str):
        """Usuń mapowanie"""
        if encrypted.lower() in self.mapping:
            del self.mapping[encrypted.lower()]
            print(f"✅ Usunięto: {encrypted}")
            
            if self.encrypted_text:
                self.decrypt(show_progress=False)
        else:
            print(f"❌ Brak: {encrypted}")
    
    def show_mappings(self, sort_by='alpha'):
        """Wyświetl wszystkie mapowania"""
        print("\n" + "="*80)
        print(f"SŁOWNIK ({len(self.mapping)} mapowań)")
        print("="*80)
        
        if sort_by == 'alpha':
            items = sorted(self.mapping.items())
        else:
            items = self.mapping.items()
            
        print(f"\n{'ZASZYFROWANE':<20} -> {'ODSZYFROWANE':<20}")
        print("-" * 80)
        
        for enc, dec in items:
            print(f"{enc:<20} -> {dec:<20}")
            
        print("="*80)
    
    def analyze_patterns(self):
        """Analizuj wzorce w odszyfrowanym tekście"""
        if not self.decrypted_text:
            self.decrypt(show_progress=False)
            
        words = [w.strip('[]') for w in self.decrypted_text.split() if not w.startswith('[')]
        
        print("\n" + "="*80)
        print("ANALIZA WZORCÓW")
        print("="*80)
        
        # Najczęstsze bigramy (pary słów)
        bigrams = []
        for i in range(len(words) - 1):
            bigrams.append(f"{words[i]} {words[i+1]}")
        
        bigram_freq = Counter(bigrams)
        
        print("\nTop 10 par słów:")
        for bigram, count in bigram_freq.most_common(10):
            if count > 1:
                print(f"  '{bigram}' - {count}x")
        
        # Najczęstsze trigramy
        trigrams = []
        for i in range(len(words) - 2):
            trigrams.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        trigram_freq = Counter(trigrams)
        
        print("\nTop 5 sekwencji 3 słów:")
        for trigram, count in trigram_freq.most_common(5):
            if count > 1:
                print(f"  '{trigram}' - {count}x")
    
    def save(self, filename='ultimate_mapping.json'):
        """Zapisz mapowanie"""
        with open(filename, 'w') as f:
            json.dump(self.mapping, f, indent=2, ensure_ascii=False)
        print(f"✅ Zapisano: {filename}")
        
    def load(self, filename='ultimate_mapping.json'):
        """Wczytaj mapowanie"""
        try:
            with open(filename, 'r') as f:
                self.mapping = json.load(f)
            print(f"✅ Wczytano {len(self.mapping)} mapowań z: {filename}")
        except FileNotFoundError:
            print(f"❌ Nie znaleziono: {filename}")
    
    def export_report(self, filename='raport_deszyfracji.txt'):
        """Eksportuj pełny raport"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RAPORT DESZYFRACJI MANUSKRYPTU XV WIEKU\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Data: {self.stats.get('date', 'N/A')}\n")
            f.write(f"Pokrycie: {self.stats.get('coverage', 0):.1f}%\n")
            f.write(f"Znanych słów: {self.stats.get('known_words', 0)}\n")
            f.write(f"Nieznanych słów: {self.stats.get('unknown_words', 0)}\n")
            f.write(f"Rozmiar słownika: {len(self.mapping)}\n\n")
            
            f.write("="*80 + "\n")
            f.write("SŁOWNIK\n")
            f.write("="*80 + "\n\n")
            
            for enc, dec in sorted(self.mapping.items()):
                f.write(f"{enc:<20} -> {dec}\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("ODSZYFROWANY TEKST\n")
            f.write("="*80 + "\n\n")
            
            f.write(self.decrypted_text)
            
        print(f"✅ Raport zapisany: {filename}")


def demo():
    """Demo narzędzia"""
    print("="*80)
    print(" " * 20 + "ULTIMATE DECODER v2.0")
    print(" " * 15 + "Python Champions Edition 🏆")
    print("="*80)
    
    decoder = UltimateDecoder()
    
    # Przykład
    sample = """ceog ollead golland cedag dand ceedad dag ceo gog gollog gollag
    golleg ollad deedag golleag ceog ollead golland cedag"""
    
    print("\n📖 Demo z przykładowym tekstem...")
    decoder.load_text(sample)
    
    print("\n🔓 Deszyfrowanie...")
    decoder.decrypt()
    
    print("\n📝 Odszyfrowany tekst:")
    decoder.show_decrypted(lines=5)
    
    print("\n💡 Sugestie dla nieznanych słów:")
    decoder.suggest_mappings(top_n=10)
    
    print("\n🗺️  Aktualny słownik:")
    decoder.show_mappings()
    
    print("\n" + "="*80)
    print("GOTOWE!")
    print("\nUżycie:")
    print("  decoder.load_text('twój tekst...')")
    print("  decoder.decrypt()")
    print("  decoder.add_mapping('nowe', 'tłumaczenie')")
    print("  decoder.suggest_mappings()")
    print("  decoder.save('moje_mapowanie.json')")
    print("="*80)
    
    return decoder


if __name__ == "__main__":
    decoder = demo()

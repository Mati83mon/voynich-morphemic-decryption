#!/usr/bin/env python3
"""
Manuscript Cryptanalysis Tool
Narzędzie do analizy i deszyfrowania średniowiecznych manuskryptów
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

class ManuscriptAnalyzer:
    def __init__(self):
        self.encrypted_text = ""
        self.key_mappings = {}
        self.word_frequencies = Counter()
        
    def load_key(self, key_text: str):
        """Wczytaj klucz deszyfrujący"""
        # Parsuj klucz i wyodrębnij mapowania
        words = re.findall(r'\b[a-zA-Z]+\b', key_text)
        
        # Utwórz pary mapowań
        for i in range(0, len(words)-1, 2):
            self.key_mappings[words[i]] = words[i+1]
            
        print(f"Wczytano {len(self.key_mappings)} mapowań z klucza")
        return self.key_mappings
    
    def analyze_frequency(self, text: str):
        """Analiza częstotliwości słów"""
        words = text.lower().split()
        self.word_frequencies = Counter(words)
        
        print("\n=== TOP 20 NAJCZĘSTSZYCH SŁÓW ===")
        for word, count in self.word_frequencies.most_common(20):
            print(f"{word:15} -> {count:4}x")
            
        return self.word_frequencies
    
    def find_patterns(self, text: str):
        """Znajdź powtarzające się wzorce"""
        words = text.lower().split()
        
        # Bigramy (pary słów)
        bigrams = Counter()
        for i in range(len(words)-1):
            bigrams[(words[i], words[i+1])] += 1
        
        # Trigramy (trójki słów)
        trigrams = Counter()
        for i in range(len(words)-2):
            trigrams[(words[i], words[i+1], words[i+2])] += 1
        
        print("\n=== NAJCZĘSTSZE BIGRAMY ===")
        for bigram, count in bigrams.most_common(10):
            if count > 1:
                print(f"{' '.join(bigram):30} -> {count}x")
        
        print("\n=== NAJCZĘSTSZE TRIGRAMY ===")
        for trigram, count in trigrams.most_common(10):
            if count > 1:
                print(f"{' '.join(trigram):40} -> {count}x")
                
        return bigrams, trigrams
    
    def try_substitution(self, encrypted_text: str, mapping: Dict[str, str]):
        """Spróbuj podstawienia według podanego mapowania"""
        words = encrypted_text.lower().split()
        decrypted_words = []
        
        for word in words:
            # Usuń interpunkcję
            clean_word = re.sub(r'[^\w]', '', word)
            
            # Spróbuj podstawić
            if clean_word in mapping:
                decrypted_words.append(f"[{mapping[clean_word]}]")
            else:
                decrypted_words.append(word)
        
        return ' '.join(decrypted_words)
    
    def statistical_analysis(self, text: str):
        """Analiza statystyczna tekstu"""
        words = text.lower().split()
        
        stats = {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'lexical_diversity': len(set(words)) / len(words) if words else 0
        }
        
        print("\n=== STATYSTYKI TEKSTU ===")
        print(f"Całkowita liczba słów: {stats['total_words']}")
        print(f"Unikalne słowa: {stats['unique_words']}")
        print(f"Średnia długość słowa: {stats['avg_word_length']:.2f}")
        print(f"Różnorodność leksykalna: {stats['lexical_diversity']:.3f}")
        
        # Długości słów
        lengths = Counter(len(w) for w in words)
        print("\nRozkład długości słów:")
        for length in sorted(lengths.keys()):
            print(f"  {length} liter: {lengths[length]:4}x {'█' * (lengths[length] // 10)}")
        
        return stats
    
    def compare_with_key(self, encrypted_text: str, key_words: List[str]):
        """Porównaj słowa z tekstu zaszyfrowanego z kluczem"""
        encrypted_words = set(encrypted_text.lower().split())
        key_word_set = set(w.lower() for w in key_words)
        
        # Znajdź wspólne słowa
        common = encrypted_words & key_word_set
        
        print("\n=== PORÓWNANIE Z KLUCZEM ===")
        if common:
            print(f"Znaleziono {len(common)} wspólnych słów:")
            for word in sorted(common):
                print(f"  - {word}")
        else:
            print("Brak bezpośrednich dopasowań.")
            print("Szukam podobnych słów...")
            
            # Znajdź podobne słowa (edit distance = 1-2)
            for enc_word in sorted(encrypted_words)[:20]:  # Top 20
                for key_word in key_word_set:
                    if self._similarity(enc_word, key_word) > 0.7:
                        print(f"  {enc_word} ~?~ {key_word}")
        
        return common
    
    def _similarity(self, word1: str, word2: str) -> float:
        """Prosta miara podobieństwa słów"""
        if not word1 or not word2:
            return 0.0
        
        max_len = max(len(word1), len(word2))
        matches = sum(1 for a, b in zip(word1, word2) if a == b)
        
        return matches / max_len


# GŁÓWNA FUNKCJA ANALIZY
def main():
    analyzer = ManuscriptAnalyzer()
    
    print("="*70)
    print("MANUSCRIPT CRYPTANALYSIS TOOL v1.0")
    print("="*70)
    
    # Przykładowy tekst zaszyfrowany (fragment ze strony 116)
    sample_encrypted = """
    ollag ceg gollad ollag e ceg ceeg gud og ogolg oegolsog
    oud eug keg geeg ceeg ceg cear og ollag gllad og
    eg sollog oleg sheg golkog ollag egg e eallo
    gollad ceg aceglo gog kano ceoleg ollag aceg olledag gollolo ollag og
    gand eeee golleeag ollag ceeg olkang allag ceeg o ollag og geg eeg
    geag olleg oloeg oler ceeg og ceeg olegoad ollag olleg
    geog ceeg olledag olleg go gollaig golleg gollad olleg kollog tollag
    dag olledag ceeg golleg gollad goloeg olleedar olledag gag keedog
    """
    
    # Klucz
    key_text = """
    anchiron olaSabad e od cenea poneal cri
    in anna morra wa chiry morrra
    otor enea vulgen ulizen o mm galmisch
    """
    
    print("\n" + "="*70)
    print("ANALIZA TEKSTU ZASZYFROWANEGO")
    print("="*70)
    
    # Analiza częstotliwości
    analyzer.analyze_frequency(sample_encrypted)
    
    # Analiza statystyczna
    analyzer.statistical_analysis(sample_encrypted)
    
    # Wzorce
    analyzer.find_patterns(sample_encrypted)
    
    # Wczytaj klucz
    print("\n" + "="*70)
    print("ANALIZA KLUCZA")
    print("="*70)
    key_mappings = analyzer.load_key(key_text)
    
    # Porównaj z kluczem
    key_words = re.findall(r'\b[a-zA-Z]+\b', key_text)
    analyzer.compare_with_key(sample_encrypted, key_words)
    
    print("\n" + "="*70)
    print("GOTOWE! Potrzeba więcej danych do pełnej deszyfracji.")
    print("="*70)

if __name__ == "__main__":
    main()

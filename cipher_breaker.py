#!/usr/bin/env python3
"""
Advanced Manuscript Decryption Tool
Zaawansowane narzędzie do łamania szyfrów średniowiecznych
by Mateusz - Python Champion 🏆
"""

import string
import itertools
from collections import Counter
from typing import List, Dict, Tuple, Optional

class CipherBreaker:
    """Ultimate cipher breaker dla średniowiecznych manuskryptów"""
    
    def __init__(self):
        # Najpopularniejsze słowa w różnych językach
        self.common_words = {
            'latin': ['et', 'in', 'non', 'est', 'cum', 'ad', 'de', 'qui', 'sunt', 'ex', 'ut', 'se', 'sed', 'esse'],
            'german': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'für'],
            'english': ['the', 'and', 'of', 'to', 'a', 'in', 'is', 'that', 'for', 'it', 'with', 'as', 'was'],
            'polish': ['w', 'i', 'na', 'z', 'do', 'się', 'o', 'nie', 'że', 'to', 'jest', 'co', 'jak']
        }
        
    def method_1_frequency_substitution(self, encrypted: str, target_lang='latin'):
        """Metoda 1: Podstawienie oparte na częstotliwości"""
        print("\n" + "="*70)
        print("METODA 1: FREQUENCY-BASED SUBSTITUTION")
        print("="*70)
        
        words = encrypted.lower().split()
        freq = Counter(words)
        most_common = [word for word, count in freq.most_common(20)]
        
        target_common = self.common_words.get(target_lang, self.common_words['latin'])
        
        mapping = {}
        for i, enc_word in enumerate(most_common[:len(target_common)]):
            mapping[enc_word] = target_common[i]
            
        print(f"\nPróba deszyfracji dla języka: {target_lang.upper()}")
        print("\nMapowanie (top 10):")
        for enc, dec in list(mapping.items())[:10]:
            print(f"  {enc:12} -> {dec}")
            
        # Zastosuj mapowanie
        decrypted_words = []
        for word in words:
            clean_word = word.lower().strip()
            if clean_word in mapping:
                decrypted_words.append(f"**{mapping[clean_word]}**")
            else:
                decrypted_words.append(word)
                
        result = ' '.join(decrypted_words)
        print("\nPierwsze 200 znaków:")
        print(result[:200] + "...")
        
        return mapping, result
    
    def method_2_pattern_matching(self, encrypted: str):
        """Metoda 2: Dopasowanie wzorców słów"""
        print("\n" + "="*70)
        print("METODA 2: PATTERN MATCHING")
        print("="*70)
        
        def get_pattern(word):
            """Zwraca wzorzec słowa (np. 'hello' -> '01223')"""
            mapping = {}
            pattern = []
            counter = 0
            for char in word.lower():
                if char not in mapping:
                    mapping[char] = str(counter)
                    counter += 1
                pattern.append(mapping[char])
            return ''.join(pattern)
        
        # Słownik wzorców dla popularnych łacińskich słów
        latin_patterns = {
            '01': ['et', 'in', 'ad', 'ut', 'se'],
            '012': ['est', 'non', 'cum', 'sed', 'nec'],
            '0123': ['esse', 'sunt', 'enim'],
            '01223': ['terra', 'pater'],
        }
        
        words = encrypted.lower().split()
        pattern_matches = {}
        
        for word in set(words):
            pattern = get_pattern(word)
            if pattern in latin_patterns:
                pattern_matches[word] = latin_patterns[pattern]
                
        print(f"\nZnaleziono {len(pattern_matches)} dopasowań wzorców:")
        for enc_word, possible_words in list(pattern_matches.items())[:10]:
            print(f"  {enc_word:12} -> {', '.join(possible_words)}")
            
        return pattern_matches
    
    def method_3_anagram_attack(self, encrypted: str):
        """Metoda 3: Atak anagramowy (jeśli to transpozycja)"""
        print("\n" + "="*70)
        print("METODA 3: ANAGRAM/TRANSPOSITION ATTACK")
        print("="*70)
        
        words = encrypted.lower().split()
        latin_words = ['et', 'in', 'non', 'est', 'cum', 'ad', 'de', 'qui', 'sunt', 'ex', 
                       'ut', 'se', 'sed', 'esse', 'enim', 'aut', 'per', 'inter', 'pro']
        
        anagram_matches = {}
        
        for enc_word in set(words):
            for lat_word in latin_words:
                if sorted(enc_word) == sorted(lat_word):
                    anagram_matches[enc_word] = lat_word
                    
        if anagram_matches:
            print(f"\nZnaleziono {len(anagram_matches)} potencjalnych anagramów:")
            for enc, dec in anagram_matches.items():
                print(f"  {enc:12} -> {dec}")
        else:
            print("\nBrak bezpośrednich anagramów. Próba permutacji...")
            
        return anagram_matches
    
    def method_4_vigenere_bruteforce(self, encrypted: str, max_key_length=10):
        """Metoda 4: Bruteforce Vigenère z kluczami do 10 znaków"""
        print("\n" + "="*70)
        print("METODA 4: VIGENÈRE BRUTEFORCE")
        print("="*70)
        
        def vigenere_decrypt(text, key):
            result = []
            key_repeated = (key * (len(text) // len(key) + 1))[:len(text)]
            
            for i, char in enumerate(text):
                if char.isalpha():
                    shift = ord(key_repeated[i].lower()) - ord('a')
                    base = ord('a') if char.islower() else ord('A')
                    decrypted_char = chr((ord(char) - base - shift) % 26 + base)
                    result.append(decrypted_char)
                else:
                    result.append(char)
                    
            return ''.join(result)
        
        # Najpopularniejsze średniowieczne klucze
        common_keys = ['pater', 'deus', 'rex', 'sanctus', 'domini', 'iesus', 
                       'maria', 'lux', 'veritas', 'vita', 'amor', 'pax']
        
        print("\nPróba z popularnymi średniowiecznymi kluczami:")
        
        best_score = 0
        best_result = None
        best_key = None
        
        for key in common_keys:
            decrypted = vigenere_decrypt(encrypted[:100], key)
            
            # Oceń wynik (prosty scoring - liczba samogłosek)
            score = sum(1 for c in decrypted.lower() if c in 'aeiou')
            
            if score > best_score:
                best_score = score
                best_result = decrypted
                best_key = key
                
        print(f"\nNajlepszy klucz: '{best_key}' (score: {best_score})")
        print(f"Wynik: {best_result}")
        
        return best_key, best_result
    
    def method_5_word_substitution_dict(self, encrypted: str, key_dict: Dict[str, str]):
        """Metoda 5: Podstawienie słownikowe (używa dostarczonego klucza)"""
        print("\n" + "="*70)
        print("METODA 5: DICTIONARY SUBSTITUTION (z kluczem)")
        print("="*70)
        
        if not key_dict:
            print("Brak klucza słownikowego!")
            return None
            
        words = encrypted.split()
        decrypted_words = []
        
        substitutions_made = 0
        
        for word in words:
            clean_word = word.lower().strip('.,;:!?')
            
            if clean_word in key_dict:
                decrypted_words.append(f"**{key_dict[clean_word]}**")
                substitutions_made += 1
            else:
                decrypted_words.append(word)
                
        result = ' '.join(decrypted_words)
        
        print(f"\nDokonano {substitutions_made} podstawień")
        print("\nPierwsze 300 znaków:")
        print(result[:300] + "...")
        
        return result
    
    def method_6_letter_frequency_analysis(self, encrypted: str):
        """Metoda 6: Analiza częstotliwości liter (nie słów)"""
        print("\n" + "="*70)
        print("METODA 6: LETTER FREQUENCY ANALYSIS")
        print("="*70)
        
        # Usuń spacje i policz litery
        letters_only = ''.join(c for c in encrypted.lower() if c.isalpha())
        freq = Counter(letters_only)
        
        # Częstotliwości w łacinie
        latin_freq = 'eiatunosrlcmdpgbfvhqxyz'
        
        # Stwórz mapowanie
        most_common_letters = [letter for letter, count in freq.most_common()]
        letter_mapping = {}
        
        for i, enc_letter in enumerate(most_common_letters):
            if i < len(latin_freq):
                letter_mapping[enc_letter] = latin_freq[i]
                
        print("\nNajczęstsze litery w tekście zaszyfrowanym:")
        for i, (letter, count) in enumerate(freq.most_common(10), 1):
            pct = (count / len(letters_only)) * 100
            print(f"  {i:2}. {letter} -> {count:5}x ({pct:5.2f}%)")
            
        print("\nPróba mapowania na łaciński alfabet częstotliwości:")
        for enc, dec in list(letter_mapping.items())[:10]:
            print(f"  {enc} -> {dec}")
            
        # Zastosuj mapowanie
        decrypted = []
        for char in encrypted:
            if char.lower() in letter_mapping:
                new_char = letter_mapping[char.lower()]
                decrypted.append(new_char.upper() if char.isupper() else new_char)
            else:
                decrypted.append(char)
                
        result = ''.join(decrypted)
        print("\nPierwsze 200 znaków:")
        print(result[:200] + "...")
        
        return letter_mapping, result
    
    def analyze_all_methods(self, encrypted_text: str, key_dict: Optional[Dict] = None):
        """Wypróbuj WSZYSTKIE metody naraz!"""
        print("\n" + "="*80)
        print(" " * 20 + "ULTIMATE CIPHER BREAKER")
        print(" " * 15 + "Próba wszystkich znanych metod!")
        print("="*80)
        
        results = {}
        
        # Metoda 1
        for lang in ['latin', 'german', 'english']:
            mapping, result = self.method_1_frequency_substitution(encrypted_text, lang)
            results[f'freq_{lang}'] = (mapping, result)
            
        # Metoda 2
        results['patterns'] = self.method_2_pattern_matching(encrypted_text)
        
        # Metoda 3
        results['anagrams'] = self.method_3_anagram_attack(encrypted_text)
        
        # Metoda 4
        results['vigenere'] = self.method_4_vigenere_bruteforce(encrypted_text)
        
        # Metoda 5 (jeśli jest klucz)
        if key_dict:
            results['dictionary'] = self.method_5_word_substitution_dict(encrypted_text, key_dict)
            
        # Metoda 6
        results['letter_freq'] = self.method_6_letter_frequency_analysis(encrypted_text)
        
        print("\n" + "="*80)
        print("ANALIZA ZAKOŃCZONA!")
        print("="*80)
        
        return results


# DEMO
if __name__ == "__main__":
    breaker = CipherBreaker()
    
    # Przykładowy zaszyfrowany tekst
    sample = """
    ollag ceg gollad ollag e ceg ceeg gud og ogolg oegolsog
    oud eug keg geeg ceeg ceg cear og ollag gllad og
    eg sollog oleg sheg golkog ollag egg e eallo
    """
    
    print("DEMONSTRACJA - uruchamiam wszystkie metody...\n")
    print("(Na prawdziwym tekście będzie działać znacznie lepiej!)")
    
    results = breaker.analyze_all_methods(sample)
    
    print("\n" + "="*80)
    print("Gotowe! To narzędzie może teraz przeanalizować cały manuskrypt!")
    print("="*80)

#!/usr/bin/env python3
"""
Interactive Manuscript Decoder
Interaktywne narzędzie do deszyfrowania manuskryptu
by Mateusz - Python Champion 🏆

Użycie:
    python3 interactive_decoder.py
"""

import json
from typing import Dict, List

class InteractiveDecoder:
    def __init__(self):
        self.mapping = {
            # Bazowe mapowanie z analizy
            'ollag': 'et',
            'ceg': 'in',
            'og': 'non',
            'ceeg': 'cum',
            'gollad': 'ad',
            'e': 'qui',
            'gud': 'ex',
        }
        
        self.encrypted_text = ""
        self.decrypted_text = ""
        
    def load_encrypted_text(self, text: str):
        """Wczytaj tekst zaszyfrowany"""
        self.encrypted_text = text.strip()
        print(f"✅ Wczytano {len(text.split())} słów")
        
    def add_mapping(self, encrypted_word: str, decrypted_word: str):
        """Dodaj nowe mapowanie"""
        self.mapping[encrypted_word.lower()] = decrypted_word.lower()
        print(f"✅ Dodano: {encrypted_word} -> {decrypted_word}")
        
    def remove_mapping(self, encrypted_word: str):
        """Usuń mapowanie"""
        if encrypted_word.lower() in self.mapping:
            del self.mapping[encrypted_word.lower()]
            print(f"✅ Usunięto mapowanie dla: {encrypted_word}")
        else:
            print(f"❌ Brak mapowania dla: {encrypted_word}")
            
    def show_mappings(self):
        """Wyświetl wszystkie mapowania"""
        print("\n" + "="*60)
        print("AKTUALNE MAPOWANIA")
        print("="*60)
        
        if not self.mapping:
            print("Brak mapowań!")
            return
            
        # Posortuj po długości (najczęstsze na górze)
        sorted_mappings = sorted(self.mapping.items(), key=lambda x: x[0])
        
        print(f"\n{'ZASZYFROWANE':<20} -> {'ODSZYFROWANE':<20}")
        print("-" * 60)
        for enc, dec in sorted_mappings:
            print(f"{enc:<20} -> {dec:<20}")
        print(f"\nRazem: {len(self.mapping)} mapowań")
        print("="*60)
        
    def decrypt(self, show_unknown=True):
        """Odszyfruj tekst używając aktualnych mapowań"""
        if not self.encrypted_text:
            print("❌ Brak tekstu do odszyfrowania!")
            return ""
            
        words = self.encrypted_text.split()
        decrypted_words = []
        unknown_words = set()
        
        for word in words:
            clean_word = word.lower().strip('.,;:!?')
            
            if clean_word in self.mapping:
                # Słowo znalezione w mapowaniu
                decrypted_words.append(self.mapping[clean_word])
            else:
                # Słowo nieznane - oznacz to
                if show_unknown:
                    decrypted_words.append(f"[{word}]")
                    unknown_words.add(clean_word)
                else:
                    decrypted_words.append(word)
                    
        self.decrypted_text = ' '.join(decrypted_words)
        
        print("\n" + "="*60)
        print("ODSZYFROWANY TEKST")
        print("="*60)
        print(self.decrypted_text)
        print("="*60)
        
        if unknown_words:
            print(f"\n⚠️  Nieznane słowa ({len(unknown_words)}):")
            for word in sorted(unknown_words)[:20]:  # Pokaż max 20
                print(f"  - {word}")
            if len(unknown_words) > 20:
                print(f"  ... i {len(unknown_words) - 20} więcej")
                
        coverage = (len(words) - len(unknown_words)) / len(words) * 100
        print(f"\n📊 Pokrycie: {coverage:.1f}%")
        
        return self.decrypted_text
    
    def suggest_words(self, context_before: str, context_after: str):
        """Zasugeruj możliwe słowa na podstawie kontekstu"""
        print("\n" + "="*60)
        print("SUGESTIE NA PODSTAWIE KONTEKSTU")
        print("="*60)
        
        # Popularne łacińskie słowa w kontekście
        suggestions = {
            'et': ['autem', 'sed', 'nam', 'enim'],
            'in': ['per', 'ad', 'ex', 'de'],
            'non': ['nec', 'neque', 'nihil'],
            'cum': ['inter', 'apud'],
        }
        
        before_lower = context_before.lower()
        after_lower = context_after.lower()
        
        print(f"Kontekst: '{context_before}' [???] '{context_after}'")
        print("\nMożliwe słowa:")
        
        # Sprawdź czy przed/po są w mapowaniu
        for enc, dec in self.mapping.items():
            if dec in suggestions:
                print(f"\nJeśli poprzednie to '{dec}', następne może być:")
                for sugg in suggestions[dec]:
                    print(f"  - {sugg}")
                    
    def save_mapping(self, filename='mapping.json'):
        """Zapisz mapowanie do pliku"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.mapping, f, indent=2, ensure_ascii=False)
        print(f"✅ Mapowanie zapisane do: {filename}")
        
    def load_mapping(self, filename='mapping.json'):
        """Wczytaj mapowanie z pliku"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.mapping = json.load(f)
            print(f"✅ Wczytano {len(self.mapping)} mapowań z: {filename}")
        except FileNotFoundError:
            print(f"❌ Plik nie znaleziony: {filename}")
            
    def statistics(self):
        """Pokaż statystyki"""
        if not self.encrypted_text:
            print("❌ Brak tekstu!")
            return
            
        words = self.encrypted_text.split()
        known = sum(1 for w in words if w.lower().strip('.,;:!?') in self.mapping)
        
        print("\n" + "="*60)
        print("STATYSTYKI")
        print("="*60)
        print(f"Całkowita liczba słów: {len(words)}")
        print(f"Znane słowa: {known}")
        print(f"Nieznane słowa: {len(words) - known}")
        print(f"Pokrycie: {known/len(words)*100:.1f}%")
        print(f"Rozmiar słownika: {len(self.mapping)} mapowań")
        print("="*60)
        

def demo():
    """Demonstracja narzędzia"""
    decoder = InteractiveDecoder()
    
    print("="*70)
    print(" " * 15 + "INTERACTIVE MANUSCRIPT DECODER")
    print(" " * 20 + "by Python Champion 🏆")
    print("="*70)
    
    # Przykładowy tekst
    sample_text = """
    ollag ceg gollad ollag e ceg ceeg gud og ogolg oegolsog
    oud eug keg geeg ceeg ceg cear og ollag gllad og
    eg sollog oleg sheg golkog ollag egg e eallo
    gollad ceg aceglo gog kano ceoleg ollag aceg
    """
    
    print("\n📖 Wczytuję przykładowy tekst...")
    decoder.load_encrypted_text(sample_text)
    
    print("\n🗺️  Wyświetlam bazowe mapowania...")
    decoder.show_mappings()
    
    print("\n🔓 Deszyfrowanie tekstu...")
    decoder.decrypt()
    
    print("\n📊 Statystyki...")
    decoder.statistics()
    
    print("\n" + "="*70)
    print("KOMENDY DOSTĘPNE:")
    print("="*70)
    print("decoder.add_mapping('zaszyfrowane', 'odszyfrowane')")
    print("decoder.decrypt()")
    print("decoder.show_mappings()")
    print("decoder.save_mapping('moja_mapa.json')")
    print("decoder.load_mapping('moja_mapa.json')")
    print("decoder.statistics()")
    print("="*70)
    
    return decoder


# INTERACTIVE MODE
if __name__ == "__main__":
    print("\n🚀 Uruchamiam Interactive Decoder...\n")
    decoder = demo()
    
    print("\n✨ Narzędzie gotowe do użycia!")
    print("💡 Użyj: decoder.add_mapping('nowe_slowo', 'tlumaczenie')")
    print("💡 Potem: decoder.decrypt() aby zobaczyć wynik\n")
    
    # Interaktywny tryb (opcjonalny)
    print("\n" + "="*70)
    print("PRZYKŁAD DODANIA NOWEGO MAPOWANIA:")
    print("="*70)
    decoder.add_mapping('gllad', 'et')
    decoder.add_mapping('sollog', 'sunt')
    decoder.decrypt()

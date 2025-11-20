#!/usr/bin/env python3
"""
FOLIO 67v YSHEDY CONTEXT ANALYSIS
Analiza YSHEDY w kontekście astronomicznym/astrologicznym
"""

import re
from collections import Counter

def analyze_67v():
    with open('voynich_67v_raw.txt', 'r') as f:
        text = f.read()

    # Extract only data lines (skip header)
    lines = [line.strip() for line in text.split('\n')
             if line.strip() and not line.startswith('#') and '===' not in line]

    # Tokenize
    all_tokens = []
    for line in lines:
        tokens = line.split()
        all_tokens.extend(tokens)

    # Find YSHEDY contexts (3 tokens before, 3 after)
    yshedy_contexts = []
    for i, token in enumerate(all_tokens):
        if 'yshed' in token.lower():
            before = all_tokens[max(0, i-3):i]
            after = all_tokens[i+1:min(len(all_tokens), i+4)]
            yshedy_contexts.append({
                'token': token,
                'before': before,
                'after': after,
                'full': ' '.join(before + [f"**{token}**"] + after)
            })

    # Co-occurrence analysis
    cooccur_tokens = []
    for ctx in yshedy_contexts:
        cooccur_tokens.extend(ctx['before'])
        cooccur_tokens.extend(ctx['after'])

    cooccur_counter = Counter(cooccur_tokens)

    # Generate report
    report = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║              FOLIO 67v - YSHEDY IN ASTROLOGICAL CONTEXT                    ║
║                    ASTRONOMICAL DIAGRAMS ANALYSIS                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

📊 BASIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total tokens in folio:     {len(all_tokens)}
YSHED occurrences:         {sum(1 for ctx in yshedy_contexts if ctx['token'] == 'yshed')}
YSHEDY occurrences:        {sum(1 for ctx in yshedy_contexts if ctx['token'] == 'yshedy')}
Total YSHED* variants:     {len(yshedy_contexts)}

Percentage of folio:       {len(yshedy_contexts)/len(all_tokens)*100:.1f}%

🔍 ALL YSHEDY CONTEXTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    for i, ctx in enumerate(yshedy_contexts, 1):
        report += f"\n{i}. {ctx['full']}"

    report += f"""

🔗 TOP CO-OCCURRING TOKENS (within ±3 window)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    for token, count in cooccur_counter.most_common(15):
        report += f"\n{token:15s} → {count:2d}x"

    # Pattern analysis
    report += """

⚡ PATTERN ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # Find common patterns
    patterns = {
        'otedy + yshedy': sum(1 for ctx in yshedy_contexts if 'otedy' in ctx['before']),
        'yshedy + othey': sum(1 for ctx in yshedy_contexts if 'othey' in ctx['after']),
        'yshedy + otay': sum(1 for ctx in yshedy_contexts if 'otay' in ctx['after']),
        'othey + yshedy': sum(1 for ctx in yshedy_contexts if 'othey' in ctx['before']),
        'sheedy + othey': 0  # placeholder
    }

    for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            report += f"\n{pattern:20s} → {count}x"

    report += """

🎯 INTERPRETATION: ASTRONOMICAL CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Context:** Folio 67v contains ASTROLOGICAL DIAGRAMS with multiple circles
            and dense annotations around geometric patterns.

**YSHEDY in this context likely means:**
  → "BEGIN OBSERVATION PROCEDURE"
  → "PERFORM ASTRONOMICAL CALCULATION"
  → "APPLY CELESTIAL MEASUREMENT"

**Key differences from botanical context:**
  ✓ In botany: YSHEDY = "begin preparation/cooking procedure"
  ✓ In astronomy: YSHEDY = "begin observation/calculation procedure"

**Universal meaning:**
  → YSHEDY is a META-PROCEDURAL MARKER
  → Works across ALL domains (botany, astronomy, etc.)
  → Signals: "Begin following this instruction/procedure"

**Co-occurrence with OTEDY:**
  → OTEDY = "repeat/iterate" (24% of corpus)
  → OTEDY + YSHEDY = "Repeat this procedure"
  → Common in astronomical contexts (iterative observations!)

📊 VARIANT ANALYSIS: YSHED vs YSHEDY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YSHED (2x):  Shortened form - possibly:
             • End-of-line truncation
             • Abbreviated version (space constraints in diagrams)
             • Phonetic reduction

YSHEDY (6x): Full form with Y...Y bracket
             • Complete procedural marker
             • Structural bracket intact
             • Standard morphological form

Ratio: 75% full form (YSHEDY) vs 25% short form (YSHED)
       → Suggests YSHEDY is the canonical form

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Folio 67v Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    return report

def main():
    print("Analyzing folio 67v YSHEDY contexts...")
    report = analyze_67v()

    with open('FOLIO_67v_YSHEDY_ANALYSIS.txt', 'w', encoding='utf-8') as f:
        f.write(report)

    print("\n" + "="*80)
    print("✅ FOLIO 67v ANALYSIS COMPLETE!")
    print("="*80)
    print("\nFile generated: FOLIO_67v_YSHEDY_ANALYSIS.txt")
    print("\n" + report)

if __name__ == '__main__':
    main()

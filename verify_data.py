#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para verificar consistência dos dados"""

import json

with open('dengue_advanced_statistics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("VERIFICACAO DE CONSISTENCIA DOS DADOS")
print("=" * 60)

total_geral = data['geral']['total_casos']
print(f"\nTotal de casos (geral): {total_geral:,}")

# Verificar faixas etárias
faixas = data.get('faixa_etaria', {})
total_faixas = sum(f['casos'] for f in faixas.values())
print(f"\nFaixas etarias:")
print(f"  Total nas faixas: {total_faixas:,}")
print(f"  Percentual: {total_faixas/total_geral*100:.2f}%")
print(f"  Diferenca: {total_geral - total_faixas:,} casos sem idade")

todas_faixas = ['0-4', '5-14', '15-29', '30-44', '45-59', '60+']
print(f"\n  Faixas presentes no JSON:")
for faixa in todas_faixas:
    if faixa in faixas:
        casos = faixas[faixa]['casos']
        perc = faixas[faixa]['percentual_do_total']
        print(f"    {faixa}: {casos:,} casos ({perc:.2f}%)")
    else:
        print(f"    {faixa}: AUSENTE!")

# Verificar sintomas por perfil
perfis = data.get('sintomas_por_perfil', {}).get('por_faixa_etaria', {})
print(f"\nSintomas por perfil:")
print(f"  Faixas presentes: {len(perfis)}")
for faixa in todas_faixas:
    if faixa in perfis:
        print(f"    {faixa}: presente")
    else:
        print(f"    {faixa}: AUSENTE!")

# Verificar gênero detalhado
gen = data.get('genero_detalhado', {}).get('distribuicao_por_faixa', {})
print(f"\nGenero detalhado (distribuicao_por_faixa):")
print(f"  Faixas presentes: {len(gen)}")
for faixa in todas_faixas:
    if faixa in gen:
        print(f"    {faixa}: presente")
    else:
        print(f"    {faixa}: AUSENTE!")

print("\n" + "=" * 60)
if len(perfis) == 6 and total_faixas > total_geral * 0.99:
    print("STATUS: DADOS CONSISTENTES! OK")
else:
    print("STATUS: ATENCAO - Verificar dados!")
print("=" * 60)


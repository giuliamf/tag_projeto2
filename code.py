import pandas as pd
import re

import networkx as nx
import matplotlib.pyplot as plt

with open('dados.txt', 'r', encoding='utf-8') as file:
  linhas = file.readlines()

linhas = [linha.strip() for linha in linhas if linha.strip()]

split_id = next(i for i, l in enumerate(linhas) if l.startswith('//alunos'))

projeto_linhas = linhas[2:split_id]
estudante_linhas = linhas[split_id+2:]

projetos = []
for linha in projeto_linhas:
  match = re.match(r'\((P\d+),\s*(\d+),\s*(\d+)\)', linha)
  if match:
    codigo, vagas, nota_min = match.groups()
    projetos.append({'projeto': codigo, 'vagas': int(vagas), 'nota_min': int(nota_min)})

df_projetos = pd.DataFrame(projetos)

alunos = []
for linha in estudante_linhas:
  match = re.match(r'\((A\d+)\):\((P\d+(?:,\s*P\d+){0,2})\)\s*\((\d+)\)', linha)
  if match:
    codigo, preferencias, nota = match.groups()
    prefs = [p.strip() for p in preferencias.split(',')]
    alunos.append({
        'aluno': codigo,
        'pref_1': prefs[0] if len(prefs) > 0 else None,
        'pref_2': prefs[1] if len(prefs) > 1 else None,
        'pref_3': prefs[2] if len(prefs) > 2 else None,
        'nota': int(nota)
        })

df_alunos = pd.DataFrame(alunos)

grafo = nx.Graph()

grafo.add_nodes_from(df_alunos['aluno'], bipartite=0)

requisitos = df_projetos.set_index('projeto').to_dict('index')

for _, row in df_projetos.iterrows():
  for i in range(row['vagas']):
    vaga = f'{row["projeto"]}-{i+1}'
    grafo.add_node(vaga, bipartite=1)

for _, aluno in df_alunos.iterrows():
  aluno_id = aluno['aluno']
  nota = aluno['nota']
  for pref in ['pref_1', 'pref_2', 'pref_3']:
    projeto = aluno[pref]
    if projeto in requisitos and nota >= requisitos[projeto]['nota_min']:
      for i in range(requisitos[projeto]['vagas']):
        vaga = f'{projeto}-{i+1}'
        grafo.add_edge(aluno_id, vaga)
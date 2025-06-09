import pandas as pd
import re
import networkx as nx
from visualizar_grafo import visualizar_grafo_bipartido

# Lê o arquivo de dados
with open('dados.txt', 'r', encoding='utf-8') as file:
  linhas = file.readlines()

# Remove linhas em branco e espaços extras
linhas = [linha.strip() for linha in linhas if linha.strip()]

# Encontra o índice onde começam os dados dos alunos
split_id = next(i for i, l in enumerate(linhas) if l.startswith('//alunos'))

# Separa as linhas dos projetos e dos alunos
projeto_linhas = linhas[2:split_id]
estudante_linhas = linhas[split_id+2:]

# Processa os projetos, extraindo código, vagas e nota mínima
projetos = []
for linha in projeto_linhas:
  match = re.match(r'\((P\d+),\s*(\d+),\s*(\d+)\)', linha)
  if match:
    codigo, vagas, nota_min = match.groups()
    projetos.append({'projeto': codigo, 'vagas': int(vagas), 'nota_min': int(nota_min)})

# Cria DataFrame com os projetos
df_projetos = pd.DataFrame(projetos)

# Processa os alunos, extraindo código, preferências e nota
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

# Cria DataFrame com os alunos
df_alunos = pd.DataFrame(alunos)

# Cria o grafo bipartido
grafo = nx.Graph()

# Adiciona nós dos alunos (um conjunto do bipartido)
grafo.add_nodes_from(df_alunos['aluno'], bipartite=0)

# Cria dicionário com requisitos dos projetos
requisitos = df_projetos.set_index('projeto').to_dict('index')

# Adiciona nós das vagas (outro conjunto do bipartido)
for _, row in df_projetos.iterrows():
  for i in range(row['vagas']):
    vaga = f'{row["projeto"]}-{i+1}'
    grafo.add_node(vaga, bipartite=1)

# Adiciona arestas entre alunos e vagas conforme preferências e requisitos
for _, aluno in df_alunos.iterrows():
  aluno_id = aluno['aluno']
  nota = aluno['nota']
  for pref in ['pref_1', 'pref_2', 'pref_3']:
    projeto = aluno[pref]
    if projeto in requisitos and nota >= requisitos[projeto]['nota_min']:
      for i in range(requisitos[projeto]['vagas']):
        vaga = f'{projeto}-{i+1}'
        grafo.add_edge(aluno_id, vaga)

# Calcula estatísticas do grafo
n_alunos = len([n for n, d in grafo.nodes(data=True) if d.get("bipartite") == 0])
n_vagas = len([n for n, d in grafo.nodes(data=True) if d.get("bipartite") == 1])
n_arestas = grafo.number_of_edges()

# Cria DataFrame com as estatísticas
df_stats = pd.DataFrame({
    "Tipo": ["Alunos", "Vagas", "Arestas"],
    "Quantidade": [n_alunos, n_vagas, n_arestas]
})

# Exibe as estatísticas e visualização do grafo
print(df_stats)
print(visualizar_grafo_bipartido(grafo, max_nos=20))
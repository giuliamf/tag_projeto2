# prompt: create and adaptation of the gale shapley algorithm

# Preparar os dados para o algoritmo Gale-Shapley
# Criar dicionários de preferências para alunos e vagas
preferencias_alunos = {}
for _, aluno in df_alunos.iterrows():
  preferencias_alunos[aluno['aluno']] = [
      f'{p}-{i+1}'
      for p in [aluno['pref_1'], aluno['pref_2'], aluno['pref_3']] if p is not None
      for i in range(requisitos.get(p, {}).get('vagas', 0))
      if p in requisitos and aluno['nota'] >= requisitos[p]['nota_min']
  ]

preferencias_vagas = {}
for _, projeto in df_projetos.iterrows():
  for i in range(projeto['vagas']):
    vaga = f'{projeto["projeto"]}-{i+1}'
    # Para as vagas, a preferência é baseada na nota do aluno (maior nota é melhor)
    # Vamos criar uma lista de alunos elegíveis para esta vaga, ordenados por nota descendente
    alunos_elegiveis = df_alunos[
        df_alunos[['pref_1', 'pref_2', 'pref_3']].apply(lambda row: projeto['projeto'] in row.values, axis=1) &
        (df_alunos['nota'] >= projeto['nota_min'])
    ].sort_values(by='nota', ascending=False)['aluno'].tolist()
    preferencias_vagas[vaga] = alunos_elegiveis

# Implementação do algoritmo Gale-Shapley (adaptação Aluno-Vaga)
# Alunos propõem para vagas

alunos_livres = list(preferencias_alunos.keys())
emparelhamento = {} # {vaga: aluno}
propostas_vagas = {vaga: [] for vaga in preferencias_vagas.keys()} # {vaga: [alunos que propuseram]}

while alunos_livres:
  aluno = alunos_livres.pop(0)
  aluno_prefs = preferencias_alunos.get(aluno, [])

  # Encontrar a primeira vaga na lista de preferências do aluno que ele ainda não propôs
  vaga_proposta = None
  for vaga in aluno_prefs:
      if aluno not in propostas_vagas[vaga]:
          vaga_proposta = vaga
          break

  if vaga_proposta is not None:
      propostas_vagas[vaga_proposta].append(aluno)

      # Se a vaga não estiver emparelhada
      if vaga_proposta not in emparelhamento:
          # A vaga aceita a proposta do aluno
          emparelhamento[vaga_proposta] = aluno
      else:
          aluno_atual = emparelhamento[vaga_proposta]
          # Verificar a preferência da vaga entre o aluno atual e o novo aluno
          preferencia_vaga_lista = preferencias_vagas.get(vaga_proposta, [])
          try:
            indice_aluno_atual = preferencia_vaga_lista.index(aluno_atual)
            indice_novo_aluno = preferencia_vaga_lista.index(aluno)

            if indice_novo_aluno < indice_aluno_atual:
              # O novo aluno é mais preferido pela vaga
              alunos_livres.append(aluno_atual) # O aluno atual volta a ser livre
              emparelhamento[vaga_proposta] = aluno # A vaga se emparelha com o novo aluno
            else:
              # O aluno atual é mais preferido ou igual. O novo aluno volta a ser livre.
              alunos_livres.append(aluno)
          except ValueError:
              # Um dos alunos não está na lista de preferências da vaga (não deveria acontecer se as arestas foram criadas corretamente)
              # Neste caso, mantemos o emparelhamento atual e o novo aluno volta a ser livre.
              alunos_livres.append(aluno)


# Imprimir o emparelhamento resultante
print("Emparelhamento:")
for vaga, aluno in emparelhamento.items():
  print(f"{aluno} está emparelhado com {vaga}")

# Opcional: Visualizar o grafo com o emparelhamento
# Criar um subgrafo com as arestas do emparelhamento
grafo_emparelhado = nx.Graph()
grafo_emparelhado.add_nodes_from(grafo.nodes(data=True))
for vaga, aluno in emparelhamento.items():
    grafo_emparelhado.add_edge(aluno, vaga, color='red', weight=2) # Adiciona arestas emparelhadas com destaque

# Adicionar as arestas não emparelhadas com outra cor
arestas_emparelhadas_tuplas = [(aluno, vaga) for vaga, aluno in emparelhamento.items()] + [(vaga, aluno) for vaga, aluno in emparelhamento.items()]

for u, v in grafo.edges():
  if (u, v) not in arestas_emparelhadas_tuplas:
     grafo_emparelhado.add_edge(u, v, color='skyblue', weight=1)


visualizar_grafo_bipartido(grafo_emparelhado, max_nos=20)

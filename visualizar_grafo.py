import matplotlib.pyplot as plt
import networkx as nx

def visualizar_grafo_bipartido(G, max_nos=40, edges_highlight=None):
    """
    Visualiza um grafo bipartido com destaque opcional para arestas emparelhadas.
    Filtra automaticamente as arestas para evitar erros com nós invisíveis.
    """
    # Identificar os dois conjuntos bipartidos
    alunos = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 0][:max_nos // 2]
    vagas = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 1][:max_nos // 2]
    visiveis = set(alunos + vagas)

    # Subgrafo visível
    subG = G.subgraph(visiveis)
    pos = nx.bipartite_layout(subG, alunos)

    # Nós
    nx.draw_networkx_nodes(subG, pos, node_color="lightgray", node_size=600)

    # Arestas padrão
    nx.draw_networkx_edges(subG, pos, edge_color="gray", alpha=0.4)

    # Arestas destacadas (emparelhamento atual)
    if edges_highlight:
        pares_filtrados = [e for e in edges_highlight if e[0] in visiveis and e[1] in visiveis]
        nx.draw_networkx_edges(subG, pos, edgelist=pares_filtrados, edge_color="green", width=2)

    # Rótulos
    nx.draw_networkx_labels(subG, pos, font_size=7)
    plt.title("Emparelhamento por Iteração")
    plt.axis("off")
    plt.show()

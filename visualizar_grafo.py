import matplotlib.pyplot as plt
import networkx as nx

def visualizar_grafo_bipartido(G, max_nos=40, edges_highlight=None):
    """
    Visualiza um grafo bipartido com destaque opcional para arestas emparelhadas.
    """
    alunos = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 0]
    vagas = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 1]

    # Cortar para visualização (debug)
    alunos = alunos[:max_nos // 2]
    vagas = vagas[:max_nos // 2]
    subG = G.subgraph(alunos + vagas)

    pos = nx.bipartite_layout(subG, alunos)

    # Nós
    nx.draw_networkx_nodes(subG, pos, node_color="lightgray", node_size=600)

    # Arestas destacadas (emparelhadas)
    if edges_highlight is None:
        edges_highlight = []
    nx.draw_networkx_edges(subG, pos, edgelist=subG.edges(), edge_color="gray", alpha=0.4)
    nx.draw_networkx_edges(subG, pos, edgelist=edges_highlight, edge_color="green", width=2)

    # Rótulos
    nx.draw_networkx_labels(subG, pos, font_size=7)
    plt.title("Emparelhamento por Iteração")
    plt.axis("off")
    plt.show()

import networkx as nx
import matplotlib.pyplot as plt

def visualizar_grafo_bipartido(G, max_nos=40):
    """
    Exibe uma visualização simples do grafo bipartido com até `max_nos` nós.
    """
    alunos = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 0]
    vagas = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 1]

    # Limita o número de nós para evitar poluição
    alunos = alunos[:max_nos // 2]
    vagas = vagas[:max_nos // 2]

    subgrafo = G.subgraph(alunos + vagas)
    pos = nx.bipartite_layout(subgrafo, alunos)

    nx.draw(
        subgrafo, pos,
        with_labels=True,
        node_size=600,
        node_color=["skyblue" if n in alunos else "lightgreen" for n in subgrafo.nodes()],
        font_size=7,
        edge_color="gray"
    )
    plt.title("Visualização do Grafo Bipartido (parcial)")
    plt.axis("off")
    plt.show()

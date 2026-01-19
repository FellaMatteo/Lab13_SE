from itertools import combinations

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.best_path = []
        self.best_score = 0

    def create_graph(self):
        # 1. Recupero i geni
        geni = DAO.get_geni()

        # Mappa fondamentale: GeneID -> Cromosoma
        # Ci serve per sapere, dato un gene dell'interazione, a che nodo (cromosoma) appartiene
        gene_map = {}

        # Aggiungo i NODI (Cromosomi)
        for gene in geni:
            if gene.cromosoma != 0:
                self.G.add_node(gene.cromosoma)
                # Popolo la mappa
                gene_map[gene.id] = gene.cromosoma


        interazioni = DAO.get_correlazione()


        edges_weights = {}

        for g1, g2, corrispondenza in interazioni:
            # Recupero i cromosomi corrispondenti ai geni
            if g1 in gene_map and g2 in gene_map:
                c1 = gene_map[g1]
                c2 = gene_map[g2]

                # Controllo che siano diversi (già fatto in SQL, ma per sicurezza)
                if c1 != c2:
                    # Chiave dell'arco orientato: da c1 a c2
                    arco = (c1, c2)

                    # Sommo la correlazione al peso totale di questo arco cromosomico
                    if arco not in edges_weights:
                        edges_weights[arco] = float(corrispondenza)
                    else:
                        edges_weights[arco] += float(corrispondenza)

        # 3. Aggiungo gli ARCHI al grafo finale
        for (c1, c2), peso_totale in edges_weights.items():
            self.G.add_edge(c1, c2, weight=peso_totale)

        print(f"Grafo creato! Vertici: {len(self.G.nodes)}, Archi: {len(self.G.edges)}")


    def get_grapgh_details(self):
        n_vertici = len(self.G.nodes)
        n_archi = len(self.G.edges)

        return n_vertici, n_archi

    def conta_archi(self, valore_soglia):
        lista_archi_maggiori_soglia = []
        lista_minori_di_soglia = []

        for u, v, data in self.G.edges(data=True):
            peso = data["weight"]

            if peso > valore_soglia:
                lista_archi_maggiori_soglia.append((u, v))
            else:
                lista_minori_di_soglia.append((u, v))

        return lista_archi_maggiori_soglia, lista_minori_di_soglia


    def get_best_path(self):
        self.best_path = []
        self.best_score = 0

        for nodo in self.G.nodes:
            parziale = [nodo]
            self.ricorsione(parziale)
            print("Ricorsione iniziata")

        print("Ricorsione riuscita")

        return self.best_path

    def ricorsione(self, parziale):
        # 1. Ho fatto meglio di prima?
        if self._get_score(parziale) > self.best_score:
            self.best_score = self._get_score(parziale)
            self.best_path = list(parziale)

        # 2. quali vicini posso esplorare?
        ultimo = parziale[-1]
        vicini = self.G.neighbors(ultimo)

        for v in vicini:
            if v not in parziale:
                if len(parziale) > 1:
                    penultimo = parziale[-2]
                    if self.G[ultimo][v]["weight"] > self.G[penultimo][ultimo]["weight"]:
                        parziale.append(v)

                        self.ricorsione(parziale)

                        parziale.pop()

                else:
                    parziale.append(v)

                    self.ricorsione(parziale)

                    parziale.pop()


    def _get_score(self, parziale):
        score = 0
        for i in range(1, len(parziale)):
            score += self.G[parziale[i - 1]][parziale[i]]["weight"]
        return score
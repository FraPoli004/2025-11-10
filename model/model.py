import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodi = None
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        return DAO.getAllStores()

    def getNodes(self,s):
        return DAO.getAllNodes(s)

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    def buildGraph(self, k,s):
        self._grafo.clear()
        self._idMap = {}
        self._nodi = DAO.getAllNodes(s)
        for n in self._nodi:
            self._grafo.add_node(n)
            self._idMap[n.order_id] = n
        self.addEdges(k,s)


    def addEdges(self, k,s):
        edges = DAO.getAllEdges(k,s)
        for e in edges:
            n1 = self._idMap.get(e[0])
            n2 = self._idMap.get(e[1])
            if n1 is None or n2 is None:
                continue
            if e[3] < 0:
                self._grafo.add_edge(n2, n1,weight=e[2]/abs(e[3]))
            else:
                self._grafo.add_edge(n1, n2, weight=e[2] / abs(e[3]))

    def get_top5_archi(self):
        archi = []
        for u, v, data in self._grafo.edges(data=True):
            archi.append((u, v, data["weight"]))
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

    def getCamminoMassimo(self, source):
        source = self._idMap.get(int(source))
        self._cammino_ottimo = []
        self._ricorsione([source])
        return self._cammino_ottimo

    def _ricorsione(self, parziale):
        # se il parziale è più lungo del migliore trovato finora, aggiorno
        if len(parziale) > len(self._cammino_ottimo):
            self._cammino_ottimo = list(parziale)  # copia!

        ultimo = parziale[-1]
        for n in self._grafo.successors(ultimo):  # solo archi uscenti
            if n not in parziale:  # no nodi ripetuti
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()  # backtracking



import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodi = None
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        return DAO.getAllStores()

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



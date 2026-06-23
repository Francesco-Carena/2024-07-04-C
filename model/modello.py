import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapNodes={}

        self._bestPath=[]
        self._bestPunteggio=0

    def getAllYears(self):
        return DAO.getAllYears()

    def getShapes(self, year):
        return DAO.getShapes(year)

    def createGraph(self, anno, forma):
        self._graph.clear()
        self._idMapNodes = {}

        nodes = DAO.getSightings(anno, forma)
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMapNodes[node.id] = node

        self._addEdges()

    def _addEdges(self):
        nodes=list(self._graph.nodes())
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                u=nodes[i]
                v=nodes[j]
                if v.state==u.state:
                    if u.longitude<v.longitude:
                        peso=v.longitude-u.longitude
                        self._graph.add_edge(u,v,weight=peso)
                    elif u.longitude>v.longitude:
                        peso=u.longitude-v.longitude
                        self._graph.add_edge(v,u,weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
    def getBestEdges(self):
        edges=list(self._graph.edges(data=True))
        edges.sort(key=lambda x: x[2]['weight'], reverse=True)
        return edges[:5]

    def searchPath(self):
        self._bestPath=[]
        self._bestPunteggio=0
        parziale=[]
        punteggio=100

        for node in self._graph.nodes():
            parziale.append(node)
            self._ricorsione(parziale,punteggio)
            parziale.pop()

        return self._bestPath, self._bestPunteggio

    def _ricorsione(self,parziale,punteggio):
        if punteggio>self._bestPunteggio:
            self._bestPunteggio=punteggio
            self._bestPath=copy.deepcopy(parziale)

        for node in self._graph.neighbors(parziale[-1]):
            if node.duration>parziale[-1].duration:
                conteggio_mese = sum(1 for n in parziale if n.datetime.month == node.datetime.month)
                if conteggio_mese<3:
                    new=punteggio+100
                    if parziale[-1].datetime.month==node.datetime.month:
                        new=punteggio+200
                    parziale.append(node)
                    self._ricorsione(parziale,new)
                    parziale.pop()
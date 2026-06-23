import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillddyear(self):
        anni=self._model.getAllYears()
        for year in anni:
            self._view.ddyear.options.append(ft.dropdown.Option(year))

    def fillddshape(self,e):
        self._view.ddshape.options.clear()
        forme=self._model.getShapes(int(self._view.ddyear.value))
        for shape in forme:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()


    def handle_graph(self, e):
        anno=self._view.ddyear.value
        if anno is None:
            self._view.create_alert("Selezionare prima un anno")
            self._view.update_page()
            return

        shape = self._view.ddshape.value
        if shape is None:
            self._view.create_alert("Selezionare prima una forma")
            self._view.update_page()
            return

        self._model.createGraph(anno, shape)
        nnodi, narchi = self._model.getGraphDetails()
        edges=self._model.getBestEdges()
        self._view.txt_result1.clean()
        self._view.txt_result1.controls.append(ft.Text("Grafo creato correttamente!"))
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha {nnodi} nodi e {narchi} archi"))
        self._view.txt_result1.controls.append(
            ft.Text(f"I 5 archi dal peso maggiore:"))
        for edge in edges:
            self._view.txt_result1.controls.append(ft.Text(f"{edge[0].id} - {edge[1].id}, {edge[2]['weight']}"))
        self._view.update_page()


    def handle_path(self, e):
        if self._model._graph is None:
            self._view.create_alert("Creare prima il grafo")
            self._view.update_page()
            return

        path, punteggio=self._model.searchPath()

        self._view.txt_result2.clean()
        self._view.txt_result2.controls.append(ft.Text("Percorso migliore trovato!"))
        self._view.txt_result2.controls.append(ft.Text(f"Il percorso ha {len(path)} nodi e {punteggio} punteggio"))
        for node in path:
            self._view.txt_result2.controls.append(ft.Text(f"{node.id} "))
        self._view.update_page()

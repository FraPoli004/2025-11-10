import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStore(self):
        stores = (self._model.getStores())
        for s in stores:
            self._view._ddStore.options.append(
                ft.dropdown.Option(key=s.store_id, text=s.store_name)
            )
        self._view.update_page()

    def fillDDNode(self):
        s = self._view._ddStore.value
        nodes = (self._model.getNodes(s))
        for n in nodes:
            self._view._ddNode.options.append(
                ft.dropdown.Option(key=n.order_id, text=n.order_id)
            )
        self._view.update_page()


    def handleCreaGrafo(self, e):
        k = self._view._txtIntK.value
        s = self._view._ddStore.value
        self._view.txt_result.controls.clear()

        if k is None or k=="":
            self._view.txt_result.controls.append(
                ft.Text("inserire un numero intero maggiore di zero", color="red"))
            self._view.update_page()
            return

        k = int(k)

        if k < 0:
            self._view.txt_result.controls.append(
                ft.Text("inserire intero maggiore di zero", color="red"))
            self._view.update_page()
            return

        if s is None:
            self._view.txt_result.controls.append(
                ft.Text("inserire uno degli store", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(k,s)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("grafo creato correttamente", color="green"))
        self._view.txt_result.controls.append(ft.Text(f'il grafo ha {self._model.get_numnodi()} nodi'))
        self._view.txt_result.controls.append(ft.Text(f'il grafo ha {self._model.get_numarchi()} archi'))

        self._view.txt_result.controls.append(ft.Text(f'i 5 archi di peso maggiore sono:'))
        for a in self._model.get_top5_archi():
            self._view.txt_result.controls.append(ft.Text(f'{a[0]}---->{a[1]}, peso: {a[2]}'))

        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        self._view._ddNode.disabled = False
        self.fillDDNode()

        self._view.update_page()




    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        source = self._view._ddNode.value
        cammino = self._model.getCamminoMassimo(source)
        self._view.txt_result.controls.append(ft.Text(f'il cammino massimo partendo dal nodo {source} è composto dai seguenti nodi:'))
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f'{n}'))
        self._view.update_page()

    def handleRicorsione(self, e):
        pass
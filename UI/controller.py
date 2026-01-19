import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """""
        self._model.create_graph()

        n_vertici, n_archi = self._model.get_grapgh_details()

        self._view.lista_visualizzazione_1.controls.clear()

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di nodi: {n_vertici}, Numero di archi: {n_archi}"))

        self._view.update()

    def handle_conta_edges(self, e):
        """ Handler per gestire il conteggio degli archi """""
        valore_soglia = int(self._view.txt_name.value)
        if valore_soglia <= 3 or valore_soglia >= 7:
            valore_soglia = 0
            self._view.lista_visualizzazione_2.controls.clear()
            self._view.lista_visualizzazione_2.controls.append(ft.Text("Errore: inserire un valore compreso tra 3 e 7."))
            self._view.update()

        else:
            print("Valore soglia salvato correttamente")
            #conta archi
            lista_maggiori_di_soglia, lista_minori_di_soglia = self._model.conta_archi(valore_soglia)

            self._view.lista_visualizzazione_2.controls.clear()
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Numero di archi con peso maggiore della soglia: {len(lista_maggiori_di_soglia)} - Numero di archi con peso minore della soglia {len(lista_minori_di_soglia)}"))

            self._view.update()


    def handle_ricerca(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """""
        best_path = self._model.get_best_path()

        self._view.lista_visualizzazione_3.controls.clear()

        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Numero archi del percorso più lungo: {len(best_path)}"))
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Peso cammino massimo: "))
        for n in best_path:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(n))

        self._view.update()
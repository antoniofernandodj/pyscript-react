from datetime import datetime

from js import window, document, localStorage, PointerEvent, location, Element
from pyodide.ffi import create_proxy

from elements import *
from state import State
from logger import Logger
from component import Component
from routing import Router



class Home(Component):
    def render(self):
        return div(
            h1("Página Inicial"),
            route_link("Ir para Sobre", href="/sobre")
        )


class NotFound(Component):
    def render(self):
        return div(
            "Página não encontrada.",
            route_link("Ir para Sobre", href="/sobre"),
            route_link("Voltar para Home", href="/")
        )


class Sobre(Component):
    def render(self):
        return div(
            h1("Sobre Nós"),
            route_link("Voltar para Home", href="/")
        )


if __name__ == "__main__":
    root = document.getElementById("app")
    if not root:
        raise RuntimeError('Node not found!')

    router = Router()
    router.add_route("/", Home)
    router.add_route("/sobre", Sobre)
    router.set_not_found(NotFound)
    router.exec(root)

    # app.apply_styles({
    #     "backgroundColor": "darkred",
    #     "color": "white",
    #     "padding": "12px",
    #     "borderRadius": "5px",
    #     "fontWeight": "bold",
    # })

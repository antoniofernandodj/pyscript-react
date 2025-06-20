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

    router = Router(
        routes=[
            {"path": "/", "component": Home},
            {"path": "/sobre", "component": Sobre}
        ],
        not_found=NotFound
    )

    router.exec(root)

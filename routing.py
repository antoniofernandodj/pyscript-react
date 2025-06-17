from datetime import datetime
from logging import root

from js import window, document, localStorage, PointerEvent, location, Element  # type: ignore
from pyodide.ffi import create_proxy  # type: ignore

from elements import *
from state import *
from logger import *
from component import *
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from js import JSObject


class NotFound(Component):
    def render(self):
        return div(
            "Página não encontrada.",
            a("Ir para Sobre", href="#/sobre"),
            a("Voltar para Home", href="#/")
        )


class Router:

    def __init__(self):
        self.routes = {}  # ex: {'/home': HomeComponent}
        self.not_found = NotFound
        self.outlet = div()
        self._on_pop_state = create_proxy(self._on_path_change)
        self._on_link_click = create_proxy(self._handle_link_click)

        window.addEventListener("popstate", self._on_pop_state)
        document.addEventListener("click", self._on_link_click)

        self._on_path_change()

    def set_not_found(self, component):
        if not issubclass(component, Component):
            raise ValueError("O componente deve ser uma subclasse de Component.")
        self.not_found = component

    def add_route(self, path, component):
        self.routes[path] = component

    def exec(self, root: 'JSObject'):
        root.innerHTML = ""
        root.appendChild(self.outlet)
        self._on_path_change()

    def __call__(self):
        return self.outlet

    def _handle_link_click(self, event: PointerEvent):
        """
        Intercepta cliques em links com className 'route-link' e usa pushState.
        """
        target = event.target
        while target and not (hasattr(target, "tagName") and target.tagName == "ROUTE-LINK"):
            target = target.parentElement

        if not target:
            return

        href = target.getAttribute("href")
        event.preventDefault()
        window.history.pushState(None, "", href)
        self._on_path_change()

    def _on_path_change(self, *args):
        path = window.location.pathname or "/"
        comp = self.routes.get(path, self.not_found)
        self.outlet.innerHTML = ""
        instance = comp() if callable(comp) else comp
        self.outlet.appendChild(instance.container)  # type: ignore

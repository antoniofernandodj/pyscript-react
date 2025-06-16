from datetime import datetime

from js import window, document, localStorage, PointerEvent, location, Element  # type: ignore
from pyodide.ffi import create_proxy  # type: ignore

from elements import *
from state import *
from logger import *
from component import *


class Router:

    class NotFound(Component):
        def render(self):
            return div(
                "Página não encontrada.",
                a("Ir para Sobre", href="#/sobre"),
                a("Voltar para Home", href="#/")
            )

    def __init__(self):
        self.routes = {}  # ex: {'/home': HomeComponent}
        self.not_found = NotFound
        self.outlet = div()  # onde os componentes serão montados
        self._listener = create_proxy(self._on_hash_change)
        window.addEventListener("hashchange", self._listener)
        self._on_hash_change()
    
    def set_not_found(self, component):
        """
        Define o componente a ser renderizado quando uma rota não for encontrada.
        """
        if not issubclass(component, Component):
            raise ValueError("O componente deve ser uma subclasse de Component.")
        self.not_found = component

    def add_route(self, path, component):
        self.routes[path] = component
    
    def exec(self, root):
        """
        Executa o roteador, montando o componente de saída no elemento root.
        """
        if not isinstance(root, Element):
            raise ValueError("O root deve ser um elemento do DOM.")
        root.appendChild(self.outlet)
        self._on_hash_change()

    def __call__(self):
        """
        Retorna o elemento de saída onde os componentes serão renderizados.
        """
        return self.outlet

    def _on_hash_change(self, *args):
        path = window.location.hash[1:] or "/"
        comp = self.routes.get(path, self.not_found)
        self.outlet.innerHTML = ""
        instance = comp() if callable(comp) else comp
        self.outlet.appendChild(instance.container)



# class Clock(Component):
#     def init(self):

#         self.state, self.set_state = use_state(
#             self, datetime.now().strftime("%H:%M:%S")
#         )

#         def update_time():
#             self.set_state(lambda _: datetime.now().strftime("%H:%M:%S"))

#         def effect():
#             interval_id = set_interval(update_time, 1000)

#             def cleanup():
#                 clear_interval(interval_id)

#             return cleanup

#         self.use_effect(effect, lambda: [self.state.value])

#     def render(self):
#         return div(
#             h2("🕒 Relógio ao Vivo"),
#             p(f"{self.state}")
#         )


# class Timer(Component):
#     shared_time = create_shared_state(0)

#     def init(self):
#         self.logger = Logger()
#         self.time = Timer.shared_time
#         self.time.subscribe_component(self)

#         self.interval_id = None
#         self.running = False

#     def start(self, _: PointerEvent):
#         if not self.running:
#             self.logger.log("Temporizador iniciado.")
#             self.running = True

#             def tick():
#                 self.time.set_value(self.time.value + 1)
#                 localStorage.setItem("time", f"{self.time.value}")


#             self.interval_id = set_interval(tick, 1000)

#     def stop(self, _):
#         if self.running:
#             token = localStorage.getItem("time")
#             self.logger.warn(f"Temporizador pausado em {token}.")
#             if self.interval_id:
#                 clear_interval(self.interval_id)
#             self.running = False

#     def reset(self, e):
#         self.logger.info("Temporizador zerado.")
#         localStorage.removeItem("time")
#         self.time.set_value(0)

#     def render(self):
#         return div(
#             h2("⏱ Temporizador"),
#             p(f"{self.time.value} segundos"),
#             button("Start", on_click=self.start),
#             button("Stop", on_click=self.stop),
#             button("Reset", on_click=self.reset),
#             self.logger()
#         )


# class App(Component):
#     def init(self):
#         self.clock = Clock()
#         self.timer = Timer()

#         def effect():
#             import os
#             print(os.listdir())
#             print({'location': location.pathname})

#             with open("meuarquivo.txt", "w") as f:
#                 f.write('teste')

#             with open("meuarquivo.txt", "r") as f:
#                 content = f.read()

#             print(os.listdir())

#             print({'content': content})


#         self.use_effect(
#             effect,
#             lambda: []
#         )

#     def render(self):
#         return div(
#             h1("⏰ Aplicativo de Tempo com PyScript"),
#             self.clock(),
#             hr(),
#             self.timer()
#         )







class NotFound(Component):
    def render(self):
        return div(
            "Página não encontrada.",
            a("Ir para Sobre", href="#/sobre"),
            a("Voltar para Home", href="#/")
        )


class Home(Component):
    def render(self):
        return div(
            h1("Página Inicial"),
            a("Ir para Sobre", href="#/sobre")
        )

class Sobre(Component):
    def render(self):
        return div(
            h1("Sobre Nós"),
            a("Voltar para Home", href="#/")
        )



if __name__ == "__main__":
    root = document.getElementById("app")
    if not root:
        raise RuntimeError('Node not found!')

    root.innerHTML = ""
    router = Router()
    router.add_route("/", Home)
    router.add_route("/sobre", Sobre)

    # app.apply_styles({
    #     "backgroundColor": "darkred",
    #     "color": "white",
    #     "padding": "12px",
    #     "borderRadius": "5px",
    #     "fontWeight": "bold",
    # })

    root.appendChild(router())

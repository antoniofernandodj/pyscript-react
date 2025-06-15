from js import document

from elements import *
from state import *
from logger import *
from component import *



class Contador(Component):
    def init(self):
        self.state, self.set_state = use_state(self, 0)

    def render(self):
        return div(
            button("+", on_click=lambda _: self.set_state(lambda v: v + 1)),
            p(f"Valor atual: {self.state}")
        )


class SharedCounter(Component):
    shared_state = create_shared_state(0)

    def init(self):
        self.state = SharedCounter.shared_state

        self.state.subscribe_component(self)

    def render(self):
        return div(
            button("+", on_click=lambda _: self.state.set_value(self.state.value + 1)),
            p(f"Valor compartilhado: {self.state}")
        )


class Contador2(Component):
    def init(self):
        self.state = SharedCounter.shared_state
        self.state.subscribe_component(self)

    def render(self):
        return div(
            button("+", on_click=lambda _: self.state.set_value(self.state.value + 1)),
            p(f"Valor atual: {self.state}")
        )
        


class App(Component):
    def init(self):
        self.state, self.set_state = use_state(self, 0)
        self.contador = Contador()
        self.shared_counter = SharedCounter()
        self.contador2 = Contador2()
        self.logger = Logger()

        def effect():
            self.logger.info("Iniciando aplicação")

            self.logger.warn("Esse é um aviso")
            self.logger.error("Erro simulado")
            self.logger.debug("Estado atual: " + str(self.state.value))

            self.logger.log(f"Estado do app mudou para {self.state.value}")
            # cleanup function opcional
            def cleanup():
                self.logger.log("Cleanup do efeito App")
            return cleanup

        self.use_effect(
            effect,
            lambda: [self.state.value]
        )

    def render(self):

        def f(e):
            return self.set_state(lambda v: v + 1)

        return div(
            h1("Contador com PyScript e efeitos"),
            button("+", on_click=f),
            p(f"Valor atual: {self.state}"),
            h2("Componentes:"),
            self.contador(),
            h2("Contador Compartilhado:"),
            self.shared_counter(),
            h2("Componente com contador compartilhado:"),
            self.contador2(),
            self.logger()
        )


if __name__ == "__main__":
    root = document.getElementById("app")
    if not root:
        raise RuntimeError('Node not found!')

    root.innerHTML = ""
    app = App()
    root.appendChild(app())
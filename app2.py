from datetime import datetime

from js import document, localStorage, PointerEvent, location

from elements import *
from state import *
from logger import *
from component import *



class Clock(Component):
    def init(self):

        self.state, self.set_state = use_state(
            self, datetime.now().strftime("%H:%M:%S")
        )

        def update_time():
            self.set_state(lambda _: datetime.now().strftime("%H:%M:%S"))

        def effect():
            interval_id = set_interval(update_time, 1000)

            def cleanup():
                clear_interval(interval_id)

            return cleanup

        self.use_effect(effect, lambda: [self.state.value])

    def render(self):
        return div(
            h2("🕒 Relógio ao Vivo"),
            p(f"{self.state}")
        )


class Timer(Component):
    shared_time = create_shared_state(0)

    def init(self):
        self.logger = Logger()
        self.time = Timer.shared_time
        self.time.subscribe_component(self)

        self.interval_id = None
        self.running = False

    def start(self, _: PointerEvent):
        if not self.running:
            self.logger.log("Temporizador iniciado.")
            self.running = True

            def tick():
                self.time.set_value(self.time.value + 1)
                localStorage.setItem("time", f"{self.time.value}")


            self.interval_id = set_interval(tick, 1000)

    def stop(self, _):
        if self.running:
            token = localStorage.getItem("time")
            self.logger.warn(f"Temporizador pausado em {token}.")
            if self.interval_id:
                clear_interval(self.interval_id)
            self.running = False

    def reset(self, e):
        self.logger.info("Temporizador zerado.")
        localStorage.removeItem("time")
        self.time.set_value(0)

    def render(self):
        return div(
            h2("⏱ Temporizador"),
            p(f"{self.time.value} segundos"),
            button("Start", on_click=self.start),
            button("Stop", on_click=self.stop),
            button("Reset", on_click=self.reset),
            self.logger()
        )


class App(Component):
    def init(self):
        self.clock = Clock()
        self.timer = Timer()

        def effect():
            import os
            print(os.listdir())
            print({'location': location.pathname})

            with open("meuarquivo.txt", "w") as f:
                f.write('teste')

            with open("meuarquivo.txt", "r") as f:
                content = f.read()

            print(os.listdir())
            
            print({'content': content})


        self.use_effect(
            effect,
            lambda: []
        )

    def render(self):
        return div(
            h1("⏰ Aplicativo de Tempo com PyScript"),
            self.clock(),
            hr(),
            self.timer()
        )


if __name__ == "__main__":
    root = document.getElementById("app")
    if not root:
        raise RuntimeError('Node not found!')

    root.innerHTML = ""
    app = App()

    app.apply_styles({
        "backgroundColor": "darkred",
        "color": "white",
        "padding": "12px",
        "borderRadius": "5px",
        "fontWeight": "bold",
    })

    root.appendChild(app())

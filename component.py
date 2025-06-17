from typing import Self
from js import document # type: ignore


class Component:
    def __init__(self):
        self.container = document.createElement("div")
        self.effects = []
        self.init()
        self._render()

    def run(self, root):
        if not root:
            raise RuntimeError('Node not found!')

        root.innerHTML = ""

        root.appendChild(self())


    def init(self):
        pass

    def _render(self):
        self.cleanup_effects()
        self.container.innerHTML = ""
        self.container.appendChild(self.render())
        self.run_effects()

    def render(self):
        raise NotImplementedError()

    def __call__(self):
        return self.container

    def use_effect(self, effect_fn, dependencies_fn=None):
        """
        Registra um efeito. 
        dependencies: lista de valores que, se mudarem, executam o efeito novamente.
        """
        self.effects.append({
            "effect_fn": effect_fn,
            "dependencies_fn": dependencies_fn,
            "last_deps": None,
            "cleanup": None,
        })

    def cleanup_effects(self):
        for effect in self.effects:
            if effect["cleanup"]:
                effect["cleanup"]()
                effect["cleanup"] = None

    def run_effects(self):
        for effect in self.effects:
            deps = effect["dependencies_fn"]() if effect["dependencies_fn"] else None
            last_deps = effect["last_deps"]
            should_run = False

            if last_deps is None:
                should_run = True
            elif deps is not None:
                if len(deps) != len(last_deps):
                    should_run = True
                else:
                    for old, new in zip(last_deps, deps):
                        if old != new:
                            should_run = True
                            break

            if should_run:
                if effect["cleanup"]:
                    effect["cleanup"]()
                    effect["cleanup"] = None

                cleanup_fn = effect["effect_fn"]()
                if callable(cleanup_fn):
                    effect["cleanup"] = cleanup_fn

                effect["last_deps"] = list(deps) if deps else None


    def apply_styles(self: Self, estilos: dict):
        elemento = self()
        for chave, valor in estilos.items():
            setattr(elemento.style, chave, valor)
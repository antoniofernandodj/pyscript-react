from copy import deepcopy
from typing import Generic, TypeVar


T = TypeVar('T')



class State(Generic[T]):

    value: T
    def __init__(self, initial_value: T):
        self.subscribers = []
        self.value = initial_value

    def get_value(self):
        return deepcopy(self.value)

    def subscribe(self, fn):
        self.subscribers.append(fn)
    
    def subscribe_component(self, component):
        self.subscribe(component._render)

    def unsubscribe(self, fn):
        if fn in self.subscribers:
            self.subscribers.remove(fn)

    def notify(self):
        for fn in self.subscribers:
            fn()

    def set_value(self, new_value: T):
        self.value = new_value
        self.notify()

    def __str__(self):
        return str(self.value)



def create_shared_state(initial_value):
    # Cria um estado global compartilhado
    return State(initial_value)



def use_state(parent, initial_value):
    """
    Se parent for None, cria estado isolado (ex: para lógica não ligada a componente)
    Se parent for componente, associa re-render automático.
    """
    state = State(initial_value)

    def set_state(fn_or_value):
        # Pode receber função (fn) ou valor direto (ex: set_state(5))
        if callable(fn_or_value):
            state.value = fn_or_value(state.value)
        else:
            state.value = fn_or_value
        state.notify()


    state.subscribe(parent._render)
    
    return state, set_state


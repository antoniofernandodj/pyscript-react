from typing import Self
from js import document # type: ignore



class VNode:
    __slots__ = ('tag', 'props', 'children', 'key', 'element')
    
    def __init__(self, tag, props=None, children=None, key=None):
        self.tag = tag
        self.props = props or {}
        self.children = children or []
        self.key = key  # Para identificação única de elementos
        self.element = None  # Referência ao elemento DOM real


class Component:
    def __init__(self):
        self.container = document.createElement("div")
        self.effects = []
        self._render()
        self.vdom = None  # Representação virtual do DOM
        self.init()

    def run(self, root):
        if not root:
            raise RuntimeError('Node not found!')

        root.innerHTML = ""

        root.appendChild(self())

    def init(self):
        pass

    def _render(self):
        self.cleanup_effects()
        new_vdom = self.render()
        
        # Primeira renderização
        if self.vdom is None:
            element = self.create_dom(new_vdom)
            self.container.innerHTML = ""
            self.container.appendChild(element)
            self.vdom = new_vdom
        else:
            self.update_dom(self.container, self.vdom, new_vdom)
            self.vdom = new_vdom
        
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

    def create_dom(self, vnode):
        """Cria o DOM real a partir de um VNode"""
        if isinstance(vnode, str):
            return document.createTextNode(vnode)
        
        element = document.createElement(vnode.tag)
        vnode.element = element
        
        # Aplica propriedades
        for attr, value in vnode.props.items():
            if attr.startswith('on_'):
                event = attr[3:]
                element.addEventListener(event, value)
            else:
                element.setAttribute(attr, value)
        
        # Cria filhos
        for child in vnode.children:
            child_element = self.create_dom(child)
            element.appendChild(child_element)
        
        return element

    def update_dom(self, parent, old_vnode, new_vnode):
        """Atualiza o DOM real comparando VNodes antigo e novo"""
        # Caso 1: Nós são diferentes (tags diferentes ou texto vs elemento)
        if type(old_vnode) != type(new_vnode) or old_vnode.tag != new_vnode.tag:
            new_element = self.create_dom(new_vnode)
            parent.replaceChild(new_element, old_vnode.element)
            return
        
        # Caso 2: Ambos são nós de texto
        if isinstance(new_vnode, str):
            if old_vnode != new_vnode:
                parent.replaceChild(
                    document.createTextNode(new_vnode),
                    old_vnode.element
                )
            return
        
        element = old_vnode.element
        new_vnode.element = element
        
        # Caso 3: Mesma tag, atualiza propriedades
        self.update_props(element, old_vnode.props, new_vnode.props)
        
        # Caso 4: Atualiza filhos
        self.update_children(element, old_vnode.children, new_vnode.children)

    def update_props(self, element, old_props, new_props):
        """Atualiza propriedades do elemento"""
        # Remove propriedades antigas que não existem mais
        for attr in old_props:
            if attr not in new_props:
                if attr.startswith('on_'):
                    event = attr[3:]
                    element.removeEventListener(event, old_props[attr])
                else:
                    element.removeAttribute(attr)
        
        # Adiciona/atualiza novas propriedades
        for attr, value in new_props.items():
            if attr not in old_props or old_props[attr] != value:
                if attr.startswith('on_'):
                    event = attr[3:]
                    # Remove listener antigo se existir
                    if attr in old_props:
                        element.removeEventListener(event, old_props[attr])
                    element.addEventListener(event, value)
                else:
                    element.setAttribute(attr, value)

    def update_children(self, parent, old_children, new_children):
        """Reconciliação eficiente de filhos usando algoritmo de diffing"""
        # Índices para percorrer as listas
        old_index = 0
        new_index = 0
        
        # Lista de operações pendentes
        changes = []
        
        # Mapa de chaves para nós antigos
        key_map = {}
        for i, child in enumerate(old_children):
            if isinstance(child, VNode) and child.key:
                key_map[child.key] = (child, i)
        
        # Primeira passada: identificar operações
        while new_index < len(new_children) and old_index < len(old_children):
            old_child = old_children[old_index]
            new_child = new_children[new_index]
            
            # Caso 1: Mesmo elemento (mesma chave ou mesma posição)
            if self.same_vnode(old_child, new_child):
                changes.append(('UPDATE', old_child, new_child))
                old_index += 1
                new_index += 1
                continue
            
            # Caso 2: Novo elemento tem chave que existe no mapa
            if isinstance(new_child, VNode) and new_child.key and new_child.key in key_map:
                mapped_child, mapped_index = key_map[new_child.key]
                changes.append(('MOVE', mapped_child, new_child, new_index))
                del key_map[new_child.key]
                new_index += 1
                continue
            
            # Caso 3: Inserção de novo elemento
            changes.append(('INSERT', new_child, new_index))
            new_index += 1
        
        # Elementos restantes no novo array
        while new_index < len(new_children):
            changes.append(('INSERT', new_children[new_index], new_index))
            new_index += 1
        
        # Elementos restantes no array antigo
        while old_index < len(old_children):
            changes.append(('REMOVE', old_children[old_index], old_index))
            old_index += 1
        
        # Elementos com chaves não utilizadas
        for unused_child, unused_index in key_map.values():
            changes.append(('REMOVE', unused_child, unused_index))
        
        # Aplica as mudanças na ordem reversa para manter índices consistentes
        changes.reverse()
        
        for change in changes:
            op = change[0]
            
            if op == 'UPDATE':
                old_child, new_child = change[1], change[2]
                self.update_dom(parent, old_child, new_child)
            
            elif op == 'INSERT':
                new_child, index = change[1], change[2]
                new_element = self.create_dom(new_child)
                if index < len(parent.childNodes):
                    parent.insertBefore(new_element, parent.childNodes[index])
                else:
                    parent.appendChild(new_element)
            
            elif op == 'REMOVE':
                old_child, index = change[1], change[2]
                parent.removeChild(old_child.element)
            
            elif op == 'MOVE':
                old_child, new_child, new_index = change[1], change[2], change[3]
                self.update_dom(parent, old_child, new_child)
                if new_index < len(parent.childNodes):
                    parent.insertBefore(old_child.element, parent.childNodes[new_index])
                else:
                    parent.appendChild(old_child.element)

    def same_vnode(self, a, b):
        """Determina se dois VNodes representam o mesmo elemento"""
        if type(a) != type(b):
            return False
        
        if isinstance(a, str) and isinstance(b, str):
            return a == b
        
        if isinstance(a, str) or isinstance(b, str):
            raise TypeError('Não é possível comparar classes diferentes')
        
        if a.key and b.key:
            return a.key == b.key
        
        return a.tag == b.tag
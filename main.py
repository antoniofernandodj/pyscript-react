import os
import traceback
import uuid
import base64
from js import document, localStorage
from dataclasses import dataclass, field
from typing import List, Optional

from elements import *  # seu framework de componentes
from component import Component
from state import use_state


def to_inline_style(style_dict: dict) -> str:
    return '; '.join(f'{k.replace("_", "-")}: {v}' for k, v in style_dict.items()) + ';'


def get_connection(db: str):
    import sqlite3
    return sqlite3.connect(db)


@dataclass
class Tarefa:
    descricao: str
    feita: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


class TarefaRepository:
    def __init__(self, db: str, storage):
        self.db = db
        self.storage = storage
        self.init_db()

    def sync_with_storage(self):
        if os.path.exists(self.db):
            with open(self.db, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
                self.storage.setItem(self.db, encoded)

    def init_db(self):
        with get_connection(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tarefas (
                    id TEXT PRIMARY KEY,
                    descricao TEXT NOT NULL,
                    feita INTEGER NOT NULL
                )
            ''')
            conn.commit()

    def add(self, tarefa: Tarefa):
        with get_connection(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tarefas (id, descricao, feita) VALUES (?, ?, ?)",
                (tarefa.id, tarefa.descricao, int(tarefa.feita))
            )
            conn.commit()
            self.sync_with_storage()

    def list_all(self) -> List[Tarefa]:
        with get_connection(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, descricao, feita FROM tarefas")
            rows = cursor.fetchall()
            return [Tarefa(id=row[0], descricao=row[1], feita=bool(row[2])) for row in rows]

    def toggle_feita(self, tarefa_id: str):
        with get_connection(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tarefas SET feita = NOT feita WHERE id = ?", (tarefa_id,)
            )
            conn.commit()
            self.sync_with_storage()

    def delete(self, tarefa_id: str):
        with get_connection(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
            conn.commit()
            self.sync_with_storage()


class TodoApp(Component):

    def init(self):
        if not os.path.exists("tarefas.db"):
            if (db_base64 := localStorage.getItem("tarefas.db")) is not None:
                with open("tarefas.db", "wb") as f:
                    f.write(base64.b64decode(db_base64))
        self.repo = TarefaRepository("tarefas.db", localStorage)
        self.nova_tarefa, self.set_nova_tarefa = use_state(self, '')
        self.tarefas, self.set_tarefas = use_state(self, self.repo.list_all())

        
        self.nova_tarefa_input = input(
            value=self.nova_tarefa.get_value(),
            placeholder="Nova tarefa...",
            on_input=self.on_nova_tarefa_input,
            style=to_inline_style({"marginRight": "8px"}),
            id='nova-tarefa'
        )
    
    def on_nova_tarefa_input(self, e):
        self.set_nova_tarefa(e.target.value)

    def adicionar(self, e):
        e.preventDefault()
        if self.nova_tarefa.get_value().strip():
            self.repo.add(Tarefa(descricao=self.nova_tarefa.get_value().strip()))
            self.set_nova_tarefa('')
            self.set_tarefas(self.repo.list_all())

    def marcar_concluida(self, tarefa_id: str):
        self.repo.toggle_feita(tarefa_id)
        self.set_tarefas(self.repo.list_all())

    def apagar(self, tarefa_id: str):
        self.repo.delete(tarefa_id)
        self.set_tarefas(self.repo.list_all())

    def render(self):

        """
        O motivo pelo qual o input não está mantendo o foco é
        provavelmente porque o render está recriando o DOM inteiro toda
        vez que o estado muda (como ao adicionar uma tarefa).
        Isso faz com que o campo de entrada seja refeito do zero e perca o foco.
        """
        print('rendering...')

        try:
            return div(
                h2("📋 Todo List"),
                form(
                    self.nova_tarefa_input,
                    input("Adicionar", type='submit'),
                    ul(
                        *[
                            li(
                                input(
                                    id=f'tarefa-{tarefa.id}',
                                    type="checkbox", checked='true',
                                    on_change=lambda e: self.marcar_concluida(tarefa.id),
                                ) if tarefa.feita else input(
                                    id=f'tarefa-{tarefa.id}',
                                    type="checkbox",
                                    on_change=lambda e: self.marcar_concluida(tarefa.id),
                                ),
                                span(
                                    tarefa.descricao,
                                    style=to_inline_style({
                                        "text-decoration": "line-through" if tarefa.feita else "none"
                                    })
                                ),
                                button(
                                    "❌",
                                    on_click=lambda e: self.apagar(tarefa.id),
                                    style='margin: "0px 0px 0px 8px;'
                                )

                            )
                            for tarefa in self.tarefas.get_value()
                        ]
                    ),
                    id='form',
                    on_submit=self.adicionar,
                )
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            return div(f"deu não {e}")



async def entrypoint():
    import micropip  # type: ignore
    await micropip.install("sqlite3")

    app = TodoApp()
    root = document.getElementById("app")
    app.run(root)


if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(entrypoint())

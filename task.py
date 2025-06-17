import os
import traceback
import uuid
import base64
from js import document, localStorage
from dataclasses import dataclass, field
from typing import List, Optional

from elements import *  # seu framework de componentes
from component import Component


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
        self.nova_tarefa = "nova tarefa"
        self.tarefas = self.repo.list_all()

    def adicionar(self, _=None):
        if self.nova_tarefa.strip():
            self.repo.add(Tarefa(descricao=self.nova_tarefa.strip()))
            self.nova_tarefa = ""
            self.tarefas = self.repo.list_all()
            # self.update()

    def marcar_concluida(self, tarefa_id: str):
        self.repo.toggle_feita(tarefa_id)
        self.tarefas = self.repo.list_all()
        # self.update()

    def apagar(self, tarefa_id: str):
        self.repo.delete(tarefa_id)
        self.tarefas = self.repo.list_all()
        # self.update()

    def render(self):

        try:
            return div(
                h2("📋 Todo List"),
                input(
                    value=self.nova_tarefa,
                    placeholder="Nova tarefa...",
                    on_input=lambda e: setattr(self, "nova_tarefa", e.target.value),
                    style={"marginRight": "8px"}
                ),
                button("Adicionar", on_click=self.adicionar),
                ul(
                    *[
                        li(
                            input(
                                type="checkbox",
                                checked=tarefa.feita,
                                on_change=lambda e: self.marcar_concluida(tarefa.id)
                            ),
                            span(tarefa.descricao, style={
                                "textDecoration": "line-through" if tarefa.feita else "none"
                            }),
                            button("❌", on_click=lambda e: self.apagar(tarefa.id), style='margin: "0px 0px 0px 8px;')

                        )
                        for tarefa in self.tarefas
                    ]
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

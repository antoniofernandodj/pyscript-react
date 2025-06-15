from js import document, console, setTimeout
from pyodide.ffi import create_proxy
import json



class Logger:
    def __init__(self):
        self.el = document.createElement("pre")
        self.el.style.position = "fixed"
        self.el.style.bottom = "10px"
        self.el.style.right = "10px"
        self.el.style.width = "300px"
        self.el.style.zIndex = "9999"
        self.el.style.boxShadow = "0 0 10px rgba(0,0,0,0.2)"

    def _append(self, level, message, color):
        line = document.createElement("div")
        line.innerHTML = f"[{level.upper()}] {message}"
        line.style.color = color
        self.el.appendChild(line)

        def scroll():
            self.el.scrollTop = self.el.scrollHeight

        setTimeout(create_proxy(scroll), 0)

    def log(self, message):
        message = self.to_string(message)
        console.log(f'[LOG] {message}')
        self._append("log", message, "#333")

    def info(self, message):
        message = self.to_string(message)
        console.info(f'[INFO] {message}')
        self._append("info", message, "blue")

    def warn(self, message):
        message = self.to_string(message)
        console.warn(message)
        self._append("warn", message, "orange")

    def error(self, message):
        message = self.to_string(message)
        console.error(message)
        self._append("error", message, "red")

    def debug(self, message):
        message = self.to_string(message)
        print(f'[DEBUG] {message}')
        self._append("debug", message, "purple")

    def __call__(self):
        return self.el

    def to_string(self, message):
        if isinstance(message, (dict, list)):
            try:
                return json.dumps(message, indent=2)
            except Exception:
                return str(message)
        return str(message)


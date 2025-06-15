from js import setInterval, clearInterval
from js import document # type: ignore
from pyodide.ffi import create_proxy

from component import Component



# Elementos HTML declarativos
def el(tag, *children, **attrs):
    element = document.createElement(tag)
    for child in children:
        if isinstance(child, (str, int, float)):
            element.appendChild(document.createTextNode(str(child)))
        else:
            element.appendChild(child)
    for attr, value in attrs.items():
        if attr.startswith("on_"):
            event = attr.split("_", 1)[1]
            element.addEventListener(event, create_proxy(value))
        else:
            element.setAttribute(attr, value)
    return element


# Todas as funções declarativas HTML

def a(*children, **attrs): return el("a", *children, **attrs)
def abbr(*children, **attrs): return el("abbr", *children, **attrs)
def address(*children, **attrs): return el("address", *children, **attrs)
def area(*children, **attrs): return el("area", *children, **attrs)
def article(*children, **attrs): return el("article", *children, **attrs)
def aside(*children, **attrs): return el("aside", *children, **attrs)
def audio(*children, **attrs): return el("audio", *children, **attrs)
def b(*children, **attrs): return el("b", *children, **attrs)
def base(*children, **attrs): return el("base", *children, **attrs)
def bdi(*children, **attrs): return el("bdi", *children, **attrs)
def bdo(*children, **attrs): return el("bdo", *children, **attrs)
def blockquote(*children, **attrs): return el("blockquote", *children, **attrs)
def body(*children, **attrs): return el("body", *children, **attrs)
def br(*children, **attrs): return el("br", *children, **attrs)
def button(*children, **attrs): return el("button", *children, **attrs)
def canvas(*children, **attrs): return el("canvas", *children, **attrs)
def caption(*children, **attrs): return el("caption", *children, **attrs)
def cite(*children, **attrs): return el("cite", *children, **attrs)
def code(*children, **attrs): return el("code", *children, **attrs)
def col(*children, **attrs): return el("col", *children, **attrs)
def colgroup(*children, **attrs): return el("colgroup", *children, **attrs)
def data(*children, **attrs): return el("data", *children, **attrs)
def datalist(*children, **attrs): return el("datalist", *children, **attrs)
def dd(*children, **attrs): return el("dd", *children, **attrs)
def del_(*children, **attrs): return el("del", *children, **attrs)  # 'del' é palavra reservada
def details(*children, **attrs): return el("details", *children, **attrs)
def dfn(*children, **attrs): return el("dfn", *children, **attrs)
def dialog(*children, **attrs): return el("dialog", *children, **attrs)
def div(*children, **attrs): return el("div", *children, **attrs)
def dl(*children, **attrs): return el("dl", *children, **attrs)
def dt(*children, **attrs): return el("dt", *children, **attrs)
def em(*children, **attrs): return el("em", *children, **attrs)
def embed(*children, **attrs): return el("embed", *children, **attrs)
def fieldset(*children, **attrs): return el("fieldset", *children, **attrs)
def figcaption(*children, **attrs): return el("figcaption", *children, **attrs)
def figure(*children, **attrs): return el("figure", *children, **attrs)
def footer(*children, **attrs): return el("footer", *children, **attrs)
def form(*children, **attrs): return el("form", *children, **attrs)
def h1(*children, **attrs): return el("h1", *children, **attrs)
def h2(*children, **attrs): return el("h2", *children, **attrs)
def h3(*children, **attrs): return el("h3", *children, **attrs)
def h4(*children, **attrs): return el("h4", *children, **attrs)
def h5(*children, **attrs): return el("h5", *children, **attrs)
def h6(*children, **attrs): return el("h6", *children, **attrs)
def head(*children, **attrs): return el("head", *children, **attrs)
def header(*children, **attrs): return el("header", *children, **attrs)
def hgroup(*children, **attrs): return el("hgroup", *children, **attrs)
def hr(*children, **attrs): return el("hr", *children, **attrs)
def html(*children, **attrs): return el("html", *children, **attrs)
def i(*children, **attrs): return el("i", *children, **attrs)
def iframe(*children, **attrs): return el("iframe", *children, **attrs)
def img(*children, **attrs): return el("img", *children, **attrs)
def input(*children, **attrs): return el("input", *children, **attrs)
def ins(*children, **attrs): return el("ins", *children, **attrs)
def kbd(*children, **attrs): return el("kbd", *children, **attrs)
def label(*children, **attrs): return el("label", *children, **attrs)
def legend(*children, **attrs): return el("legend", *children, **attrs)
def li(*children, **attrs): return el("li", *children, **attrs)
def link(*children, **attrs): return el("link", *children, **attrs)
def main(*children, **attrs): return el("main", *children, **attrs)
def map(*children, **attrs): return el("map", *children, **attrs)
def mark(*children, **attrs): return el("mark", *children, **attrs)
def meta(*children, **attrs): return el("meta", *children, **attrs)
def meter(*children, **attrs): return el("meter", *children, **attrs)
def nav(*children, **attrs): return el("nav", *children, **attrs)
def noscript(*children, **attrs): return el("noscript", *children, **attrs)
def object(*children, **attrs): return el("object", *children, **attrs)
def ol(*children, **attrs): return el("ol", *children, **attrs)
def optgroup(*children, **attrs): return el("optgroup", *children, **attrs)
def option(*children, **attrs): return el("option", *children, **attrs)
def output(*children, **attrs): return el("output", *children, **attrs)
def p(*children, **attrs): return el("p", *children, **attrs)
def param(*children, **attrs): return el("param", *children, **attrs)
def picture(*children, **attrs): return el("picture", *children, **attrs)
def pre(*children, **attrs): return el("pre", *children, **attrs)
def progress(*children, **attrs): return el("progress", *children, **attrs)
def q(*children, **attrs): return el("q", *children, **attrs)
def rp(*children, **attrs): return el("rp", *children, **attrs)
def rt(*children, **attrs): return el("rt", *children, **attrs)
def ruby(*children, **attrs): return el("ruby", *children, **attrs)
def s(*children, **attrs): return el("s", *children, **attrs)
def samp(*children, **attrs): return el("samp", *children, **attrs)
def script(*children, **attrs): return el("script", *children, **attrs)
def section(*children, **attrs): return el("section", *children, **attrs)
def select(*children, **attrs): return el("select", *children, **attrs)
def small(*children, **attrs): return el("small", *children, **attrs)
def source(*children, **attrs): return el("source", *children, **attrs)
def span(*children, **attrs): return el("span", *children, **attrs)
def strong(*children, **attrs): return el("strong", *children, **attrs)
def style(*children, **attrs): return el("style", *children, **attrs)
def sub(*children, **attrs): return el("sub", *children, **attrs)
def summary(*children, **attrs): return el("summary", *children, **attrs)
def sup(*children, **attrs): return el("sup", *children, **attrs)
def table(*children, **attrs): return el("table", *children, **attrs)
def tbody(*children, **attrs): return el("tbody", *children, **attrs)
def td(*children, **attrs): return el("td", *children, **attrs)
def template(*children, **attrs): return el("template", *children, **attrs)
def textarea(*children, **attrs): return el("textarea", *children, **attrs)
def tfoot(*children, **attrs): return el("tfoot", *children, **attrs)
def th(*children, **attrs): return el("th", *children, **attrs)
def thead(*children, **attrs): return el("thead", *children, **attrs)
def time(*children, **attrs): return el("time", *children, **attrs)
def title(*children, **attrs): return el("title", *children, **attrs)
def tr(*children, **attrs): return el("tr", *children, **attrs)
def track(*children, **attrs): return el("track", *children, **attrs)
def u(*children, **attrs): return el("u", *children, **attrs)
def ul(*children, **attrs): return el("ul", *children, **attrs)
def var(*children, **attrs): return el("var", *children, **attrs)
def video(*children, **attrs): return el("video", *children, **attrs)
def wbr(*children, **attrs): return el("wbr", *children, **attrs)



def set_interval(callable, time_ms):
    proxy = create_proxy(callable)
    return setInterval(proxy, time_ms)  # 1 segundo


def clear_interval(interval_id):
    clearInterval(interval_id)




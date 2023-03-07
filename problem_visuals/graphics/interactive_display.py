from problem_visuals.graphics.svg_handling import SvgProducer, prepare_output
import uuid
from IPython.display import display, clear_output

repl_code = """
var svg = {}
container = svg.parentNode;
svg_new = '{}'
container.innerHTML = svg_new   
    """


class JSCode:
    def __init__(self, content="content"):
        self.content = content

    def _repr_html_(self):
        return f"<script type='application/javascript'>{self.content}</script>"


def exec_js(code):
    display(JSCode(code))


class InteractiveDisplay(SvgProducer):

    def __init__(self, viewbox_width: int, viewbox_height: int, ipy_off: bool = False,
                 html_width: str = "25%"):
        super().__init__(viewbox_width, viewbox_height, ipy_off, html_width)
        self.raw_svg.attrib["id"] = "id" + str(uuid.uuid1()).replace("-", "")

    def update(self):
        id = self.raw_svg.attrib["id"]
        selector = f"""document.querySelector("#{id}");"""
        code = repl_code.format(selector, prepare_output(self.raw_svg, ipy_off=True))
        exec_js(code)
        clear_output()
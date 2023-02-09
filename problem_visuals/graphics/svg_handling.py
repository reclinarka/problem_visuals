try:
    from ipywidgets import Layout, HTML

    ipy_loaded = True
except ModuleNotFoundError:
    print("Jupyter not found, using standard wrapper")
    ipy_loaded = False

import xml.etree.ElementTree as ET


class SvgWrapper(str):
    def _repr_svg_(self):
        return self

    def save_svg(self, file):
        with open(file, "w") as f:
            f.write(self)


def prepare_output(svg, ipy_off=False, html_width="25%"):
    svg = SvgWrapper(ET.tostring(svg).decode("utf-8"))
    if ipy_loaded and not ipy_off:
        html_wrapper = f'<div style="{html_width}">{svg}</div>'
        svg_widget = HTML(value=html_wrapper, layout=Layout(grid_area="top"))
        return svg_widget
    return svg


def svg_f(viewbox_width: int, viewbox_height: int) -> ET.Element:
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "version": "1.2",
        "baseProfile": "tiny",
        "viewBox": f"0 0 {viewbox_width:d} {viewbox_height:d}",
    })
    return svg


def attrs_f(attrs):
    return {k: str(v) for k, v in attrs.items() if v is not None}


def remove_elements_by_attr_values(svg: ET, attrs: list):
    filter_str = "./*" + "".join([f"[@{attr}'{val}']" for attr, val in attrs])
    for el in svg.findall(filter_str):
        svg.remove(el)


def add_line(svg: ET, x1: int, y1: int, x2: int, y2: int, color: str, width: float, stroke_linecap: str = "butt"):
    ET.SubElement(svg, "line", attrs_f({
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "stroke": color,
        "stroke-width": width,
        "stroke-linecap": stroke_linecap
    }))


class SvgProducer:
    raw_svg = None
    defs = None
    ipy_off = False
    html_width = "25%"

    def __init__(self, viewbox_width: int, viewbox_height: int, ipy_off: bool = False,
                 html_width: str = "25%"):
        self.ipy_off = ipy_off
        self.html_width = html_width
        self.raw_svg = svg_f(viewbox_width, viewbox_height)
        self.defs = ET.SubElement(self.raw_svg, "defs")

    def _repr_html_(self):
        return "<div style='width:{}'>{}</div>".format(self.html_width, prepare_output(self.raw_svg, ipy_off=True))

    def present(self):
        return prepare_output(self.raw_svg, ipy_off=self.ipy_off, html_width=self.html_width)

    def save_svg(self, file):
        with open(file, "w") as f:
            f.write(ET.tostring(self.raw_svg).decode("utf-8"))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the chess-problem-visuals library.
# Copyright (C) 2012-2021 Philipp Polland <contact@philipp-polland.dev>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import xml.etree.ElementTree as ET
import math

try:
    from ipywidgets import Layout, HTML

    ipy_loaded = True
except ModuleNotFoundError:
    print("Jupyter not found, using standard wrapper")
    ipy_loaded = False

PIECES = {
    "b": """<g id="black-bishop" class="black bishop" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.354.49-2.323.47-3-.5 1.354-1.94 3-2 3-2zm6-4c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2zM25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z" fill="#000" stroke-linecap="butt"/><path d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5" stroke="#fff" stroke-linejoin="miter"/></g>""",
    # noqa: E501
    "k": """<g id="black-king" class="black king" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22.5 11.63V6" stroke-linejoin="miter"/><path d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5" fill="#000" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z" fill="#000"/><path d="M20 8h5" stroke-linejoin="miter"/><path d="M32 29.5s8.5-4 6.03-9.65C34.15 14 25 18 22.5 24.5l.01 2.1-.01-2.1C20 18 9.906 14 6.997 19.85c-2.497 5.65 4.853 9 4.853 9M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0" stroke="#fff"/></g>""",
    # noqa: E501
    "n": """<g id="black-knight" class="black knight" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 22,10 C 32.5,11 38.5,18 38,39 L 15,39 C 15,30 25,32.5 23,18" style="fill:#000000; stroke:#000000;"/><path d="M 24,18 C 24.38,20.91 18.45,25.37 16,27 C 13,29 13.18,31.34 11,31 C 9.958,30.06 12.41,27.96 11,28 C 10,28 11.19,29.23 10,30 C 9,30 5.997,31 6,26 C 6,24 12,14 12,14 C 12,14 13.89,12.1 14,10.5 C 13.27,9.506 13.5,8.5 13.5,7.5 C 14.5,6.5 16.5,10 16.5,10 L 18.5,10 C 18.5,10 19.28,8.008 21,7 C 22,7 22,10 22,10" style="fill:#000000; stroke:#000000;"/><path d="M 9.5 25.5 A 0.5 0.5 0 1 1 8.5,25.5 A 0.5 0.5 0 1 1 9.5 25.5 z" style="fill:#ececec; stroke:#ececec;"/><path d="M 15 15.5 A 0.5 1.5 0 1 1 14,15.5 A 0.5 1.5 0 1 1 15 15.5 z" transform="matrix(0.866,0.5,-0.5,0.866,9.693,-5.173)" style="fill:#ececec; stroke:#ececec;"/><path d="M 24.55,10.4 L 24.1,11.85 L 24.6,12 C 27.75,13 30.25,14.49 32.5,18.75 C 34.75,23.01 35.75,29.06 35.25,39 L 35.2,39.5 L 37.45,39.5 L 37.5,39 C 38,28.94 36.62,22.15 34.25,17.66 C 31.88,13.17 28.46,11.02 25.06,10.5 L 24.55,10.4 z " style="fill:#ececec; stroke:none;"/></g>""",
    # noqa: E501
    "p": """<g id="black-pawn" class="black pawn"><path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z" fill="#000" stroke="#000" stroke-width="1.5" stroke-linecap="round"/></g>""",
    # noqa: E501
    "q": """<g id="black-queen" class="black queen" fill="#000" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><g fill="#000" stroke="none"><circle cx="6" cy="12" r="2.75"/><circle cx="14" cy="9" r="2.75"/><circle cx="22.5" cy="8" r="2.75"/><circle cx="31" cy="9" r="2.75"/><circle cx="39" cy="12" r="2.75"/></g><path d="M9 26c8.5-1.5 21-1.5 27 0l2.5-12.5L31 25l-.3-14.1-5.2 13.6-3-14.5-3 14.5-5.2-13.6L14 25 6.5 13.5 9 26zM9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z" stroke-linecap="butt"/><path d="M11 38.5a35 35 1 0 0 23 0" fill="none" stroke-linecap="butt"/><path d="M11 29a35 35 1 0 1 23 0M12.5 31.5h20M11.5 34.5a35 35 1 0 0 22 0M10.5 37.5a35 35 1 0 0 24 0" fill="none" stroke="#fff"/></g>""",
    # noqa: E501
    "r": """<g id="black-rook" class="black rook" fill="#000" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 39h27v-3H9v3zM12.5 32l1.5-2.5h17l1.5 2.5h-20zM12 36v-4h21v4H12z" stroke-linecap="butt"/><path d="M14 29.5v-13h17v13H14z" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M14 16.5L11 14h23l-3 2.5H14zM11 14V9h4v2h5V9h5v2h5V9h4v5H11z" stroke-linecap="butt"/><path d="M12 35.5h21M13 31.5h19M14 29.5h17M14 16.5h17M11 14h23" fill="none" stroke="#fff" stroke-width="1" stroke-linejoin="miter"/></g>""",
    # noqa: E501
    "B": """<g id="white-bishop" class="white bishop" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><g fill="#fff" stroke-linecap="butt"><path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.354.49-2.323.47-3-.5 1.354-1.94 3-2 3-2zM15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2zM25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z"/></g><path d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5" stroke-linejoin="miter"/></g>""",
    # noqa: E501
    "K": """<g id="white-king" class="white king" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22.5 11.63V6M20 8h5" stroke-linejoin="miter"/><path d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5" fill="#fff" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10V37z" fill="#fff"/><path d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0"/></g>""",
    # noqa: E501
    "N": """<g id="white-knight" class="white knight" fill="none" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M 22,10 C 32.5,11 38.5,18 38,39 L 15,39 C 15,30 25,32.5 23,18" style="fill:#ffffff; stroke:#000000;"/><path d="M 24,18 C 24.38,20.91 18.45,25.37 16,27 C 13,29 13.18,31.34 11,31 C 9.958,30.06 12.41,27.96 11,28 C 10,28 11.19,29.23 10,30 C 9,30 5.997,31 6,26 C 6,24 12,14 12,14 C 12,14 13.89,12.1 14,10.5 C 13.27,9.506 13.5,8.5 13.5,7.5 C 14.5,6.5 16.5,10 16.5,10 L 18.5,10 C 18.5,10 19.28,8.008 21,7 C 22,7 22,10 22,10" style="fill:#ffffff; stroke:#000000;"/><path d="M 9.5 25.5 A 0.5 0.5 0 1 1 8.5,25.5 A 0.5 0.5 0 1 1 9.5 25.5 z" style="fill:#000000; stroke:#000000;"/><path d="M 15 15.5 A 0.5 1.5 0 1 1 14,15.5 A 0.5 1.5 0 1 1 15 15.5 z" transform="matrix(0.866,0.5,-0.5,0.866,9.693,-5.173)" style="fill:#000000; stroke:#000000;"/></g>""",
    # noqa: E501
    "P": """<g id="white-pawn" class="white pawn"><path d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z" fill="#fff" stroke="#000" stroke-width="1.5" stroke-linecap="round"/></g>""",
    # noqa: E501
    "Q": """<g id="white-queen" class="white queen" fill="#fff" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM24.5 7.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM41 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM16 8.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM33 9a2 2 0 1 1-4 0 2 2 0 1 1 4 0z"/><path d="M9 26c8.5-1.5 21-1.5 27 0l2-12-7 11V11l-5.5 13.5-3-15-3 15-5.5-14V25L7 14l2 12zM9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z" stroke-linecap="butt"/><path d="M11.5 30c3.5-1 18.5-1 22 0M12 33.5c6-1 15-1 21 0" fill="none"/></g>""",
    # noqa: E501
    "R": """<g id="white-rook" class="white rook" fill="#fff" fill-rule="evenodd" stroke="#000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 39h27v-3H9v3zM12 36v-4h21v4H12zM11 14V9h4v2h5V9h5v2h5V9h4v5" stroke-linecap="butt"/><path d="M34 14l-3 3H14l-3-3"/><path d="M31 17v12.5H14V17" stroke-linecap="butt" stroke-linejoin="miter"/><path d="M31 29.5l1.5 2.5h-20l1.5-2.5"/><path d="M11 14h23" fill="none" stroke-linejoin="miter"/></g>""",
    # noqa: E501
}

PIECE_CLASS_REF = {
    "b": "#black-bishop",
    "k": "#black-king",
    "n": "#black-knight",
    "p": "#black-pawn",
    "q": "#black-queen",
    "r": "#black-rook",
    "B": "#white-bishop",
    "K": "#white-king",
    "N": "#white-knight",
    "P": "#white-pawn",
    "Q": "#white-queen",
    "R": "#white-rook"
}


def attrs_f(attrs):
    return {k: str(v) for k, v in attrs.items() if v is not None}


def svg_f(viewbox: int, size: int = None) -> ET.Element:
    svg = ET.Element("svg", {
        "xmlns": "http://www.w3.org/2000/svg",
        "xmlns:xlink": "http://www.w3.org/1999/xlink",
        "version": "1.2",
        "baseProfile": "tiny",
        "viewBox": f"0 0 {viewbox:d} {viewbox:d}",
    })
    if size is not None:
        svg.set("width", str(size))
        svg.set("height", str(size))
    return svg


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


def create_base(n: int = 8, SQUARE_SIZE: int = 16, size: int = None):
    svg = svg_f(n * SQUARE_SIZE, size)
    fields = [(file, rank) for file in range(n) for rank in range(n)]
    defs = ET.SubElement(svg, "defs")
    for _, piece_string in PIECES.items():
        defs.append(ET.fromstring(piece_string))
    for file_index, rank_index in fields:
        x = file_index * SQUARE_SIZE
        y = rank_index * SQUARE_SIZE
        light = (file_index + rank_index) % 2 == 0
        cls = ["square", "light" if light else "dark"]
        square_color = "#ffce9e" if light else "#d18b47"
        ET.SubElement(svg, "rect", attrs_f({
            "x": x,
            "y": y,
            "width": SQUARE_SIZE,
            "height": SQUARE_SIZE,
            "class": " ".join(cls),
            "stroke": "none",
            "fill": square_color,
            "opacity": 1.0,
        }))
    return svg


class Board:

    def add_piece(self, position: tuple, piece: str):
        svg = self.raw_svg
        assert piece in PIECE_CLASS_REF.keys(), "unknown piece"
        file_index, rank_index = position
        assert self.n > file_index >= 0 and self.n > rank_index >= 0, "Piece is outside of board"

        x = file_index * self.SQUARE_SIZE
        y = rank_index * self.SQUARE_SIZE

        href = PIECE_CLASS_REF[piece]
        ET.SubElement(svg, "use", attrs_f({
            "href": href,
            "xlink:href": href,
            "transform": f"translate({x:d}, {y:d}) scale({self.scale:f})",
        }))

        self.raw_svg = svg
        return self

    def add_arrow(self, tail, head, default_color="white", arrow_width=1):
        svg = self.raw_svg
        SQUARE_SIZE = self.SQUARE_SIZE

        tail_file, tail_rank = tail
        head_file, head_rank = head

        if abs(tail_rank - head_rank) + abs(tail_file - head_file) != 3:
            color = "red"
        else:
            color = default_color

        xtail = (tail_file + 0.5) * SQUARE_SIZE
        ytail = (tail_rank + 0.5) * SQUARE_SIZE
        xhead = (head_file + 0.5) * SQUARE_SIZE
        yhead = (head_rank + 0.5) * SQUARE_SIZE

        marker_size = 0.75 * SQUARE_SIZE
        marker_margin = 0.1 * SQUARE_SIZE

        dx, dy = xhead - xtail, yhead - ytail
        hypot = math.hypot(dx, dy)

        shaft_x = xhead - dx * (marker_size + marker_margin) / hypot
        shaft_y = yhead - dy * (marker_size + marker_margin) / hypot

        xtip = xhead - dx * marker_margin / hypot
        ytip = yhead - dy * marker_margin / hypot

        ET.SubElement(svg, "line", attrs_f({
            "x1": xtail,
            "y1": ytail,
            "x2": shaft_x,
            "y2": shaft_y,
            "stroke": color,
            "stroke-width": SQUARE_SIZE * 0.2 * arrow_width,
            "stroke-linecap": "butt",
            "class": "arrow",
        }))

        marker = [(xtip, ytip),
                  (shaft_x + dy * 0.5 * arrow_width * marker_size / hypot,
                   shaft_y - dx * 0.5 * arrow_width * marker_size / hypot),
                  (shaft_x - dy * 0.5 * arrow_width * marker_size / hypot,
                   shaft_y + dx * 0.5 * arrow_width * marker_size / hypot)]

        ET.SubElement(svg, "polygon", attrs_f({
            "points": " ".join(f"{x},{y}" for x, y in marker),
            "fill": color,
            "class": "arrow",
        }))

        return self

        return self

    def __init__(self, n: int = 8, SQUARE_SIZE: int = 16, size: int = None, ipy_off: bool = False,
                 html_width: str = "25%"):
        self.n = n
        self.SQUARE_SIZE = SQUARE_SIZE
        self.size = size
        self.ipy_off = ipy_off
        self.html_width = html_width
        self.scale = SQUARE_SIZE / 45
        self.raw_svg = create_base(n, SQUARE_SIZE, size)

    def _repr_html_(self):
        return "<div style='width:{}'>{}</div>".format(self.html_width, prepare_output(self.raw_svg, ipy_off=True))

    def present(self):
        return prepare_output(self.raw_svg, ipy_off=self.ipy_off, html_width=self.html_width)

    def save_svg(self, file):
        with open(file, "w") as f:
            f.write(ET.tostring(self.raw_svg).decode("utf-8"))


def paint_problem_board(n: int = 8, SQUARE_SIZE: int = 16, size: int = None, ipy_off=False, Qs: list = None,
                        K_start: tuple = None, K_path: list = None, html_width: str = "25%", arrow_color="white",
                        arrow_width=1):
    board = Board(n, SQUARE_SIZE, size, ipy_off, html_width)

    if Qs:
        for file_index, rank_index in enumerate(Qs):
            if rank_index is None:
                continue
            board.add_piece((file_index, rank_index), "Q")
    if K_start:
        '''
        Knight tour Problem:
            A Knight is placed somewhere on th
        '''
        assert isinstance(K_start,
                          tuple), "K_start should be of format (knight_x,knight_y)"
        file_index, rank_index = K_start
        board.add_piece((file_index, rank_index), "N")

        if K_path and len(K_path) > 1:
            last_step = K_path[0]
            assert isinstance(last_step, tuple), "A step should be a tuple of form (x,y)"
            for step in K_path[1:]:
                assert isinstance(step, tuple), "A step should be a tuple of form (x,y)"
                board.add_arrow(last_step, step, default_color=arrow_color, arrow_width=arrow_width)
                last_step = step

    return board


def knight_tour(n: int, K_start: tuple, K_path: list,
                html_width="25%", SQUARE_SIZE: int = 16, size: int = None, ipy_off=False, arrow_color="white",
                arrow_width=1):
    visited = []

    while len(K_path) > 0:
        board = Board(n=n, SQUARE_SIZE=SQUARE_SIZE, size=size, ipy_off=ipy_off,
                      html_width=html_width, arrow_width= arrow_width, arrow_color=arrow_color)
        board.add_piece(K_start, "N")

        visited.append(K_start)

        for rank in range(n):
            for file in range(n):
                pos = (file, rank)
                if pos not in visited:
                    board.add_piece(pos, "p")

        last_point = K_start
        for point in K_path:
            board.add_arrow(last_point, point, arrow_color)

        K_start = K_path[0]
        K_path = K_path[1:]
        yield board

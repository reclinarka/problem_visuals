from problem_visuals.graphics.svg_handling import SvgProducer, attrs_f, add_line
import xml.etree.ElementTree as ET


class Grid(SvgProducer):
    margin_x = 6
    margin_y = 5

    def __init__(self, viewbox: int = 180, ipy_off: bool = False, html_width: str = "25%",
                 state: list = None, square_size: int = 20, assigned: dict = None, highlight: str = "#99ff33"):
        super().__init__(viewbox, viewbox, ipy_off, html_width)
        self.square_size = square_size
        self.setup_grid()
        self.checker = [[None for i in range(9)] for j in range(9)]
        if state:
            self.state = state
            for x in range(9):
                for y in range(9):
                    if state[y][x] != '*':
                        self.add_number(state[y][x], y, x)
        if assigned:
            for coord, val in assigned.items():
                row = int(coord[1]) - 1
                col = int(coord[2]) - 1
                self.add_number(val, row, col, highlight)

    def add_number(self, number: int, row, col, color: str = "black"):
        assert not isinstance(self.checker[row][col], ET.Element), f"Double assignment of {row},{col}"
        x = col * 20 + self.margin_x
        y = (row + 1) * 20 - self.margin_y
        svg = self.raw_svg
        num = ET.SubElement(svg, "text", attrs_f({
            "x": x,
            "y": y,
            "stroke": color,
            "fill": color,
        }))
        num.text = str(number)
        self.checker[row][col] = num
        return self

    def remove_number(self, row: int, col: int):
        assert isinstance(self.checker[row][col], ET.Element), f"No element at {row},{col}"
        svg = self.raw_svg
        svg.remove(self.checker[row][col])
        self.checker[row][col] = False
        return self

    def change_number(self, number: int, row: int, col: int, color: str = "black"):
        assert isinstance(self.checker[row][col], ET.Element), f"No element at {row},{col}"
        self.checker[row][col].text = str(number)
        self.checker[row][col].attrib["fill"] = color
        self.checker[row][col].attrib["stroke"] = color
        return self

    def setup_grid(self):
        svg = self.raw_svg
        square_size = self.square_size
        square_highlighted = 0

        # field accents
        for row in range(9):
            square_highlighted = 0 < (row) // 3 < 2
            for col in range(9):
                if col % 3 == 0:
                    square_highlighted = not square_highlighted
                if not square_highlighted:
                    color = "#6699cc" if (col + row) % 2 == 0 else "#79a6d2"
                else:
                    color = "#538cc6" if (col + row) % 2 == 0 else "#8cb3d9"
                ET.SubElement(svg, "rect", attrs_f({
                    "x": (col) * square_size,
                    "y": (row) * square_size,
                    "width": square_size,
                    "height": square_size,
                    "stroke": "none",
                    "fill": color,
                }))
        # boarder
        # verticals

        max_coord = 9 * square_size
        for i in range(4):
            x = square_size * i * 3
            add_line(svg, x, 0, x, max_coord, "white", 1.2)
        # horizontals
        for i in range(4):
            y = square_size * i * 3
            add_line(svg, 0, y, max_coord, y, "white", 1.2)
        return self

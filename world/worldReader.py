from dataclasses import dataclass
import xml.etree.ElementTree as ET

@dataclass
class Beeper:
    x: int
    y: int
    count: int

@dataclass
class Wall:
    x1: int
    y1: int
    horizontal: bool

@dataclass
class Karel:
    x: int
    y: int
    direction: str

@dataclass
class World:
    width: int
    height: int
    beepers: list[Beeper]
    walls: list[Wall]
    karel: Karel
    eval_cells: set[tuple[int, int]]

def loadWorld(path: str) -> World:
    tree = ET.parse(path)
    root = tree.getroot()

    worldXML = root.find(".//mundo")

    if worldXML is None:
        raise ValueError("File Invalid, No world tag found")

    width = int(worldXML.attrib["ancho"])
    height = int(worldXML.attrib["alto"])

    beepers = []
    walls = []

    eval_cells = set()

    for elem in worldXML:
        if elem.tag == "monton":
            beepers.append(
                Beeper(
                    x=int(elem.attrib["x"]),
                    y=int(elem.attrib["y"]),
                    count=int(elem.attrib["zumbadores"])
                )
            )

        elif elem.tag == "pared":
            x1 = int(elem.attrib["x1"])
            y1 = int(elem.attrib["y1"])

            if "x2" in elem.attrib:
                x2 = int(elem.attrib["x2"])

                for x in range(x1, x2):
                    walls.append(
                        Wall(
                            x1=x,
                            y1=y1,
                            horizontal=True
                        )
                    )
            elif "y2" in elem.attrib:
                y2 = int(elem.attrib["y2"])

                for y in range(y1, y2):
                    walls.append(
                        Wall(
                            x1=x1,
                            y1=y,
                            horizontal=False
                        )
                    )

        elif elem.tag == "posicionDump":
            eval_cells.add(
                (
                    int(elem.attrib["x"]),
                    int(elem.attrib["y"])
                )
            )

    programXML = root.find(".//programa")

    if programXML is None:
        raise ValueError("File Invalid, No program tag found")

    karel = Karel(
        x=int(programXML.attrib["xKarel"]),
        y=int(programXML.attrib["yKarel"]),
        direction=programXML.attrib["direccionKarel"]
    )

    return World(
        width=width,
        height=height,
        beepers=beepers,
        walls=walls,
        karel=karel,
        eval_cells=eval_cells
    )
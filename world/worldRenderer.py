from worldReader import *

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class WorldView(QGraphicsView):
    CELL_SIZE = 40
    def __init__(self, world):
        super().__init__()

        self.world = world

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setBackgroundBrush(QBrush(Qt.white))

        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.render_world()

    def render_world(self):
        self.draw_grid()
        self.draw_evaluator()
        self.draw_beepers()
        self.draw_walls()
        self.draw_karel()

        self.setSceneRect(
            self.scene.itemsBoundingRect()
        )

    def draw_grid(self):
        pen = QPen(QColor(180, 180, 180))

        for x in range(self.world.width + 1):
            self.scene.addLine(
                x * self.CELL_SIZE,
                0,
                x * self.CELL_SIZE,
                self.world.height * self.CELL_SIZE,
                pen
            )

        for y in range(self.world.height + 1):
            self.scene.addLine(
                0,
                y * self.CELL_SIZE,
                self.world.width * self.CELL_SIZE,
                y * self.CELL_SIZE,
                pen
            )

    def draw_beepers(self):
        green = QBrush(QColor(0, 181, 26))
        pen = QPen(QColor(0,0,0))
        pen.setWidth(2)

        beeperSize = self.CELL_SIZE // 2

        for b in self.world.beepers:
            sx, sy = self.world_to_scene(b.x, b.y)

            offset = (self.CELL_SIZE - beeperSize) / 2

            self.scene.addRect(
                sx + offset,
                sy + offset,
                beeperSize,
                beeperSize,
                QPen(QColor(0, 181, 26)),
                green
            )

            text = self.scene.addText(str(b.count))
            text.setDefaultTextColor(QColor(0,0,0))

            font = QFont()
            font.setPixelSize(int(beeperSize * 0.6))
            text.setFont(font)

            textRect = text.boundingRect()
            text.setPos(
                sx + (self.CELL_SIZE - textRect.width()) / 2,
                sy + (self.CELL_SIZE - textRect.height()) / 2
            )

    def draw_walls(self):
        pen = QPen(Qt.black)
        pen.setWidth(3)

        for wall in self.world.walls:
            sx, sy = self.world_to_scene(wall.x1 + 1, wall.y1 + 1)

            if wall.horizontal:
                self.scene.addLine(
                    sx, sy + self.CELL_SIZE,
                    sx + self.CELL_SIZE, sy + self.CELL_SIZE,
                    pen
                )
            else:
                self.scene.addLine(
                    sx, sy,
                    sx, sy + self.CELL_SIZE,
                    pen
                )

    def draw_karel(self):
        sx, sy = self.world_to_scene(self.world.karel.x, self.world.karel.y)

        centerX = sx + self.CELL_SIZE / 2
        centerY = sy + self.CELL_SIZE / 2

        poly = QPolygonF([
            QPointF(centerX - 10, centerY - 10),
            QPointF(centerX + 10, centerY),
            QPointF(centerX - 10, centerY + 10)
        ])

        item = self.scene.addPolygon(
            poly,
            QPen(QColor("#3e6ac1")),
            QBrush(QColor("#3e6ac1"))
        )

        rotations = {
            "ESTE": 0,
            "SUR": 90,
            "OESTE": 180,
            "NORTE": 270
        }

        item.setTransformOriginPoint(centerX, centerY)
        item.setRotation(rotations.get(self.world.karel.direction, 0))

    def world_to_scene(self, x, y):
        sx = (x - 1) * self.CELL_SIZE
        sy = (self.world.height - y) * self.CELL_SIZE

        return sx, sy

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scale(1.15, 1.15)
        else:
            self.scale(0.85, 0.85)

    def draw_evaluator(self):
        brush = QBrush(QColor(255, 255, 0, 80))

        pen = Qt.NoPen

        for x, y in self.world.eval_cells:
            sx, sy = self.world_to_scene(x, y)

            self.scene.addRect(
                sx,
                sy,
                self.CELL_SIZE,
                self.CELL_SIZE,
                pen,
                brush
            )

if __name__ == "__main__":

    app = QApplication([])

    world = loadWorld("worldFiles/mundo.in")

    view = WorldView(world)

    view.resize(1200, 800)
    view.show()

    app.exec()
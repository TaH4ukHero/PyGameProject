# import pygame
# import pygame_menu as pgm
# import pygame.freetype
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QApplication


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class Menu(QWidget):
    def __init__(self):
        super(Menu, self).__init__()
        self.initUi()

    def initUi(self):
        self.setGeometry(300,300, 961, 640)
        self.px = QPixmap('maps/Screenshot_3.png')
        self.lbl = QLabel(self)
        self.lbl.resize(QSize(961, 640))
        self.lbl.move(0, 0)
        self.lbl.setPixmap(self.px)


# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# font = pgm.font.get_font('maps/PeaberryDoublespace.ttf', 40)
# myimage = pgm.baseimage.BaseImage(
#     image_path='maps/Screenshot_3.png',
#     drawing_mode=pgm.baseimage.IMAGE_MODE_FILL
# )
# my_theme = pgm.Theme(widget_font=font, widget_font_color=pygame.Color(113, 170, 52),
#                      title_bar_style=pgm.widgets.MENUBAR_STYLE_NONE,
#                      title_font_color=pygame.Color(113, 170, 52), title_font_size=50,
#                      selection_color=pygame.Color(52, 85, 81))
# my_theme.background_color = myimage
# menu = pgm.Menu('', 800, 600, theme=my_theme)
# menu.add.button('Play', None)
# menu.add.button('Quit', None)
# menu.add.text_input('Nickname : ', default='Player1', maxchar=11)
# items = [('First',), ('Third',), ('Second',)]
# menu.add.button('First', None, align=pgm.locals.ALIGN_CENTER)
# menu.add.button('Second', None, align=pgm.locals.ALIGN_CENTER)
# menu.add.button('Third', None, align=pgm.locals.ALIGN_CENTER)
# menu.mainloop(screen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

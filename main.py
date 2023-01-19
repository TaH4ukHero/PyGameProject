import pygame
import pygame_menu as pgm
import pygame.freetype

CURRENT_BTN = 0


# # import sys
# #
# # from PyQt5.QtCore import QSize
# # from PyQt5.QtGui import QPixmap
# # from PyQt5.QtWidgets import QWidget, QLabel, QApplication
#
#
# # def except_hook(cls, exception, traceback):
# #     sys.__excepthook__(cls, exception, traceback)
# #
# #
# # class Menu(QWidget):
# #     def __init__(self):
# #         super(Menu, self).__init__()
# #         self.initUi()
# #
# #     def initUi(self):
# #         self.setGeometry(300,300, 961, 640)
# #         self.px = QPixmap('maps/Screenshot_3.png')
# #         self.lbl = QLabel(self)
# #         self.lbl.resize(QSize(961, 640))
# #         self.lbl.move(0, 0)
# #         self.lbl.setPixmap(self.px)
# #
#
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# font = pgm.font.get_font('maps/PeaberryDoublespace.ttf', 40)
# my_theme = pgm.Theme(widget_font=font, widget_font_color=pygame.Color(113, 170, 52),
#                      title_bar_style=pgm.widgets.MENUBAR_STYLE_NONE,
#                      title_font_color=pygame.Color(113, 170, 52), title_font_size=50,
#                      selection_color=pygame.Color(52, 85, 81))
# my_theme.background_color = pygame.Color(223,246,245)
# menu = pgm.Menu('', 800, 600, theme=my_theme)
# menu.add.button('Play', None)
# menu.add.text_input('Nickname : ', default='Player1', maxchar=11)
# items = [('First',), ('Third',), ('Second',)]
# menu.add.button('First', None, align=pgm.locals.ALIGN_CENTER)
# menu.add.button('Second', None, align=pgm.locals.ALIGN_CENTER)
# menu.add.button('Third', None, align=pgm.locals.ALIGN_CENTER)
# menu.add.button('Quit', None)
# menu.mainloop(screen)


class Menu(pygame.sprite.Sprite):
    def __init__(self, mode, pos):
        self.surf = pygame.Surface((200, 50))
        self.rect = self.surf.get_rect()
        self.pos = pos
        self.rect.x, self.rect.y = self.pos
        super().__init__()
        self.mode = mode
        self.setup()
        self.update()

    def setup(self):
        self.image = pygame.transform.scale(pygame.image.load(f'maps/{self.mode}_unactive.png'), (200, 50))
        self.image.set_colorkey((255, 255, 255))

    def update(self):
        global CURRENT_BTN
        if CURRENT_BTN % 2 == 1 and self.mode == 'Quit':
            self.image = pygame.transform.scale(pygame.image.load(f'maps/{self.mode}_active.png'), (200, 50))
            self.image.set_colorkey((255, 255, 255))
        if CURRENT_BTN % 2 == 0 and self.mode == 'Start':
            self.image = pygame.transform.scale(pygame.image.load(f'maps/{self.mode}_active.png'), (200, 50))
            self.image.set_colorkey((255, 255, 255))
        else:
            self.image = pygame.transform.scale(pygame.image.load(f'maps/{self.mode}_unactive.png'), (200, 50))
            self.image.set_colorkey((255, 255, 255))


buttons = pygame.sprite.Group()
start_btn = Menu('Start', (300, 100))
quit_btn = Menu('Quit', (300, 200))
buttons.add(start_btn)
buttons.add(quit_btn)


def main():
    global CURRENT_BTN
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    CURRENT_BTN += 1
                    buttons.update()
        screen.fill(pygame.Color(223, 246, 245))
        buttons.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()

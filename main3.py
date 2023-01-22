import sys

import pygame as pg
import pytmx


class Map:
    def __init__(self):
        self.map = pytmx.load_pygame('maps/second.tmx')

    def render(self,screen):
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x,y,0)
                if image is not None:
                    image = pg.transform.scale(image, (32,32))
                    screen.blit(image, (x*32, y*32))
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x,y,1)
                if image is not None:
                    image = pg.transform.scale(image, (32,32))
                    screen.blit(image, (x*32, y*32))
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x,y,2)
                if image is not None:
                    image = pg.transform.scale(image, (32,32))
                    screen.blit(image, (x*32, y*32))

def main():
    pg.init()
    screen = pg.display.set_mode((40*32, 20*32))
    mp = Map()
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill(pg.Color('black'))
        mp.render(screen)
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
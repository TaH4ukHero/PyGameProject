import sys

import pygame
import pytmx

from CONSTANTS import *
from EVENTS import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")

vec = pygame.math.Vector2
Clock = pygame.time.Clock()
ACTIVATION_END = False
GAME_OVER = False
AVAILABLE_FINISH = False


class Game_Over:
    def __init__(self, score, mode):
        self.mode = mode


class Mechanism(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Mechanism, self).__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.image = pygame.transform.scale(pygame.image.load(
            'maps/kenney_pixelPlatformer/Tiles/tile_0064.png'), (TILE_SIZE, TILE_SIZE))

    def activation(self):
        global ACTIVATION_END
        cooperation = pygame.sprite.spritecollide(self, game.player, False)
        if cooperation:
            self.image = pygame.transform.scale(pygame.image.load(
                'maps/kenney_pixelPlatformer/Tiles/tile_0066.png'), (TILE_SIZE, TILE_SIZE))
            ACTIVATION_END = True


class Ledder(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Ledder, self).__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.image = pygame.transform.scale(pygame.image.load(
            'maps/kenney_pixelPlatformer/Tiles/tile_0071.png'), (TILE_SIZE, TILE_SIZE))


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, pos, mode=None):
        super(AnimatedSprite, self).__init__()
        self.mode = mode
        self.images = ('maps/kenney_pixelPlatformer/Tiles/tile_0033.png',
                       'maps/kenney_pixelPlatformer/Tiles/tile_0053.png')
        self.images_coins = ('maps/kenney_pixelPlatformer/Tiles/tile_0151.png',
                             'maps/kenney_pixelPlatformer/Tiles/tile_0152.png')

        self.images_flags = ('maps/kenney_pixelPlatformer/Tiles/tile_0111.png',
                             'maps/kenney_pixelPlatformer/Tiles/tile_0112.png')
        self.cur_img = 1
        if mode and mode != 'Finish':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_coins[(self.cur_img + 1)
                                                    % 2]), [TILE_SIZE, TILE_SIZE])
        elif mode == 'Finish':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_flags[(self.cur_img + 1)
                                                    % 2]), [TILE_SIZE, TILE_SIZE])
        else:
            self.image = pygame.transform.scale(pygame.image.load(self.images[(self.cur_img + 1) %
                                                                              2]),
                                                [TILE_SIZE, TILE_SIZE])
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE

    def update(self):
        if self.mode and self.mode != 'Finish':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_coins[(self.cur_img + 1)
                                                    % 2]), [TILE_SIZE, TILE_SIZE])
        elif self.mode == 'Finish':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_flags[(self.cur_img + 1)
                                                    % 2]), [TILE_SIZE, TILE_SIZE])

        else:
            self.image = pygame.transform.scale(pygame.image.load
                                                (self.images[(self.cur_img + 1) % 2])
                                                , [TILE_SIZE, TILE_SIZE])
        self.cur_img += 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, end):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.pos = pos
        self.start = pos[0]
        self.end = end
        self.cur_img = 5
        self.first_step = True

        if self.start > self.end:
            self.cur_direction = 'left'
            self.image = pygame.transform.scale(pygame.image.load(
                'maps/kenney_pixelPlatformer/Characters/character_0024_left.png'),
                (TILE_SIZE, TILE_SIZE))
        else:
            self.cur_direction = 'right'
            self.image = pygame.transform.scale(pygame.image.load(
                'maps/kenney_pixelPlatformer/Characters/character_0024_right.png'),
                (TILE_SIZE, TILE_SIZE))

        self.images_left = ('maps/kenney_pixelPlatformer/Characters/character_0024_left.png',
                            'maps/kenney_pixelPlatformer/Characters/character_0027_left.png',
                            'maps/kenney_pixelPlatformer/Characters/character_0025_left.png',
                            'maps/kenney_pixelPlatformer/Characters/character_0028_left.png',
                            'maps/kenney_pixelPlatformer/Characters/character_0026_left.png')

        self.images_right = ('maps/kenney_pixelPlatformer/Characters/character_0024_right.png',
                             'maps/kenney_pixelPlatformer/Characters/character_0027_right.png',
                             'maps/kenney_pixelPlatformer/Characters/character_0025_right.png',
                             'maps/kenney_pixelPlatformer/Characters/character_0028_right.png',
                             'maps/kenney_pixelPlatformer/Characters/character_0026_right.png')

    def update(self):
        if self.first_step:
            self.next_step()
            self.first_step = False
        elif self.pos[0] == self.start or self.pos[0] == self.end:
            self.switch_direction()
            self.next_step()
        else:
            self.next_step()
        self.rect.x, self.rect.y = self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE

    def next_step(self):
        if self.cur_direction == 'left':
            self.pos[0] -= 1
        elif self.cur_direction == 'right':
            self.pos[0] += 1

    def switch_direction(self):
        if self.cur_direction == 'left':
            self.cur_direction = 'right'
        else:
            self.cur_direction = 'left'

    def change_img(self):
        if self.cur_direction == 'left':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_left[(self.cur_img + 1) %
                                                   5]), [TILE_SIZE, TILE_SIZE])
        elif self.cur_direction == 'right':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_right[(self.cur_img + 1)
                                                    % 5]), [TILE_SIZE,
                                                            TILE_SIZE])
        self.cur_img += 1


class HealthPoint(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(HealthPoint, self).__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.is_alive = True
        self.image = pygame.transform.scale(pygame.image.load(
            'maps/kenney_pixelPlatformer/Tiles/tile_0044.png'), (TILE_SIZE, TILE_SIZE))

    def death(self):
        self.is_alive = False
        self.image = pygame.transform.scale(pygame.image.load(
            'maps/kenney_pixelPlatformer/Tiles/tile_0046.png'), (TILE_SIZE, TILE_SIZE))


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, jump):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE

        self.start_pos = (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)
        self.pos = vec((pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

        self.score = 0

        self.image = pygame.image.load(
            'maps/kenney_pixelPlatformer/Characters/character_0000_right.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.images_left = ('maps/kenney_pixelPlatformer/Characters/character_0000_left.png',
                            'maps/kenney_pixelPlatformer/Characters/character_0001_left.png')
        self.images_right = ('maps/kenney_pixelPlatformer/Characters/character_0000_right.png',
                             'maps/kenney_pixelPlatformer/Characters/character_0001_right.png')
        self.cur_img = 1
        self.direction = 'right'
        self.jump_height = jump

    def move(self):
        self.acceleration = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acceleration.x = -ACCELERATION
            self.direction = 'left'
        if pressed_keys[K_RIGHT]:
            self.acceleration.x = ACCELERATION
            self.direction = 'right'
        if pressed_keys[K_UP] and pygame.sprite.spritecollideany(self, game.ledders):
            self.velocity.y = -5
        if pressed_keys[K_DOWN] and pygame.sprite.spritecollideany(self, game.ledders):
            self.pos.y -= 1
            self.velocity.y = 5

        self.acceleration.x += self.velocity.x * FRICTION
        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration

        if self.pos.x > WINDOW_WIDTH:
            self.pos.x = WINDOW_WIDTH - self.rect.width // 2
        if self.pos.x < 0:
            self.pos.x = 0 + self.rect.width // 2

        self.rect.midbottom = self.pos

    def update(self):
        global GAME_OVER, AVAILABLE_FINISH
        hits = pygame.sprite.spritecollide(self, game.platforms, False)
        k = 0
        if self.velocity.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.velocity.y = 0
        if pygame.sprite.spritecollideany(self, game.traps) or \
                pygame.sprite.spritecollideany(self, game.enemys):
            for i in game.hp.sprites():
                if i.is_alive:
                    i.death()
                    break
            for i in game.hp.sprites():
                if i.is_alive:
                    k += 1
            if k == 0:
                GAME_OVER = True
                print('GAME OVER')
                return
            self.pos = self.start_pos
        if pygame.sprite.spritecollide(self, game.coins, True):
            game.score_count.score += 1
            game.score_count.update()
        if pygame.sprite.spritecollide(self, game.finish, False) and AVAILABLE_FINISH:
            GAME_OVER = True
            print('YOU WON')

    def jump(self):
        hits = pygame.sprite.spritecollide(self, game.platforms, False)
        if hits:
            self.velocity.y = -self.jump_height

    def change_img(self):
        if self.direction == 'left':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_left[(self.cur_img + 1) %
                                                   2]),
                (TILE_SIZE, TILE_SIZE))
        elif self.direction == 'right':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_right[(self.cur_img + 1) %
                                                    2]),
                (TILE_SIZE, TILE_SIZE))
        self.cur_img += 1


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


# class Map:
#     def __init__(self, filename):
#         super(Map, self).__init__()
#         self.map = pytmx.load_pygame(f'maps/{filename}')
#         self.secrets = []
#
#     def render(self):
#         for y in range(self.map.height):
#             for x in range(self.map.width):
#                 image = self.map.get_tile_image(x, y, 7)  # Secrets
#                 if image is not None:
#                     self.secrets.append([x, y])
#         for y in range(self.map.height):
#             for x in range(self.map.width):
#                 image = self.map.get_tile_image(x, y, 0)  # BG
#                 if image is not None:
#                     if y == WINDOW_HEIGHT // TILE_SIZE - 1:
#                         block = AnimatedSprite((x, y))
#                         animated_sprites.add(block)
#                     else:
#                         block = Tile((x, y), image)
#                         all_sprites.add(block)
#         for y in range(self.map.height):
#             for x in range(self.map.width):
#                 image = self.map.get_tile_image(x, y, 1)  # BG2
#                 if image is not None:
#                     block = Tile((x, y), image)
#                     if [x, y] in self.secrets:
#                         secrets.add(block)
#                     else:
#                         all_sprites.add(block)
#         for y in range(self.map.height):
#             for x in range(self.map.width):
#                 image = self.map.get_tile_image(x, y, 2)  # Platforms
#                 if image is not None:
#                     block = Tile((x, y), image)
#                     all_sprites.add(block)
#                     if [x, y] in self.secrets:
#                         secrets_platforms.add(block)
#                         platforms.add(block)
#                     else:
#                         platforms.add(block)
#         for y in range(self.map.height):
#             for x in range(self.map.width):
#                 image = self.map.get_tile_image(x, y, 3)  # Traps
#                 if image is not None:
#                     if y == WINDOW_HEIGHT // TILE_SIZE - 1:
#                         block = AnimatedSprite((x, y))
#                         animated_sprites.add(block)
#                         traps.add(block)
#                     else:
#                         block = Tile((x, y), image)
#                         traps.add(block)
#                         if [x, y] in self.secrets:
#                             secrets_traps.add(block)
#             for y in range(self.map.height):
#                 for x in range(self.map.width):
#                     image = self.map.get_tile_image(x, y, 5)  # Mechanisms
#                     if image is not None:
#                         block = Mechanism((x, y))
#                         mechanisms.add(block)
#                         all_sprites.add(block)
#             for y in range(self.map.height):
#                 for x in range(self.map.width):
#                     image = self.map.get_tile_image(x, y, 6)  # Ledders
#                     if image is not None:
#                         block = Ledder((x, y))
#                         ledders.add(block)
#                         all_sprites.add(block)
#             for y in range(self.map.height):
#                 for x in range(self.map.width):
#                     image = self.map.get_tile_image(x, y, 8)  # Coins
#                     if image is not None:
#                         coin = AnimatedSprite((x, y), True)
#                         coins.add(coin)
#             for y in range(self.map.height):
#                 for x in range(self.map.width):
#                     image = self.map.get_tile_image(x, y, 10)  # Finish
#                     if image is not None:
#                         flag = Tile([x, y], image)
#                         all_sprites.add(flag)
#                         finish.add(flag)


class Score(pygame.sprite.Sprite):
    def __init__(self, pos, mode=None):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.mode = mode
        self.score = 0
        if self.mode:
            self.image = pygame.transform.scale(pygame.image.load(
                'maps/kenney_pixelPlatformer/Tiles/tile_0158.png'), (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pygame.transform.scale(
                pygame.image.load('maps/kenney_pixelPlatformer/Tiles/tile_0160.png'), [TILE_SIZE,
                                                                                       TILE_SIZE])

    def update(self):
        images = ('maps/kenney_pixelPlatformer/Tiles/tile_0160.png',
                  'maps/kenney_pixelPlatformer/Tiles/tile_0161.png',
                  'maps/kenney_pixelPlatformer/Tiles/tile_0162.png',
                  'maps/kenney_pixelPlatformer/Tiles/tile_0163.png'
                  )

        if self.mode:
            self.image = pygame.transform.scale(pygame.image.load(
                'maps/kenney_pixelPlatformer/Tiles/tile_0158.png'), (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pygame.transform.scale(pygame.image.load(images[self.score]), [TILE_SIZE,
                                                                                        TILE_SIZE])


# platforms = pygame.sprite.Group()
# traps = pygame.sprite.Group()
# animated_sprites = pygame.sprite.Group()
# ledders = pygame.sprite.Group()
# coins = pygame.sprite.Group()
# mechanisms = pygame.sprite.Group()
# player = pygame.sprite.Group()
# secrets = pygame.sprite.Group()  # Платформы которые потом включатся
# secrets_traps = pygame.sprite.Group()  # Ловушки которые пропадут
# secrets_platforms = pygame.sprite.Group()  # Платформы которые потом выключатся
# scores = pygame.sprite.Group()
# finish = pygame.sprite.Group()
#
# score_coin = AnimatedSprite((6, 0), True)
# score_sign = Score((7, 0), True)
# score_count = Score((8, 0), False)
# scores.add(score_coin)
# scores.add(score_sign)
# scores.add(score_count)
# finish_flag = AnimatedSprite((40, 2), 'Finish')
# finish.add(finish_flag)

# all_sprites = pygame.sprite.Group()
# hp = pygame.sprite.Group()
# heart1 = HealthPoint((0, 0))
# heart2 = HealthPoint((1, 0))
# heart3 = HealthPoint((2, 0))
# hp.add(heart3)
# hp.add(heart2)
# hp.add(heart1)
# enemys = pygame.sprite.Group()


# pygame.time.set_timer(MOVING_HERO_EVENT, 240)
# pygame.time.set_timer(MOVING_ENEMY_EVENT, 180)
# pygame.time.set_timer(ANIMATED_SPRITE, 360)
# pygame.time.set_timer(CHANGE_IMG_EVENT, 90)


class First_Level:
    def __init__(self):
        self.hero = [1, 16]
        self.finish_flag = (40, 2), 'Finish'
        self.enemys = ([2, 3, 12], [12, 4, 19], [18, 6, 24], [29, 8, 24], [24, 11, 18])
        self.map_name = 'second.tmx'
        self.jump_height = 12


class Second_Level:
    def __init__(self):
        self.hero = [1, 12]
        self.finish_flag = (42, 3), 'Finish'
        self.map_name = 'Third.tmx'
        self.jump_height = 12


class Artem_Level:
    def __init__(self):
        self.hero = [1, 16]
        self.finish_flag = (11, 8), 'Finish'
        self.map_name = 'Artem.tmx'
        self.enemys = [[13, 16, 16], [29, 8, 32], [36, 13, 39], [36, 4, 39]]
        self.jump_height = 11.5


# def activate_end():
#     global ACTIVATION_END, AVAILABLE_FINISH
#     for sprite in secrets:
#         platforms.add(sprite)
#         all_sprites.add(sprite)
#     for sprite in secrets_platforms:
#         platforms.remove(sprite)
#     for sprite in secrets_traps:
#         traps.remove(sprite)
#     ACTIVATION_END = False
#     AVAILABLE_FINISH = True


class Game:
    pygame.time.set_timer(MOVING_HERO_EVENT, 240)
    pygame.time.set_timer(MOVING_ENEMY_EVENT, 180)
    pygame.time.set_timer(ANIMATED_SPRITE, 360)
    pygame.time.set_timer(CHANGE_IMG_EVENT, 45)  # Таймер смены изображения у птиц

    def __init__(self):
        self.enemys = pygame.sprite.Group()
        self.hp = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.animated_sprites = pygame.sprite.Group()
        self.ledders = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.mechanisms = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.secrets = pygame.sprite.Group()  # Платформы которые потом включатся
        self.secrets_traps = pygame.sprite.Group()  # Ловушки которые пропадут
        self.secrets_platforms = pygame.sprite.Group()  # Платформы которые потом выключатся
        self.secrets_bg = pygame.sprite.Group()  # Элементы фона которые потом включатся
        self.secrets_ledders = pygame.sprite.Group()  # Лестницы которые должны появится
        self.scores = pygame.sprite.Group()
        self.finish = pygame.sprite.Group()
        self.sprites_groups = [self.all_sprites, self.animated_sprites, self.traps, self.enemys,
                               self.coins, self.scores, self.hp, self.player]
        self.first_level = First_Level()
        self.Artem_level = Artem_Level()
        self.second_level = Second_Level()
        self.setup_level(self.Artem_level)
        self.setup_base_of_game()
        self.cur_lvl = self.Artem_level.map_name

    def setup_base_of_game(self):
        hps = ([2, 0], [1, 0], [0, 0])
        for i in hps:
            self.hp.add(HealthPoint(i))
        self.score_coin = AnimatedSprite((6, 0), True)
        self.score_sign = Score((7, 0), True)
        self.score_count = Score((8, 0), False)
        self.scores.add(self.score_coin)
        self.scores.add(self.score_sign)
        self.scores.add(self.score_count)

    def setup_level(self, level):
        self.hero = Player(level.hero, level.jump_height)
        self.player.add(self.hero)
        for i in level.enemys:
            self.enemys.add(Enemy(([i[0], i[1]]), i[2]))
        self.finish_flag = AnimatedSprite(level.finish_flag[0], 'Finish')
        self.finish.add(self.finish_flag)
        self.animated_sprites.add(self.finish_flag)
        self.render_level(level.map_name)
        self.all_sprites.add(self.hero)

    def setup_second_level(self):
        global AVAILABLE_FINISH
        AVAILABLE_FINISH = True
        self.hero = Player(self.second_level.hero, 12)
        self.player.add(self.hero)
        self.finish_flag = AnimatedSprite(self.second_level.finish_flag[0],
                                          self.second_level.finish_flag[1])
        self.finish.add(self.finish_flag)
        self.animated_sprites.add(self.finish_flag)
        self.render_level(self.second_level.map_name)
        self.all_sprites.add(self.hero)

    def setup_artem_level(self):
        self.hero = Player(self.Artem_level.hero, 11.5)
        self.player.add(self.hero)
        for i in self.Artem_level.enemys:
            self.enemys.add(Enemy(([i[0], i[1]]), i[2]))
        self.finish_flag = AnimatedSprite(self.first_level.finish_flag[0],
                                          self.first_level.finish_flag[1])
        self.finish_flag = AnimatedSprite(self.Artem_level.finish_flag[0],
                                          'Finish')
        self.finish.add(self.finish_flag)
        self.animated_sprites.add(self.finish_flag)
        self.render_level(self.Artem_level.map_name)
        self.all_sprites.add(self.hero)

    def render_level(self, level):
        self.map = pytmx.load_pygame(f'maps/{level}')
        self.secrets_places = []
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 7)  # Secrets
                if image is not None:
                    self.secrets_places.append([x, y])
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 0)  # BG
                if image is not None:
                    if y == WINDOW_HEIGHT // TILE_SIZE - 1 and level == self.first_level.map_name:
                        block = AnimatedSprite((x, y))
                        self.animated_sprites.add(block)
                    else:
                        block = Tile((x, y), image)
                        self.all_sprites.add(block)
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 1)  # BG2
                if image is not None:
                    block = Tile((x, y), image)
                    if [x, y] in self.secrets_places:
                        self.secrets.add(block)
                    else:
                        self.all_sprites.add(block)
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 2)  # Platforms
                if image is not None:
                    block = Tile((x, y), image)
                    self.all_sprites.add(block)
                    if [x, y] in self.secrets_places:
                        self.secrets_platforms.add(block)
                        self.platforms.add(block)
                    else:
                        self.platforms.add(block)
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 3)  # Traps
                if image is not None:
                    if y == WINDOW_HEIGHT // TILE_SIZE - 1 and level == self.first_level.map_name:
                        block = AnimatedSprite((x, y))
                        self.animated_sprites.add(block)
                        self.traps.add(block)
                    else:
                        block = Tile((x, y), image)
                        self.traps.add(block)
                        if [x, y] in self.secrets_places:
                            self.secrets_traps.add(block)
                            if self.second_level.map_name:
                                self.traps.remove(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 5)  # Mechanisms
                    if image is not None:
                        block = Mechanism((x, y))
                        self.mechanisms.add(block)
                        self.all_sprites.add(block)
            if level == self.second_level.map_name:
                for y in range(self.map.height):
                    for x in range(self.map.width):
                        image = self.map.get_tile_image(x, y, 4)  # Enemys
                        if image is not None:
                            block = Tile((x, y), image)
                            self.secrets_bg.add(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 6)  # Ledders
                    if image is not None:
                        block = Ledder((x, y))
                        self.ledders.add(block)
                        if not [x, y] in self.secrets_places:
                            self.all_sprites.add(block)
                        elif level == self.second_level.map_name:
                            self.secrets_ledders.add(block)
                            self.ledders.remove(block)
                        else:
                            self.secrets.add(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 8)  # Coins
                    if image is not None:
                        coin = AnimatedSprite((x, y), True)
                        self.coins.add(coin)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 10)  # Finish
                    if image is not None:
                        flag = Tile([x, y], image)
                        self.all_sprites.add(flag)
                        self.finish.add(flag)

    def new_game(self):
        for i in self.hp:
            i.is_alive = True

    def get_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.hero.jump()
            if event.key == pygame.K_e and pygame.sprite.spritecollide(self.hero, self.mechanisms,
                                                                       False):
                for i in self.mechanisms:
                    i.activation()
            if event.key == pygame.K_ESCAPE:
                self.new_game()
        if event.type == MOVING_HERO_EVENT:
            self.hero.change_img()
        if event.type == MOVING_ENEMY_EVENT:
            self.enemys.update()
            self.coins.update()
            self.scores.update()
        if event.type == ANIMATED_SPRITE:
            self.animated_sprites.update()
        if event.type == CHANGE_IMG_EVENT:
            for i in self.enemys:
                i.change_img()
        if ACTIVATION_END:
            self.activate_end()

    def activate_end(self):
        global ACTIVATION_END, AVAILABLE_FINISH
        for sprite in self.secrets:
            self.platforms.add(sprite)
            self.all_sprites.add(sprite)
        for sprite in self.secrets_platforms:
            self.platforms.remove(sprite)
            if self.cur_lvl == self.Artem_level.map_name:
                self.all_sprites.remove(sprite)
        if self.cur_lvl == self.second_level.map_name:
            for sprite in self.secrets_traps:
                self.traps.add(sprite)
        else:
            for sprite in self.secrets_traps:
                self.traps.remove(sprite)
        for sprite in self.secrets_bg:
            self.all_sprites.add(sprite)
        for sprite in self.secrets_ledders:
            self.all_sprites.add(sprite)
            self.ledders.add(sprite)
        ACTIVATION_END = False
        AVAILABLE_FINISH = True


# pygame.time.set_timer(MOVING_HERO_EVENT, 240)
# pygame.time.set_timer(MOVING_ENEMY_EVENT, 180)
# pygame.time.set_timer(ANIMATED_SPRITE, 360)
# pygame.time.set_timer(CHANGE_IMG_EVENT, 45)  # Таймер смены изображения у птиц
game = Game()
while True:
    for event in pygame.event.get():
        game.get_event(event)
    #     if event.type == QUIT:
    #         pygame.quit()
    #         sys.exit()
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_SPACE:
    #             first.hero.jump()
    #         if event.key == pygame.K_e and pygame.sprite.spritecollide(first.hero, mechanisms,
    #                                                                    False):
    #             for i in mechanisms:
    #                 i.activation()
    #         if event.key == pygame.K_ESCAPE:
    #             new_game()
    #     if event.type == MOVING_HERO_EVENT:
    #         first.hero.change_img()
    #     if event.type == MOVING_ENEMY_EVENT:
    #         enemys.update()
    #         coins.update()
    #         scores.update()
    #     if event.type == ANIMATED_SPRITE:
    #         animated_sprites.update()
    #     if event.type == CHANGE_IMG_EVENT:
    #         for i in enemys:
    #             i.change_img()
    # if ACTIVATION_END:
    #     activate_end()
    # first.hero.move()
    # all_sprites.update()
    # all_sprites.draw(screen)
    # animated_sprites.draw(screen)
    # traps.draw(screen)
    # enemys.draw(screen)
    # coins.draw(screen)
    # scores.draw(screen)
    # hp.draw(screen)
    game.hero.move()
    game.all_sprites.update()
    for i in game.sprites_groups:
        i.draw(screen)
    pygame.display.flip()
    Clock.tick(FPS)

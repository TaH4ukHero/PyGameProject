import sys

import pygame
import pygame_menu
import pytmx
from pygame.locals import *
from CONSTANTS import *

pygame.init()
flags = DOUBLEBUF
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags, 8)
pygame.display.set_caption("Average Platformer")
MOVING_HERO_EVENT = pygame.USEREVENT + 1
MOVING_ENEMY_EVENT = pygame.USEREVENT + 2
ANIMATED_SPRITE = pygame.USEREVENT + 3
CHANGE_IMG_EVENT = pygame.USEREVENT + 4

vec = pygame.math.Vector2
Clock = pygame.time.Clock()
ACTIVATION_END = False
GAME_OVER = False
AVAILABLE_FINISH = False
CURRENT_STATUS = 'Menu'
SETUP_SCREEN = False
CHOOSED_LEVEL = 'First'
FLAG = False
CURRENT_SCORE = 0


class GameOver:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        pygame.init()
        self.coin = AnimatedSprite((4.9, 4.6), 64, True)
        self.sprites.add(self.coin)
        self.btns = {'Back': ['active', 0], 'Restart': ['unactive', 1]}
        self.cur_btn = 0
        self.active_color = pygame.Color(182, 213, 60)
        self.unactive_color = pygame.Color(52, 85, 81)

    def draw(self, screen, score):
        pygame.font.init()
        font = pygame_menu.font.get_font('Font/PeaberryDoublespace.ttf', 64)
        screen.blit(pygame.transform.scale(pygame.image.load('Images/Screenshot_4.png'), (800, 600)),
                    (0, 0))
        text = font.render('GAME OVER', False, pygame.Color(182, 213, 60))
        x, y = 220, 80
        screen.blit(text, (x, y))
        text = font.render(f'x {score}', False, pygame.Color(182, 213, 60))
        x, y = 400, 300
        screen.blit(text, (x, y))
        x, y = 150, 200
        for key, val in self.btns.items():
            if val[0] == 'active':
                text = font.render(key, False, self.active_color)
            else:
                text = font.render(key, False, self.unactive_color)
            screen.blit(text, (x, y))
            x += 256
        self.sprites.draw(screen)

    def get_events(self, event):
        global CURRENT_STATUS, SETUP_SCREEN, FLAG
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        if event.type == ANIMATED_SPRITE:
            self.sprites.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.cur_btn -= 1
                if self.cur_btn == -1:
                    self.cur_btn = 1
                self.change_active(self.cur_btn)
            if event.key == pygame.K_LEFT:
                self.cur_btn += 1
                if self.cur_btn == 2:
                    self.cur_btn = 0
                self.change_active(self.cur_btn)
            if event.key == pygame.K_e and self.btns['Back'][0] == 'active':
                with open(f'logs/Last_Attempt_of_{CHOOSED_LEVEL}', 'w', encoding='utf8') as f:
                    f.write(f'Последняя попытка - {CURRENT_SCORE} монет.')
                CURRENT_STATUS = 'Menu'
                SETUP_SCREEN = False
                menu.cur_window = 0
                menu.cur_btn = 0
            if event.key == pygame.K_e and self.btns['Restart'][0] == 'active':
                with open(f'logs/Last_Attempt_of_{CHOOSED_LEVEL}', 'w', encoding='utf8') as f:
                    f.write(f'Последняя попытка - {CURRENT_SCORE} монет.')
                FLAG = True
                SETUP_SCREEN = False

    def change_active(self, cur_btn):
        for key, val in self.btns.items():
            if val[1] == cur_btn:
                self.btns[key][0] = 'active'
            else:
                self.btns[key][0] = 'unactive'


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
    def __init__(self, pos, tile_size, mode=None):
        super(AnimatedSprite, self).__init__()
        self.mode = mode
        self.tile_size = tile_size
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
                                                    % 2]), [self.tile_size, self.tile_size])
        elif mode == 'Finish':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_flags[(self.cur_img + 1)
                                                    % 2]), [self.tile_size, self.tile_size])
        else:
            self.image = pygame.transform.scale(pygame.image.load(self.images[(self.cur_img + 1) %
                                                                              2]),
                                                [self.tile_size, self.tile_size])
        self.surf = pygame.Surface((self.tile_size, self.tile_size))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * self.tile_size, pos[1] * self.tile_size

    def update(self):
        if self.mode and self.mode != 'Finish':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_coins[(self.cur_img + 1)
                                                    % 2]), [self.tile_size, self.tile_size])
        elif self.mode == 'Finish':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_flags[(self.cur_img + 1)
                                                    % 2]), [self.tile_size, self.tile_size])

        else:
            self.image = pygame.transform.scale(pygame.image.load
                                                (self.images[(self.cur_img + 1) % 2])
                                                , [self.tile_size, self.tile_size])
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

    def reborn(self):
        self.is_alive = True
        self.image = pygame.transform.scale(pygame.image.load(
            'maps/kenney_pixelPlatformer/Tiles/tile_0044.png'), (TILE_SIZE, TILE_SIZE))


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
        global GAME_OVER, AVAILABLE_FINISH, SETUP_SCREEN, CURRENT_STATUS
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
                self.end_game()
                return
            self.pos = self.start_pos
        if pygame.sprite.spritecollide(self, game.coins, True):
            game.score_count.score += 1
            game.score_count.update()
            self.score += 1
        if pygame.sprite.spritecollide(self, game.finish, False) and AVAILABLE_FINISH:
            GAME_OVER = True
            self.end_game()

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

    def end_game(self):
        global SETUP_SCREEN, CURRENT_STATUS, CURRENT_SCORE
        pygame.display.quit()
        CURRENT_STATUS = 'Game_Over'
        SETUP_SCREEN = False
        CURRENT_SCORE = self.score


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


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
            self.image = pygame.transform.scale(pygame.image.load(images[self.score]),
                                                [TILE_SIZE,
                                                 TILE_SIZE])


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


class Third_Level:
    def __init__(self):
        self.hero = [1, 16]
        self.finish_flag = (11, 8), 'Finish'
        self.map_name = 'Artem.tmx'
        self.enemys = [[13, 16, 16], [29, 8, 32], [36, 13, 39], [36, 4, 39]]
        self.jump_height = 11.5


def exit_from_game():
    pygame.display.quit()
    sys.exit()


class Menu:
    def __init__(self):
        self.active_color = pygame.Color(182, 213, 60)
        self.unactive_color = pygame.Color(52, 85, 81)
        self.bg_color = pygame.Color(223, 246, 245)
        self.btns_first_window = {'Start': ['active', 0, 50], 'Quit': ['unactive', 1, 70]}
        self.btns_second_window = {'First Lvl': ['active', 0],
                                   'Second Lvl': ['unactive', 1], 'Third Lvl': ['unactive', 2],
                                   'Back': ['unactive', 3, 70]}
        self.cur_btn = 0
        self.cur_window = 0

    def draw(self, screen):
        screen.fill(self.bg_color)
        font = pygame_menu.font.get_font('Font/PeaberryDoublespace.ttf', 50)
        if self.cur_window == 0:
            btns = self.btns_first_window
            x, y = 250, 200
        else:
            btns = self.btns_second_window
            x, y = 250, 100
        for key, val in btns.items():
            if val[0] == 'active':
                text = font.render(key, False, self.active_color)
            else:
                text = font.render(key, False, self.unactive_color)
            x += val[-1]
            screen.blit(text, (x, y))
            y += 100
            x = 250

    def change_active(self, cur_btn):
        if self.cur_window == 0:
            btns = self.btns_first_window
        else:
            btns = self.btns_second_window
        for key, val in btns.items():
            if val[1] == cur_btn:
                btns[key][0] = 'active'
            else:
                btns[key][0] = 'unactive'

    def get_events(self, event):
        global CURRENT_STATUS, SETUP_SCREEN, CHOOSED_LEVEL, FLAG
        if event.type == pygame.QUIT:
            exit_from_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.cur_btn -= 1
                if self.cur_window == 0:
                    if self.cur_btn == -1:
                        self.cur_btn = 1
                elif self.cur_window == 1:
                    if self.cur_btn == -1:
                        self.cur_btn = 3
                self.change_active(self.cur_btn)
            if event.key == pygame.K_DOWN:
                self.cur_btn += 1
                if self.cur_window == 0:
                    if self.cur_btn == 2:
                        self.cur_btn = 0
                elif self.cur_window == 1:
                    if self.cur_btn == 4:
                        self.cur_btn = 0
                self.change_active(self.cur_btn)
            if event.key == pygame.K_e:
                if self.cur_window == 0:
                    if self.btns_first_window['Start'][0] == 'active':
                        self.cur_window = 1
                    else:
                        exit_from_game()
                else:
                    if self.btns_second_window['Back'][0] == 'active':
                        self.cur_window = 0
                        self.cur_btn = 0
            if event.key == pygame.K_f and self.cur_window == 1:
                for key, val in self.btns_second_window.items():
                    if val[0] == 'active' and key != 'Back':
                        CHOOSED_LEVEL = f'{key.strip(" Lvl")}'
                        FLAG = True
                        SETUP_SCREEN = False
                        break


class Game:
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
        self.all_groups = [self.enemys, self.hp, self.all_sprites, self.platforms, self.traps,
                           self.animated_sprites, self.ledders, self.coins, self.mechanisms,
                           self.player, self.secrets, self.secrets_traps, self.secrets_platforms,
                           self.secrets_bg, self.secrets_ledders, self.scores, self.finish]

    def setup_game(self, level):
        for i in self.all_groups:
            i.empty()
        self.setup_level(level)
        self.setup_base_of_game()

    def setup_base_of_game(self):
        hps = ([2, 0], [1, 0], [0, 0])
        for i in hps:
            self.hp.add(HealthPoint(i))
        self.score_coin = AnimatedSprite((6, 0), 32, True)
        self.score_sign = Score((7, 0), True)
        self.score_count = Score((8, 0), False)
        self.scores.add(self.score_coin)
        self.scores.add(self.score_sign)
        self.scores.add(self.score_count)

    def setup_level(self, level):
        global AVAILABLE_FINISH
        self.cur_lvl = level
        if level == 'First':
            level = First_Level()
        elif level == 'Third':
            level = Third_Level()
        elif level == 'Second':
            AVAILABLE_FINISH = True
            level = Second_Level()
        self.hero = Player(level.hero, level.jump_height)
        self.player.add(self.hero)
        if self.cur_lvl != 'Second':
            for i in level.enemys:
                self.enemys.add(Enemy(([i[0], i[1]]), i[2]))
        self.finish_flag = AnimatedSprite(level.finish_flag[0], 32, 'Finish')
        self.finish.add(self.finish_flag)
        self.animated_sprites.add(self.finish_flag)
        self.render_level(level.map_name)
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
                    if y == WINDOW_HEIGHT // TILE_SIZE - 1 and self.cur_lvl == 'First':
                        block = AnimatedSprite((x, y), 32)
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
                    block = Tile((x, y), image.convert_alpha())
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
                    if y == WINDOW_HEIGHT // TILE_SIZE - 1 and self.cur_lvl == 'First':
                        block = AnimatedSprite((x, y), 32)
                        self.animated_sprites.add(block)
                        self.traps.add(block)
                    else:
                        block = Tile((x, y), image)
                        self.traps.add(block)
                        if [x, y] in self.secrets_places:
                            self.secrets_traps.add(block)
                            if self.cur_lvl == 'Second':
                                self.traps.remove(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 5)  # Mechanisms
                    if image is not None:
                        block = Mechanism((x, y))
                        self.mechanisms.add(block)
                        self.all_sprites.add(block)
            if self.cur_lvl == 'Second':
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
                        elif self.cur_lvl == 'Second':
                            self.secrets_ledders.add(block)
                            self.ledders.remove(block)
                        else:
                            self.secrets.add(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 8)  # Coins
                    if image is not None:
                        coin = AnimatedSprite((x, y), 32, True)
                        self.coins.add(coin)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 10)  # Finish
                    if image is not None:
                        flag = Tile([x, y], image)
                        self.all_sprites.add(flag)
                        self.finish.add(flag)

    def get_event(self, event):
        if event.type == QUIT:
            exit_from_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.hero.jump()
            if event.key == pygame.K_e and pygame.sprite.spritecollide(self.hero, self.mechanisms,
                                                                       False):
                for i in self.mechanisms:
                    i.activation()
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
            if self.cur_lvl == 'Third':
                self.all_sprites.remove(sprite)
        if self.cur_lvl == 'Second':
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


game = Game()
menu = Menu()
game_over = GameOver()


def set_timers():
    pygame.time.set_timer(MOVING_HERO_EVENT, 0)
    pygame.time.set_timer(MOVING_ENEMY_EVENT, 0)
    pygame.time.set_timer(ANIMATED_SPRITE, 0)
    pygame.time.set_timer(CHANGE_IMG_EVENT, 0)
    pygame.time.set_timer(MOVING_HERO_EVENT, 480)
    pygame.time.set_timer(MOVING_ENEMY_EVENT, 300)
    pygame.time.set_timer(ANIMATED_SPRITE, 200)
    pygame.time.set_timer(CHANGE_IMG_EVENT, 45)  # Таймер смены изображения у птиц


while 1:
    if not SETUP_SCREEN:
        if FLAG:
            pygame.display.quit()
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags, 8)
            screen.set_alpha(True)
            pygame.display.set_caption('Average Platformer')
            SETUP_SCREEN = True
            set_timers()
            game.setup_game(CHOOSED_LEVEL)
            CURRENT_STATUS = 'Play'
            FLAG = False
        elif CURRENT_STATUS == 'Menu' or CURRENT_STATUS == 'Game_Over':
            pygame.display.quit()
            screen = pygame.display.set_mode((800, 600), flags, 8)
            pygame.display.set_caption('Average Platformer')
            set_timers()
            screen.set_alpha(True)
            SETUP_SCREEN = True
            if CURRENT_STATUS == 'Game_Over':
                game_over.score = CURRENT_SCORE
    for event in pygame.event.get():
        if CURRENT_STATUS == 'Play':
            game.get_event(event)
        elif CURRENT_STATUS == 'Menu':
            menu.get_events(event)
        elif CURRENT_STATUS == 'Game_Over':
            game_over.get_events(event)
    if CURRENT_STATUS == 'Play':
        game.hero.move()
        game.player.update()
        if CURRENT_STATUS != 'Game_Over':
            for i in game.sprites_groups:
                i.draw(screen)
        else:
            continue
    elif CURRENT_STATUS == 'Menu':
        menu.draw(screen)
    elif CURRENT_STATUS == 'Game_Over':
        game_over.draw(screen, CURRENT_SCORE)
        game_over.sprites.draw(screen)
    pygame.display.flip()
    Clock.tick(FPS)

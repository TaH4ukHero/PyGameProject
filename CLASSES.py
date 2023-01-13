import pygame
from CONSTANTS import *




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
        cooperation = pygame.sprite.spritecollide(self, player, False)
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
    def __init__(self, pos, mode=False):
        super(AnimatedSprite, self).__init__()
        self.mode = mode
        self.images = ('maps/kenney_pixelPlatformer/Tiles/tile_0033.png',
                       'maps/kenney_pixelPlatformer/Tiles/tile_0053.png')
        self.images_coins = ('maps/kenney_pixelPlatformer/Tiles/tile_0151.png',
                             'maps/kenney_pixelPlatformer/Tiles/tile_0152.png')
        self.cur_img = 1
        if mode:
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_coins[(self.cur_img + 1)
                                                    % 2]), [TILE_SIZE, TILE_SIZE])
        else:
            self.image = pygame.transform.scale(pygame.image.load(self.images[(self.cur_img + 1) %
                                                                              2]),
                                                [TILE_SIZE, TILE_SIZE])
        self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE

    def update(self):
        if self.mode:
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_coins[(self.cur_img + 1)
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
        self.cur_img = 3
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
                            'maps/kenney_pixelPlatformer/Characters/character_0025_left.png',
                            'maps/kenney_pixelPlatformer/Characters/character_0026_left.png')

        self.images_right = ('maps/kenney_pixelPlatformer/Characters/character_0024_right.png',
                             'maps/kenney_pixelPlatformer/Characters/character_0025_right.png',
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
                                                   3]), [TILE_SIZE, TILE_SIZE])
        elif self.cur_direction == 'right':
            self.image = pygame.transform.scale(
                pygame.image.load(self.images_right[(self.cur_img + 1)
                                                    % 3]), [TILE_SIZE,
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
    def __init__(self, pos):
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

    def new_game(self):
        heart1.is_alive = True
        heart2.is_alive = True
        heart3.is_alive = True
        self.pos = self.start_pos

    def move(self):
        self.acceleration = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acceleration.x = -ACCELERATION
            self.direction = 'left'
        if pressed_keys[K_RIGHT]:
            self.acceleration.x = ACCELERATION
            self.direction = 'right'
        if pressed_keys[K_UP] and pygame.sprite.spritecollideany(self, ledders):
            self.velocity.y = -5
        if pressed_keys[K_DOWN] and pygame.sprite.spritecollideany(self, ledders):
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
        global GAME_OVER
        hits = pygame.sprite.spritecollide(self, platforms, False)
        k = 0
        if self.velocity.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.velocity.y = 0
        if pygame.sprite.spritecollideany(self, traps) or \
                pygame.sprite.spritecollideany(self, enemys):
            for i in hp.sprites():
                if i.is_alive:
                    i.death()
                    break
            for i in hp.sprites():
                if i.is_alive:
                    k += 1
            if k == 0:
                GAME_OVER = True
                print('GAME OVER')
                return
            self.pos = self.start_pos
        if pygame.sprite.spritecollide(self, coins, True):
            self.score += 1

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.velocity.y = -12

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


class Map:
    def __init__(self, filename):
        super(Map, self).__init__()
        self.map = pytmx.load_pygame(f'maps/{filename}')
        self.secrets = []

    def render(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 7)  # Secrets
                if image is not None:
                    self.secrets.append([x, y])
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 0)  # BG
                if image is not None:
                    if y == WINDOW_HEIGHT // TILE_SIZE - 1:
                        block = AnimatedSprite((x, y))
                        animated_sprites.add(block)
                    else:
                        block = Tile((x, y), image)
                        all_sprites.add(block)
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 1)  # BG2
                if image is not None:
                    block = Tile((x, y), image)
                    if [x, y] in self.secrets:
                        secrets.add(block)
                    else:
                        all_sprites.add(block)
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 2)  # Platforms
                if image is not None:
                    block = Tile((x, y), image)
                    all_sprites.add(block)
                    if [x, y] in self.secrets:
                        secrets_platforms.add(block)
                        platforms.add(block)
                    else:
                        platforms.add(block)
        for y in range(self.map.height):
            for x in range(self.map.width):
                image = self.map.get_tile_image(x, y, 3)  # Traps
                if image is not None:
                    if y == WINDOW_HEIGHT // TILE_SIZE - 1:
                        block = AnimatedSprite((x, y))
                        animated_sprites.add(block)
                        traps.add(block)
                    else:
                        block = Tile((x, y), image)
                        traps.add(block)
                        if [x, y] in self.secrets:
                            secrets_traps.add(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 5)  # Mechanisms
                    if image is not None:
                        block = Mechanism((x, y))
                        mechanisms.add(block)
                        all_sprites.add(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 6)  # Ledders
                    if image is not None:
                        block = Ledder((x, y))
                        ledders.add(block)
                        all_sprites.add(block)
            for y in range(self.map.height):
                for x in range(self.map.width):
                    image = self.map.get_tile_image(x, y, 8)  # Coins
                    if image is not None:
                        coin = AnimatedSprite((x, y), True)
                        coins.add(coin)

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
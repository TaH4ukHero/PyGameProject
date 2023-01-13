import pygame

enemys = pygame.sprite.Group()
hp = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
traps = pygame.sprite.Group()
animated_sprites = pygame.sprite.Group()
ledders = pygame.sprite.Group()
coins = pygame.sprite.Group()
mechanisms = pygame.sprite.Group()
player = pygame.sprite.Group()
secrets = pygame.sprite.Group()  # Платформы которые потом включатся
secrets_traps = pygame.sprite.Group()  # Ловушки которые пропадут
secrets_platforms = pygame.sprite.Group()  # Платформы которые потом выключатся
scores = pygame.sprite.Group()
finish = pygame.sprite.Group()
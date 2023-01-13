import pygame
from Sprites_Groups import *
from CLASSES import *



heart1 = HealthPoint((0, 0))
heart2 = HealthPoint((1, 0))
heart3 = HealthPoint((2, 0))
score_coin = AnimatedSprite((6, 0), True)
score_sign = Score((7, 0), True)
score_count = Score((8, 0), False)
def setup():
    hp.add(heart3)
    hp.add(heart2)
    hp.add(heart1)
    scores.add(score_coin)
    scores.add(score_sign)
    scores.add(score_count)

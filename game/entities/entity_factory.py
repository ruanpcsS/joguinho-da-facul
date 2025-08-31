import pygame
import os
import random
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.bullet import Bullet


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=1.0):
        super().__init__()

        # Carregar sprites de explosão
        self.images = []
        for i in range(1, 4):
            try:
                img = pygame.image.load(os.path.join('assets', 'effects', f'explosion{i}.png')).convert_alpha()
                if scale != 1.0:
                    size = (int(img.get_width() * scale), int(img.get_height() * scale))
                    img = pygame.transform.scale(img, size)
                self.images.append(img)
            except:
                # Fallback
                surf = pygame.Surface((int(50 * scale), int(50 * scale)), pygame.SRCALPHA)
                color = (255, 200, 100, 200)
                pygame.draw.circle(surf, color, (surf.get_width() // 2, surf.get_height() // 2), surf.get_width() // 2)
                self.images.append(surf)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # ms

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class EntityFactory:
    def create_entity(self, entity_type, x, y, *args):
        if entity_type == "player":
            return Player(x, y)
        elif entity_type.startswith("enemy"):
            enemy_level = int(entity_type[-1]) if entity_type[-1].isdigit() else 1
            return Enemy(x, y, enemy_level)
        elif entity_type == "bullet":
            return Bullet(x, y)
        elif entity_type == "explosion":
            scale = args[0] if args else 1.0
            return Explosion(x, y, scale)
        else:
            raise ValueError(f"Tipo de entidade desconhecido: {entity_type}")
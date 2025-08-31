import pygame
import os
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, level=1):
        super().__init__()
        self.level = level

        # Carregar imagem baseada no nível
        if level == 1:
            self.image = self.load_image('enemies', 'enemy1.png', 0.5)
            self.points = 100
            self.speed_multiplier = 1.0
        elif level == 2:
            self.image = self.load_image('enemies', 'enemy2.png', 0.5)
            self.points = 200
            self.speed_multiplier = 1.2
        else:
            self.image = self.load_image('enemies', 'enemy3.png', 0.5)
            self.points = 300
            self.speed_multiplier = 1.5

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Velocidades aleatórias
        self.speedy = random.randrange(1, 4) * self.speed_multiplier
        self.speedx = random.randrange(-2, 2) * self.speed_multiplier

        # Mascaramento para colisões precisas
        self.mask = pygame.mask.from_surface(self.image)

    def load_image(self, folder, filename, scale=1):
        try:
            path = os.path.join('assets', folder, filename)
            image = pygame.image.load(path).convert_alpha()
            if scale != 1:
                size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, size)
            return image
        except:
            surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            color = [(255, 100, 100), (100, 255, 100), (100, 100, 255)][self.level - 1]
            pygame.draw.polygon(surf, color, [(20, 0), (0, 40), (40, 40)])
            return surf

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Se o inimigo sair da tela, reaparece no topo
        screen_width = self.get_screen_width()
        screen_height = self.get_screen_height()

        if (self.rect.top > screen_height + 10 or
                self.rect.left < -25 or
                self.rect.right > screen_width + 25):
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 4) * self.speed_multiplier
            self.speedx = random.randrange(-2, 2) * self.speed_multiplier

    def get_screen_width(self):
        return 800

    def get_screen_height(self):
        return 600
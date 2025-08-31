import pygame
import os


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = self.load_image('effects', 'bullet.png', 0.3)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

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
            surf = pygame.Surface((5, 15), pygame.SRCALPHA)
            pygame.draw.rect(surf, (0, 200, 255), surf.get_rect())
            return surf

    def update(self):
        self.rect.y += self.speedy
        # Remove a bala se ela sair da tela
        if self.rect.bottom < 0:
            self.kill()
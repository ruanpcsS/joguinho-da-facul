import pygame
import os
import random


class Background:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Carregar camadas de background
        self.bg_image = self.load_image('background', 'bg.png')
        self.stars_image = self.load_image('background', 'stars.png')
        self.nebula_image = self.load_image('background', 'nebula.png')

        # Configurações de parallax
        self.bg_y = 0
        self.stars_y = 0
        self.nebula_y = 0

        self.bg_speed = 1
        self.stars_speed = 2
        self.nebula_speed = 0.5

        # Estrelas adicionais para efeito de profundidade
        self.depth_stars = []
        for _ in range(100):
            star = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.5, 3.0),
                'brightness': random.randint(150, 255)
            }
            self.depth_stars.append(star)

    def load_image(self, folder, filename):
        try:
            path = os.path.join('assets', folder, filename)
            image = pygame.image.load(path).convert_alpha()
            # Redimensionar para caber na tela
            image = pygame.transform.scale(image, (self.width, self.height))
            return image
        except:
            surf = pygame.Surface((self.width, self.height))
            surf.fill((10, 10, 40))
            for _ in range(100):
                x, y = random.randint(0, self.width), random.randint(0, self.height)
                size = random.randint(1, 3)
                brightness = random.randint(100, 255)
                pygame.draw.circle(surf, (brightness, brightness, brightness), (x, y), size)
            return surf

    def update(self):
        # Movimento parallax
        self.bg_y = (self.bg_y + self.bg_speed) % self.height
        self.stars_y = (self.stars_y + self.stars_speed) % self.height
        self.nebula_y = (self.nebula_y + self.nebula_speed) % self.height

        # Atualizar estrelas de profundidade
        for star in self.depth_stars:
            star['y'] += star['speed']
            if star['y'] > self.height:
                star['y'] = 0
                star['x'] = random.randint(0, self.width)

    def render(self):
        # Renderizar camadas de parallax
        self.screen.blit(self.bg_image, (0, self.bg_y))
        self.screen.blit(self.bg_image, (0, self.bg_y - self.height))

        self.screen.blit(self.stars_image, (0, self.stars_y))
        self.screen.blit(self.stars_image, (0, self.stars_y - self.height))

        self.screen.blit(self.nebula_image, (0, self.nebula_y))
        self.screen.blit(self.nebula_image, (0, self.nebula_y - self.height))

        # Renderizar estrelas de profundidade
        for star in self.depth_stars:
            color = (star['brightness'], star['brightness'], star['brightness'])
            pygame.draw.circle(self.screen, color, (star['x'], star['y']), star['size'])
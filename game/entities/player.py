import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Carregar sprites
        self.ship_image = self.load_image('player', 'ship.png', 0.7)

        # Criar imagens de motor alternativas
        self.engine_images = [
            self.create_engine_surface(0.7, 1.0),
            self.create_engine_surface(0.7, 1.2)
        ]

        self.image = self.ship_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # Propriedades
        self.speed = 8
        self.health = 100
        self.shoot_delay = 200  # ms
        self.last_shot = pygame.time.get_ticks()
        self.engine_animation = 0
        self.engine_timer = 0

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
            surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.polygon(surf, (0, 255, 0), [(25, 0), (0, 50), (50, 50)])
            return surf

    def create_engine_surface(self, scale, intensity):
        surf = pygame.Surface((int(50 * scale), int(20 * scale)), pygame.SRCALPHA)
        for i in range(3):
            width = int(15 * intensity * (3 - i) / 3)
            height = int(20 * intensity * (3 - i) / 3)
            color = (255, 200, 100, 200 - i * 60)
            pygame.draw.ellipse(surf, color, (surf.get_width() / 2 - width / 2,
                                              surf.get_height() - height,
                                              width, height))
        return surf

    def update(self):
        keys = pygame.key.get_pressed()

        # Movimento
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        # Manter na tela
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.get_screen_width(), self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(self.get_screen_height(), self.rect.bottom)

        # Animação do motor
        self.engine_timer += 1
        if self.engine_timer >= 5:
            self.engine_timer = 0
            self.engine_animation = (self.engine_animation + 1) % len(self.engine_images)

            # Criar imagem composta (nave + motor)
            self.image = self.ship_image.copy()
            engine_img = self.engine_images[self.engine_animation]
            self.image.blit(engine_img, (self.image.get_width() / 2 - engine_img.get_width() / 2,
                                         self.image.get_height() - 5))

    def get_screen_width(self):
        return 800

    def get_screen_height(self):
        return 600

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            from game.entities.bullet import Bullet
            return Bullet(self.rect.centerx, self.rect.top)
        return None
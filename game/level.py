import pygame
import random
import os
from game.entities.entity_factory import EntityFactory
from game.background import Background


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.background = Background(screen)
        self.entity_factory = EntityFactory()

        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        # Criar jogador
        self.player = self.entity_factory.create_entity("player",
                                                        self.width // 2,
                                                        self.height - 100)
        self.all_sprites.add(self.player)

        # Configurações do nível
        self.score = 0
        self.level = 1
        self.enemy_spawn_timer = 0
        self.game_over = False

        # Fontes
        self.font = self.load_font('ui', 'font.ttf', 28)
        self.big_font = self.load_font('ui', 'font.ttf', 48)

        # Sons
        self.shoot_sound = self.load_sound('laser.wav')
        self.explosion_sound = self.load_sound('explosion.wav')

        # Spawn inicial de inimigos
        self.spawn_enemies(5)

    def load_font(self, folder, filename, size):
        try:
            path = os.path.join('assets', folder, filename)
            return pygame.font.Font(path, size)
        except:
            return pygame.font.Font(None, size)

    def load_sound(self, filename):
        try:
            path = os.path.join('assets', 'sounds', filename)
            return pygame.mixer.Sound(path)
        except:
            return None

    def spawn_enemies(self, count):
        enemy_types = ["enemy1", "enemy2", "enemy3"]
        for i in range(count):
            enemy_type = random.choice(enemy_types)
            enemy = self.entity_factory.create_entity(
                enemy_type,
                random.randrange(50, self.width - 50),
                random.randrange(-300, -50)
            )
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            if event.key == pygame.K_SPACE and not self.game_over:
                bullet = self.player.shoot()
                if bullet:
                    self.all_sprites.add(bullet)
                    self.bullets.add(bullet)
                    if self.shoot_sound:
                        self.shoot_sound.play()
        return None

    def update(self):
        if self.game_over:
            return "playing"

        # Atualizar background
        self.background.update()

        # Atualizar sprites
        self.all_sprites.update()

        # Spawn de inimigos
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= 60:  # Spawn a cada segundo
            self.enemy_spawn_timer = 0
            if len(self.enemies) < 10 + self.level:  # Limite de inimigos
                self.spawn_enemies(1)

        # Colisões: bala - inimigo
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                self.score += enemy.points
                # Criar explosão
                explosion = self.entity_factory.create_entity("explosion",
                                                              enemy.rect.centerx,
                                                              enemy.rect.centery)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)

                if self.explosion_sound:
                    self.explosion_sound.play()

        # Colisões: jogador - inimigo
        hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hits:
            self.player.health -= 10 * len(hits)
            if self.player.health <= 0:
                self.game_over = True
                # Explosão do jogador
                explosion = self.entity_factory.create_entity("explosion",
                                                              self.player.rect.centerx,
                                                              self.player.rect.centery,
                                                              2.0)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)
                if self.explosion_sound:
                    self.explosion_sound.play()

        # Level up
        if self.score >= self.level * 1000:
            self.level += 1

        return "playing"

    def render(self):
        # Renderizar fundo
        self.background.render()

        # Renderizar sprites
        self.all_sprites.draw(self.screen)

        # HUD
        self.render_hud()

        # Tela de game over
        if self.game_over:
            self.render_game_over()

    def render_hud(self):
        # Barra de saúde
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = 20

        # Fundo da barra
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (health_x, health_y, health_width, health_height))

        # Saúde atual
        health_percent = self.player.health / 100
        health_color = (
            int(255 * (1 - health_percent)),
            int(255 * health_percent),
            0
        )
        pygame.draw.rect(self.screen, health_color,
                         (health_x, health_y, health_width * health_percent, health_height))

        # Borda
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (health_x, health_y, health_width, health_height), 2)

        # Pontuação e nível
        score_text = self.font.render(f"⭐ Score: {self.score}", True, (255, 255, 255))
        level_text = self.font.render(f"🚀 Level: {self.level}", True, (255, 255, 255))

        self.screen.blit(score_text, (self.width - score_text.get_width() - 20, 20))
        self.screen.blit(level_text, (self.width - level_text.get_width() - 20, 60))

    def render_game_over(self):
        # Overlay escuro
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Texto de game over
        game_over_text = self.big_font.render("GAME OVER", True, (255, 50, 50))
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Press ESC to return to menu", True, (200, 200, 200))

        self.screen.blit(game_over_text,
                         (self.width // 2 - game_over_text.get_width() // 2,
                          self.height // 2 - 60))
        self.screen.blit(score_text,
                         (self.width // 2 - score_text.get_width() // 2,
                          self.height // 2))
        self.screen.blit(restart_text,
                         (self.width // 2 - restart_text.get_width() // 2,
                          self.height // 2 + 60))
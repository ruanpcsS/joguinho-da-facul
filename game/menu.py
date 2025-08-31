import pygame
import os
import random


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        # Carregar assets
        self.background = self.load_image('background', 'menu_bg.png')
        self.button_img = self.load_image('ui', 'button.png')
        self.font = self.load_font('ui', 'font.ttf', 36)
        self.title_font = self.load_font('ui', 'font.ttf', 72)

        # Estrelas de fundo
        self.stars = []
        for _ in range(50):
            self.stars.append([
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.randint(1, 3)
            ])

        # Opções do menu
        self.options = ["🚀 Iniciar Jogo", "🎮 Tutorial", "⭐ Créditos", "❌ Sair"]
        self.selected_option = 0

    def load_image(self, folder, filename):
        try:
            path = os.path.join('assets', folder, filename)
            image = pygame.image.load(path).convert_alpha()
            return image
        except:
            surf = pygame.Surface((200, 60))
            surf.fill((50, 50, 150))
            pygame.draw.rect(surf, (100, 100, 200), surf.get_rect(), 5)
            return surf

    def load_font(self, folder, filename, size):
        try:
            path = os.path.join('assets', folder, filename)
            return pygame.font.Font(path, size)
        except:
            return pygame.font.Font(None, size)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    return "start_game"
                elif self.selected_option == 3:
                    return "quit"
        return None

    def update(self):
        # Animar estrelas
        for star in self.stars:
            star[1] += star[2]  # Move star down
            if star[1] > self.height:
                star[0] = random.randint(0, self.width)
                star[1] = 0
                star[2] = random.randint(1, 3)

    def render(self):
        # Fundo
        self.screen.blit(self.background, (0, 0))

        # Estrelas
        for x, y, size in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size)

        # Título
        title = self.title_font.render("🌟 COSMIC DEFENDER", True, (255, 255, 255))
        title_shadow = self.title_font.render("🌟 COSMIC DEFENDER", True, (0, 100, 200))
        self.screen.blit(title_shadow, (self.width // 2 - title.get_width() // 2 + 3, 53))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

        # Opções do menu
        for i, option in enumerate(self.options):
            color = (255, 215, 0) if i == self.selected_option else (200, 200, 200)
            text = self.font.render(option, True, color)

            # Botão background
            button_rect = self.button_img.get_rect(center=(self.width // 2, 250 + i * 70))
            self.screen.blit(self.button_img, button_rect)

            # Texto do botão
            text_rect = text.get_rect(center=(self.width // 2, 250 + i * 70))
            self.screen.blit(text, text_rect)

        # Instruções
        instructions = self.font.render("Use ↑↓ para navegar e ENTER para selecionar",
                                        True, (180, 180, 180))
        self.screen.blit(instructions, (self.width // 2 - instructions.get_width() // 2, 500))
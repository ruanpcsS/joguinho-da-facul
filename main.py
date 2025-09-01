import pygame
import sys
import os
from game.menu import Menu
from game.level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Configurações da tela
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("🌟 Cosmic Defender - Space Shooter")

        # Ícone da janela
        try:
            icon = pygame.image.load(os.path.join('assets', 'images', 'player', 'ship.png'))

            pygame.display.set_icon(icon)
        except:
            pass

        # Estados do jogo
        self.states = {
            "menu": Menu(self.screen),
            "game": None
        }
        self.current_state = "menu"

        # Configurações
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            # Processar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle events based on current state
                if self.current_state == "menu":
                    result = self.states["menu"].handle_event(event)
                    if result == "start_game":
                        self.states["game"] = Level(self.screen)
                        self.current_state = "game"
                    elif result == "quit":
                        self.running = False

                elif self.current_state == "game":
                    result = self.states["game"].handle_event(event)
                    if result == "menu":
                        self.current_state = "menu"
                        self.states["game"] = None

            # Atualizar estado atual
            if self.current_state == "menu":
                self.states["menu"].update()
                self.states["menu"].render()

            elif self.current_state == "game":
                game_result = self.states["game"].update()
                self.states["game"].render()

                if game_result == "game_over":
                    self.current_state = "menu"
                    self.states["game"] = None

            # Atualizar display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
# Example file showing a circle moving on screen
import pygame
from string import ascii_lowercase
from compiler import Compiler
from prompt_toolkit.key_binding.bindings.scroll import scroll_one_line_down

# pygame setup
pygame.init()

SPEED = 10

BOX_SIZE = 50
TOTAL_BOXES = 13
WIDTH = BOX_SIZE * TOTAL_BOXES
HEIGHT = 500

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

font=pygame.font.SysFont(None,int(BOX_SIZE // 1.5))

class Button:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.surface = pygame.Surface((150, 50))
        self.text = font.render("Automate Run", True, (0, 0, 0))
        self.text_rect = self.text.get_rect(center=(self.surface.get_width()/2, self.surface.get_height()/2))
        self.rect = pygame.Rect(125, 125, 150, 50)

    def update(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.surface, (127, 255, 212), (1, 1, 148, 48))
        else:
            pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, 150, 50))
            pygame.draw.rect(self.surface, (255, 255, 255), (1, 1, 148, 48))
            pygame.draw.rect(self.surface, (0, 0, 0), (1, 1, 148, 1), 2)
            pygame.draw.rect(self.surface, (0, 100, 0), (1, 48, 148, 10), 2)

    def draw(self, screen):
        self.surface.blit(self.text, self.text_rect)
        screen.blit(self.surface, (self.rect.x, self.rect.y))


class Tape:
    def __init__(self, x, y):
        self.tape_length = 100
        self.tape = ['/' for _ in range(self.tape_length)]
        self.current_index = len(self.tape) // 2
        self.box_dimensions = (BOX_SIZE, BOX_SIZE)

    def draw(self, screen):
        # first draw the cursor

        window_center_rect = ((screen.get_width() / 2) - self.box_dimensions[0] / 2, (screen.get_height() / 2) - self.box_dimensions[1] / 2, self.box_dimensions[0], self.box_dimensions[1])

        for i in range(self.current_index + 1, len(self.tape)):
            current_box_rect = (window_center_rect[0] + (self.box_dimensions[0] * (i - self.current_index)), window_center_rect[1], self.box_dimensions[0], self.box_dimensions[1])
            pygame.draw.rect(screen, WHITE, current_box_rect, 1)
            text_img = font.render(self.tape[i], True, WHITE)
            box_rect = pygame.Rect(current_box_rect)
            rect = text_img.get_rect(center=box_rect.center)
            screen.blit(text_img, rect)

        for i in range(self.current_index - 1, -1, -1):
            current_box_rect = (window_center_rect[0] - (self.box_dimensions[0] * (self.current_index - i)), window_center_rect[1], self.box_dimensions[0], self.box_dimensions[1])
            pygame.draw.rect(screen, WHITE, current_box_rect, 1)
            text_img = font.render(self.tape[i], True, WHITE)
            box_rect = pygame.Rect(current_box_rect)
            rect = text_img.get_rect(center=box_rect.center)
            screen.blit(text_img, rect)


        pygame.draw.rect(screen, GREEN, window_center_rect,3)
        text_img = font.render(self.tape[self.current_index], True, WHITE)
        box_rect = pygame.Rect(window_center_rect)
        rect = text_img.get_rect(center=box_rect.center)
        screen.blit(text_img, rect)


    def move(self, direction):
        if self.current_index == 0 and direction == -1:
            return
        if self.current_index == len(self.tape) - 1 and direction == 1:
            return
        self.current_index += direction


class Game:
    def __init__(self):
        self.output = 'Output: '
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.compiler = Compiler()
        self.tape = Tape(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.button = Button()

        # Automated testing
        self.current_state = "START"
        self.compiler.compile("language.txt")
        self.is_automate = False

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.tape.move(-1)
                if event.key == pygame.K_RIGHT:
                    self.tape.move(1)
                if event.key == pygame.K_RETURN:
                    self.output += self.tape.tape[self.tape.current_index]

                key_name = pygame.key.name(event.key)
                if key_name in set(ascii_lowercase) or key_name == '/':
                    self.tape.tape[self.tape.current_index] = key_name

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button.rect.collidepoint(event.pos):
                    self.is_automate = not self.is_automate

    def update(self):
        self.button.update()

        if self.is_automate:
            if not self.current_state == "HALT":
                output_char, direction, next_state = self.compiler.update(self.current_state, self.tape.tape[self.tape.current_index])
                self.tape.tape[self.tape.current_index] = output_char
                if direction == 'l':
                    self.tape.move(-1)
                elif direction == 'r':
                    self.tape.move(1)
                self.current_state = next_state

    def draw(self):
        self.screen.fill("black")
        # Draw here
        output_img = font.render(self.output, True, WHITE)
        self.screen.blit(output_img, (0, HEIGHT - output_img.get_rect().height))
        self.tape.draw(self.screen)
        self.button.draw(self.screen)

        pygame.display.flip()
        self.dt = self.clock.tick(60) / 1000


if __name__ == "__main__":
    game = Game()
    game.run()

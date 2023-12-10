from network import Network
import time
import pygame
import numpy as np
from game_engine import Engine, Player
from network import Network
from typing import Union
from utils import *


class Button(pygame.Rect):
    def __init__(self, x: int,
                 y: int,
                 w: int,
                 h: int,
                 text: str,
                 coord: tuple[int, int],
                 text_color: tuple[int, int, int],
                 rect_color: tuple[int, int, int],
                 font: pygame.font.Font,
                 rect_width: int = 3):
        super().__init__(x, y, w, h)
        self.text = text
        self.rect_width = rect_width
        self.rect_color = rect_color
        self.text_color = text_color
        self.coord = coord
        self.font = font

    def draw(self, surf: pygame.Surface) -> None:
        """
        draw_game button on a surface
        :param surf: surface
        :return:
        """
        pygame.draw.rect(surf, self.rect_color, self, width=self.rect_width)
        text_centered(self.text, surf, self.font, self.text_color, self.centerx, self.centery)


class LocalState:

    def __init__(self,
                 w: int,
                 h: int,
                 player: Player,
                 engine: Engine,
                 network: Union[bool, Network] = False):

        pygame.init()

        self.WIN = pygame.display.set_mode((w, h))
        self.player = player
        self.w = w
        self.h = h
        self.buttons = []
        self.selected = []
        self.submitted_seq = []
        self.engine = engine
        self.network = network
        self.fonts = {'large': pygame.font.SysFont('Agency FB', 40),
                      'small': pygame.font.SysFont('Agency FB', 15)}
        self.colors = {'wht': (255, 255, 255),
                       'blk': (0, 0, 0),
                       'grn': (0, 255, 0),
                       'red': (255, 0, 0),
                       'blue': (0, 0, 255),
                       'yellow': (255, 255, 0)}

    def update(self) -> None:
        """
        submit sequence
        :return:
        """

        if not self.network:
            if len(self.submitted_seq) < 2:
                return
            self.engine.check_sequence(self.submitted_seq, self.player)
            self.submitted_seq.clear()

        else:
            # if len(self.submitted_seq) < 2:
            #     # self.network.send_obj([])
            #     pass
            # else:
            self.network.send_obj(self.submitted_seq)
            self.submitted_seq.clear()
            # data = self.network.receive()
            # if type(data) is dict:
            #     self.engine.status = data

    def submit_word(self, seq: list[tuple[int, int]]) -> None:
        """
        submit word to engine
        :param seq: integer pairs corresponding with coordinates
        :return:
        """
        self.submitted_seq = seq

    def make_buttons(self, grid: np.ndarray) -> None:
        """
        from grid of letters create buttons
        :param grid: grid of letters
        :return:
        """
        shape = grid.shape
        dw = 0.5 * self.w / (shape[0] + 1)
        dh = self.h / (shape[0] + 1)
        length = min((dw, dh))
        box_size = length * 0.9
        rect_width = 3
        self.buttons = []

        for i in range(shape[0]):
            for j in range(shape[1]):
                x = (j + 1) * length - box_size // 2
                y = (i + 1) * length - box_size // 2
                self.buttons.append(
                    Button(x,
                           y,
                           box_size,
                           box_size,
                           grid[i, j],
                           (i, j),
                           self.colors['blk'],
                           self.colors['blk'],
                           self.fonts['large']))

    def draw_game(self) -> None:
        """
        displays players on window surface
        :return:
        """
        guess_x = round(self.w * 0.55 + 20)
        guess_y = 50

        self.WIN.fill(self.colors['wht'])
        for button in self.buttons:
            button.draw(self.WIN)

        for button in self.selected:
            pygame.draw.circle(self.WIN,
                               self.colors['grn'],
                               button.center, 10)

        point_pairs = make_pairs([button.center for button in self.selected])
        for points in point_pairs:
            pygame.draw.line(self.WIN, self.colors['grn'], points[0], points[1], width=5)

        text_leftadj(self.make_text(),
                     self.WIN,
                     self.fonts['large'],
                     self.colors['blk'],
                     guess_x,
                     guess_y)

        text_leftadj(str(round(self.engine.status['time_left'], 1)),
                     self.WIN,
                     self.fonts['large'],
                     self.colors['blk'],
                     self.w - 100,
                     guess_y)

        names = [player for player in self.engine.status['players']]
        x_pos = np.linspace(guess_x,
                            self.w - 100,
                            len(names)).round()

        y_pos = [i for i in range(guess_y + self.fonts['large'].get_height()
                                  + 2 * self.fonts['small'].get_height(),
                                  self.h,
                                  self.fonts['small'].get_height())]

        for name in zip(names, x_pos):
            text_centered(name[0] + f" : {self.engine.status['players'][name[0]].score}",
                          self.WIN,
                          self.fonts['small'],
                          self.engine.status['players'][name[0]].color,
                          name[1],
                          100)

            for word in zip(self.engine.status['words'][name[0]], y_pos):
                text_centered(word[0] + f" : {self.engine.value_word(word[0])}",
                              self.WIN,
                              self.fonts['small'],
                              self.engine.status['players'][name[0]].color,
                              name[1],
                              word[1])

        pygame.display.update()

    def make_text(self) -> str:
        """
        determine text from buttons selected
        :return: word
        """
        return str().join([button.text for button in self.selected])

    def game_loop(self, engine: Engine):
        """
        game loop requiring a game engine
        :param engine: game engine
        :return:
        """
        # pygame.init()

        clock = pygame.time.Clock()
        fps = 60
        self.make_buttons(self.engine.status['grid'])
        # players = [Player('Logan', (200, 000, 000))]

        run = True

        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # quit if user quits
                    run = False
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        pos = pygame.mouse.get_pos()
                        buttons = [button for button in self.buttons if button.collidepoint(*pos)]
                        if len(buttons) == 1 and (
                                self.selected == [] or adj(buttons[-1].coord, self.selected[-1].coord)) and \
                                buttons[-1] not in self.selected:
                            self.selected.append(buttons[-1])
                    elif mouse[2]:
                        self.submit_word([button.coord for button in self.selected])
                        self.selected.clear()
                    # elif mouse[2]:
                    #     self.selected.clear()

            self.engine.update()
            self.update()
            self.draw_game()


def main() -> None:
    """
    game loop
    :return:
    """
    player = Player('Logan', (200, 0, 100))
    engine = Engine()
    engine.start(5, 20, [player])
    ls = LocalState(600, 600, player, engine)
    ls.game_loop(engine)


if __name__ == '__main__':
    main()

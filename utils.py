import pygame


def adj(first_tuple: tuple[int, int], second_tuple: tuple[int, int]) -> bool:
    """
    checks if two coordinates are adjacent
    :param first_tuple: first coordinate set
    :param second_tuple: second coordinate set
    :return: true or false based on coordinates
    """
    return abs(first_tuple[0] - second_tuple[0]) <= 1 and abs(first_tuple[1] - second_tuple[1]) <= 1


def make_pairs(mylist: list) -> list:
    """
    makes pairs out of list
    :param mylist: list
    :return: list of object pairs
    """
    return [x for x in zip(mylist[:-1], mylist[1:])]


def text_centered(text: str, surf: pygame.Surface, font: pygame.font.Font, color: tuple[int, int, int], x: int,
                  y: int) -> None:
    """
    blits text onto surface centered on x, y
    :param text: text to be displayed on the screen
    :param surf: surface to blit onto
    :param font: font to display the text
    :param color: color of font
    :param x: center x
    :param y: center y
    :return:
    """
    text_surface = font.render(text, True, color)
    xt = x - text_surface.get_width() / 2
    yt = y - text_surface.get_height() / 2
    surf.blit(text_surface, (xt, yt))


def text_leftadj(text: str, surf: pygame.Surface, font: pygame.font.Font, color: tuple[int, int, int], x: int,
                  y: int) -> None:
    """
    blits text onto surface centered on y, with x
    :param text: text to be displayed on the screen
    :param surf: surface to blit onto
    :param font: font to display the text
    :param color: color of font
    :param x: left x
    :param y: center y
    :return:
    """
    text_surface = font.render(text, True, color)
    yt = y - text_surface.get_height() / 2
    surf.blit(text_surface, (x, yt))
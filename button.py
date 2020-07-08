import pygame

pygame.init()

# Button attributes
button_width, button_height = (200, 50)
active_color = pygame.Color('dodgerblue1')
inactive_color = pygame.Color('dodgerblue4')
clicked_color = pygame.Color('darkblue')
text_color = (255, 255, 255)
font = pygame.font.Font(None, 42)

def create_button(x_pos, y_pos, text, callback):
    """Make button as a dictionary that stores all relevant data."""
    text_render = font.render(text, True, text_color)
    button_rect = pygame.Rect(x_pos, y_pos, button_width, button_height)
    text_rect = text_render.get_rect(center=button_rect.center)

    button = {
        'rect': button_rect,
        'text': text_render,
        'text rect': text_rect,
        'color': inactive_color,
        'callback': callback,
        }
    return button

def draw_button(button, screen):
    """Draw the button and text on screen."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])
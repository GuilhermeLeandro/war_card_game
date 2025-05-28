import pygame

def draw_linear_gradient_rect(surface, rect, color_start, color_end, vertical=True):

    target_rect = pygame.Rect(rect)
    if vertical:
        height = target_rect.height
        if height == 0: return # Evita divisão por zero
        for y in range(height):
            progress = y / height
            # Interpolação linear simples
            r = color_start[0] + (color_end[0] - color_start[0]) * progress
            g = color_start[1] + (color_end[1] - color_start[1]) * progress
            b = color_start[2] + (color_end[2] - color_start[2]) * progress
            color = (int(r), int(g), int(b))
            pygame.draw.line(surface, color, (target_rect.left, target_rect.top + y), (target_rect.right -1 , target_rect.top + y))
    else: # Horizontal
        width = target_rect.width
        if width == 0: return # Evita divisão por zero
        for x in range(width):
            progress = x / width
            r = color_start[0] + (color_end[0] - color_start[0]) * progress
            g = color_start[1] + (color_end[1] - color_start[1]) * progress
            b = color_start[2] + (color_end[2] - color_start[2]) * progress
            color = (int(r), int(g), int(b))
            pygame.draw.line(surface, color, (target_rect.left + x, target_rect.top), (target_rect.left + x, target_rect.bottom -1))
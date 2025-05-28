import pygame
import os
from models.card import Card as CardModel 
from . import constants as C
from . import card_graphics 

class Button:
    def __init__(self, x, y, width, height, text, 
                 font_object: pygame.font.Font, # Recebe o objeto Font já carregado
                 action=None,
                 color=C.BUTTON_DEFAULT_BG_NORMAL, 
                 hover_color=C.BUTTON_DEFAULT_BG_HOVER, 
                 disabled_color=C.BUTTON_DEFAULT_BG_DISABLED,
                 text_color=C.BUTTON_DEFAULT_TEXT_NORMAL, 
                 text_disabled_color=C.BUTTON_DEFAULT_TEXT_DISABLED,
                 border_radius=C.UI_BUTTON_BORDER_RADIUS,
                 border_color=None, 
                 border_width=0):   
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font_object 
        
        self.action = action
        self.color_normal = color
        self.color_hover = hover_color
        self.color_disabled = disabled_color
        self.text_color_normal = text_color
        self.text_color_disabled = text_disabled_color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        
        self.is_hovered = False
        self.is_enabled = True

    def handle_event(self, event):
        if not self.is_enabled:
            self.is_hovered = False
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered and self.action:
                self.action()
                return True 
        return False

    def draw(self, surface):
        current_bg_color = self.color_normal
        current_text_color = self.text_color_normal

        if not self.is_enabled:
            current_bg_color = self.color_disabled
            current_text_color = self.text_color_disabled
        elif self.is_hovered:
            current_bg_color = self.color_hover
        
        pygame.draw.rect(surface, current_bg_color, self.rect, border_radius=self.border_radius)
        
        if self.border_color and self.border_width > 0:
             pygame.draw.rect(surface, self.border_color, self.rect, self.border_width, border_radius=self.border_radius)

        text_surf = self.font.render(self.text, True, current_text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def set_enabled(self, enabled_status):
        self.is_enabled = enabled_status
        if not self.is_enabled:
            self.is_hovered = False

class VisualCard(pygame.sprite.Sprite):
    def __init__(self, card_str_or_model, x, y, is_face_up=True, owner=None):
        super().__init__() 
        if isinstance(card_str_or_model, CardModel):
            self.card_str = str(card_str_or_model)
        else:
            self.card_str = card_str_or_model if card_str_or_model else "UNKNOWN_CARD"

        self.owner = owner 
        self.is_face_up_logical = is_face_up 
        self.is_face_up_visual = is_face_up  
        
        self.image = card_graphics.get_card_surface(self.card_str if self.is_face_up_visual else "BACK")
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.target_pos = pygame.math.Vector2(x, y)
        self.current_pos = pygame.math.Vector2(x, y)
        self.is_moving = False
        self.move_speed = 1600 
        self.on_target_reached_callback = None

        self.is_flipping = False
        self.flip_progress = 0.0 
        self.flip_speed = 7.0  
        self.on_flip_done_callback = None
        self.is_collecting_to_winner = False 

    def set_target_pos(self, tx, ty, speed=None, on_reached=None):
        self.target_pos = pygame.math.Vector2(tx, ty)
        if speed is not None: self.move_speed = speed
        
        if (self.target_pos - self.current_pos).length_squared() > 1e-4: 
            self.is_moving = True
        else: 
            self.current_pos = self.target_pos 
            self.rect.topleft = (int(self.current_pos.x), int(self.current_pos.y))
            self.is_moving = False
            if on_reached: on_reached(self) 
        
        self.on_target_reached_callback = on_reached if self.is_moving else None


    def start_flip(self, to_face_up_status, on_flip_done=None):
        if self.is_face_up_visual == to_face_up_status and not self.is_flipping:
            if on_flip_done: on_flip_done(self) 
            return

        self.is_flipping = True
        self.is_face_up_logical = to_face_up_status 
        self.is_face_up_visual = not to_face_up_status if self.flip_progress == 0.0 else self.is_face_up_visual
        self.flip_progress = 0.0 
        self.on_flip_done_callback = on_flip_done
        
    def update(self, dt): 
        if self.is_moving:
            direction = self.target_pos - self.current_pos
            distance_sq = direction.length_squared()
            move_step_dist = self.move_speed * dt
            
            if distance_sq < (move_step_dist * move_step_dist) or distance_sq < 1.5*1.5: 
                self.current_pos.x, self.current_pos.y = self.target_pos.x, self.target_pos.y
                self.rect.topleft = (int(self.current_pos.x), int(self.current_pos.y))
                self.is_moving = False
                if self.on_target_reached_callback:
                    callback_to_call = self.on_target_reached_callback 
                    self.on_target_reached_callback = None 
                    callback_to_call(self)
            else:
                direction.normalize_ip(); movement = direction * move_step_dist
                if movement.length_squared() >= distance_sq: self.current_pos = self.target_pos
                else: self.current_pos += movement
                self.rect.topleft = (int(self.current_pos.x), int(self.current_pos.y))

        if self.is_flipping:
            self.flip_progress += self.flip_speed * dt
            if self.flip_progress >= 1.0:
                self.flip_progress = 1.0; self.is_flipping = False
                self.is_face_up_visual = self.is_face_up_logical 
                if self.on_flip_done_callback:
                    callback_to_call = self.on_flip_done_callback
                    self.on_flip_done_callback = None
                    callback_to_call(self)

            elif self.flip_progress >= 0.5 and self.is_face_up_visual != self.is_face_up_logical:
                self.is_face_up_visual = self.is_face_up_logical
        
        key_for_image = "BACK"
        if self.is_flipping:
            if self.flip_progress < 0.5: 
                key_for_image = self.card_str if not self.is_face_up_logical else "BACK" 
            else: 
                key_for_image = self.card_str if self.is_face_up_logical else "BACK"
        else:
            key_for_image = self.card_str if self.is_face_up_visual else "BACK"
        
        self.image = card_graphics.get_card_surface(key_for_image)

    def draw(self, surface): 
        image_to_render = self.image 
        current_scale_x = 1.0
        if self.is_flipping:
            current_scale_x = abs(1.0 - 2.0 * self.flip_progress) 
        
        if image_to_render: 
            original_width = image_to_render.get_width()
            original_height = image_to_render.get_height()
            scaled_width = int(original_width * current_scale_x)
            
            if scaled_width > 0: 
                if abs(current_scale_x - 1.0) < 1e-3 : 
                    scaled_image = image_to_render 
                else: 
                    scaled_image = pygame.transform.smoothscale(image_to_render, (scaled_width, original_height))
                
                draw_rect = scaled_image.get_rect(center=self.rect.center)
                surface.blit(scaled_image, draw_rect)
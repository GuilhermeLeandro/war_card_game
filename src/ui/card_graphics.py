# src/ui/card_graphics.py
import pygame
import os
from . import constants as C

_CARD_IMAGES_CACHE = {}
_CARD_BACK_IMAGE_CACHE = None

def _load_raw_image(filename):
    path = os.path.join(C.CARD_ASSETS_PATH, filename)
    if not os.path.exists(path):
        raise pygame.error(f"Arquivo de imagem não encontrado: {path}")
    return pygame.image.load(path).convert_alpha()

def _create_placeholder_surface(width, height, color, text_lines=None):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    pygame.draw.rect(surf, C.CARD_OUTLINE_COLOR, surf.get_rect(), 1)
    if text_lines:
        try:
            font = pygame.font.Font(None, 14)
            line_height = font.get_linesize()
            y_offset = (height - (len(text_lines) * line_height)) // 2
            for i, line in enumerate(text_lines):
                text_surf = font.render(line, True, C.BLACK)
                text_rect = text_surf.get_rect(centerx=width // 2, y=y_offset + i * line_height)
                surf.blit(text_surf, text_rect)
        except Exception: pass
    return surf

def preload_card_images():
    global _CARD_BACK_IMAGE_CACHE, _CARD_IMAGES_CACHE
    print("[CardGraphics] Pré-carregando imagens das cartas...")
    _CARD_IMAGES_CACHE.clear() 

    try:
        raw_back_img = _load_raw_image("card_back.png")
        _CARD_BACK_IMAGE_CACHE = pygame.transform.smoothscale(raw_back_img, (C.CARD_WIDTH, C.CARD_HEIGHT))
    except pygame.error:
        _CARD_BACK_IMAGE_CACHE = _create_placeholder_surface(C.CARD_WIDTH, C.CARD_HEIGHT, C.CARD_BACK_PLACEHOLDER_BG, ["VERSO"])
        print(f"Aviso CG: card_back.png não encontrado, usando placeholder.")

    suit_file_map = {"Copas": "hearts", "Ouros": "diamonds", "Paus": "clubs", "Espadas": "spades"}
    rank_file_map = {
        "Ás": "A", "Rei": "K", "Dama": "Q", "Valete": "J",
        "10": "10", "9": "09", "8": "08", "7": "07", "6": "06",
        "5": "05", "4": "04", "3": "03", "2": "02"
    }

    from models.card import Card as CardModel 

    loaded_count = 0
    for suit_model in CardModel.SUITS:
        for rank_model in CardModel.RANKS:
            card_str_key = f"{rank_model} de {suit_model}"
            if suit_model not in suit_file_map or rank_model not in rank_file_map:
                _CARD_IMAGES_CACHE[card_str_key] = _create_placeholder_surface(C.CARD_WIDTH, C.CARD_HEIGHT, C.CARD_PLACEHOLDER_BG, card_str_key.split(" de "))
                continue
            file_suit = suit_file_map[suit_model]
            file_rank = rank_file_map[rank_model]
            filename_rank_part = file_rank.upper() if file_rank.isalpha() else file_rank
            filename = f"card_{file_suit.lower()}_{filename_rank_part}.png"
            try:
                raw_img = _load_raw_image(filename)
                _CARD_IMAGES_CACHE[card_str_key] = pygame.transform.smoothscale(raw_img, (C.CARD_WIDTH, C.CARD_HEIGHT))
                loaded_count +=1
            except pygame.error:
                _CARD_IMAGES_CACHE[card_str_key] = _create_placeholder_surface(C.CARD_WIDTH, C.CARD_HEIGHT, C.CARD_PLACEHOLDER_BG, card_str_key.split(" de "))
    print(f"[CardGraphics] Pré-carregamento concluído. {loaded_count} faces de cartas encontradas e carregadas.")

def get_card_surface(card_identifier):
    if card_identifier == "BACK":
        if _CARD_BACK_IMAGE_CACHE is None: preload_card_images()
        return _CARD_BACK_IMAGE_CACHE if _CARD_BACK_IMAGE_CACHE else _create_placeholder_surface(C.CARD_WIDTH, C.CARD_HEIGHT, C.CARD_BACK_PLACEHOLDER_BG, ["VERSO"])
    if not _CARD_IMAGES_CACHE : preload_card_images()
    return _CARD_IMAGES_CACHE.get(card_identifier, 
                                  _create_placeholder_surface(C.CARD_WIDTH, C.CARD_HEIGHT, C.CARD_PLACEHOLDER_BG, 
                                                              card_identifier.split(" de ") if isinstance(card_identifier, str) else ["ERRO"]))
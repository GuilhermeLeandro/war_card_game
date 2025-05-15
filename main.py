from src.game.war_game import WarGame

if __name__ == "__main__":
    game = WarGame()
    # Se você tiver uma ConsoleUI:
    # ui = ConsoleUI(game)
    # ui.run()
    # Ou diretamente:
    game.start_game()
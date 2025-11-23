import pygame
import os
import sys

# 1. Obtém o caminho absoluto para o diretório onde este script (run_game.py) está.
#    Ex: /caminho/para/o/seu/projeto/WAR_CARD_GAME/
project_root = os.path.dirname(os.path.abspath(__file__))

# 2. Constrói o caminho para a pasta 'src' que está dentro do diretório do projeto.
#    Ex: /caminho/para/o/seu/projeto/WAR_CARD_GAME/src/
src_path = os.path.join(project_root, "src")

# 3. Adiciona o caminho da pasta 'src' ao sys.path.
#    Isso diz ao Python para procurar módulos também dentro da pasta 'src'.
#    Ao fazer isso, podemos usar importações como 'from ui.gui_manager ...' ou 'from game.war_game_logic ...'
#    como se os pacotes 'ui' e 'game' estivessem no nível superior para o interpretador.
#    Sem essa linha, as importações 'from src.ui...' seriam necessárias se 'project_root'
#    fosse adicionado ao sys.path e 'src' fosse um pacote (com __init__.py).
#    A abordagem atual (adicionar 'src_path') simplifica as importações nos outros módulos
#    para não precisarem do prefixo 'src.'.
if src_path not in sys.path:
    sys.path.insert(0, src_path) # Insere no início para prioridade.

# --- Importações Principais ---
# Agora que 'src/' está no sys.path, podemos importar diretamente dos pacotes dentro de 'src'.
try:
    from ui.gui_manager import GUIManager         # Módulo principal da interface gráfica.
    from game.war_game_logic import WarGameLogic   # Módulo da lógica do jogo.
                                                # Esta importação aqui é opcional se o GUIManager
                                                # for o único a instanciar WarGameLogic.
except ImportError as e:
    print(f"ERRO FATAL: Falha ao importar componentes principais: {e}")
    print(f"Verifique se a pasta 'src' existe em: {project_root}")
    print("E se as subpastas 'ui' e 'game' (com seus respectivos __init__.py) estão dentro de 'src'.")
    sys.exit(1)
except Exception as e:
    print(f"ERRO FATAL: Erro inesperado durante importações: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def main_local_gui():
    """
    Função principal: inicializa o gerenciador da GUI e executa o jogo.
    """
    print("Iniciando Jogo de Guerra Local com GUI...")
    gui_manager_instance = None # Para acesso no bloco 'finally'
    try:
        # A lógica do jogo (WarGameLogic) é instanciada dentro do GUIManager.
        gui_manager_instance = GUIManager()
        gui_manager_instance.executar() # Inicia o loop principal do jogo.

    except ImportError as e: # Este except é mais para erros de importação dentro do try
        print(f"ERRO FATAL: Falha na importação de um módulo da UI ou do Jogo durante a execução: {e}")
    except pygame.error as e_pygame:
        print(f"ERRO DO PYGAME: {e_pygame}")
    except Exception as e_geral:
        print(f"ERRO INESPERADO NA APLICAÇÃO: {e_geral}")
        import traceback
        traceback.print_exc()
    finally:
        # Garante que o Pygame seja finalizado corretamente.
        if pygame.get_init():
            pygame.quit()
        print("Aplicação encerrada.")

if __name__ == "__main__":
    # Executa a função principal apenas se este script for o ponto de entrada.
    main_local_gui()

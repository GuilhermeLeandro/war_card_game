from war_card_game.src.structures.actions import criar_baralho, criar_pilha, comprar_carta

def testar_pilha():
    baralho = criar_baralho()
    pilha_baralho = criar_pilha(baralho)
    
    print("Ordem inicial das cartas na pilha (do topo para o fundo):")
    for carta in reversed(pilha_baralho):
        print(carta)
    
    print("\nComprando uma carta...")
    comprar_carta(pilha_baralho)
    
    print("\nOrdem das cartas na pilha após a compra:")
    for carta in reversed(pilha_baralho): 
        print(carta)

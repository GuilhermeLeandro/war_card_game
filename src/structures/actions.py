import random

def criar_baralho():
    naipe = ['copas', 'paus', 'espadas', 'ouros']
    valores = list(range(1, 14))
    baralho = [(valor, naipe) for naipe in naipe for valor in valores]
    random.shuffle(baralho)
    
    return baralho


def criar_pilha(baralho):
    pilha = []
    while baralho:
        pilha.append(baralho.pop())
    
    return pilha

def comprar_carta(pilha):
    if pilha:
        carta_comprada = pilha.pop()
        print(f"Carta comprada: {carta_comprada}")
        return carta_comprada
    else:
        print("Não há mais cartas na pilha!")
        return None
    

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




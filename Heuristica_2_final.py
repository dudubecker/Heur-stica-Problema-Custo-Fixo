import numpy as np


####### FO #######

# Função de calcular o valor da função objetivo,
# passando um dicionário onde as keys são os itens e as values
# são os valores produzidos do recurso

def FO(dict_solucao):
    
    Z = 0
    
    # Iterando no dicionário da solução
    for i, X in dict_solucao.items():
        
        # Somando o lucro
        Z += p[i]*X
        
        # Subtraindo os custos fixos
        Z -= st[i]
    
    return Z

####### Carregando dados do problema #######

## INSTÂNCIA 1: 

# Número de itens
#i = 6

# Número de recursos
#j = 3

# lista de itens
#I = list(range(i))

# lista de recursos
#J = list(range(j))

# Lucro de cada item
#p = [10,13,15,12,8,9]

# Custo fixo de cada item
#st = [900,1020,1200,850,700,900]

# Disponibilidade de cada recurso
#R = [500,200,120]

# Consumo de recurso para cada item
#r = [[0,1,4],
#     [2,0,0],
#     [1,6,0],
#     [3,1,1],
#     [2,0,1],
#     [1,1,0]]



## INSTÂNCIA 2:

# Número de itens
#i = 10

# Número de recursos
#j = 3

# lista de itens
#I = list(range(i))

# lista de recursos
#J = list(range(j))

# Lucro de cada item
#p = [9,14,12,10,10,10,10,14,8,12]

# Custo fixo de cada item
#st = [1199, 947, 1195, 1057, 678, 984, 696, 750, 1001, 861]

# Disponibilidade de cada recurso
#R = [308,305,239]

# Consumo de recurso para cada item
#r = [[3,3,5],
#     [3,5,8],
#     [3,3,3],
#     [3,5,3],
#     [3,6,9],
#     [6,3,3],
#     [3,3,3],
#     [3,3,4],
#     [4,10,3],
#     [7,9,5]]



## INSTÂNCIA 3:

# Número de itens
#i = 20

# Número de recursos
#j = 3

# lista de itens
#I = list(range(i))

# lista de recursos
#J = list(range(j))

# Lucro de cada item
#p = [9,14,12,10,10,10,10,14,8,12,15,12,15,13,9,12,9,10,13,11]

# Custo fixo de cada item
#st = [816, 811, 679, 690, 953, 1099, 738, 999, 1066, 782,
      #666, 901, 696, 1123, 759, 771, 956, 1034, 877, 878]

# Disponibilidade de cada recurso
#R = [324, 235, 294]

# Consumo de recurso para cada item
#r = [[1,2,1],
     #[3,3,7],
     #[1,5,6],
     #[4,1,1],
     #[1,3,2],
     #[1,1,2],
     #[4,1,1],
     #[2,7,1],
     #[1,1,1],
     #[1,4,1],
     #[5,1,1],
     #[3,2,1],
     #[1,1,1],
     #[1,1,1],
     #[6,1,2],
     #[1,3,9],
     #[1,1,1],
     #[1,4,2],
     #[1,1,1],
     #[1,1,1]]



## INSTÂNCIA 4

# Número de itens
i = 20

# Número de recursos
j = 3

# lista de itens
I = list(range(i))

# lista de recursos
J = list(range(j))

# Lucro de cada item
p = [9,14,12,10,10,10,10,14,8,12,15,12,15,13,9,12,9,10,13,11]

# Custo fixo de cada item
st = [472,470,426,430,518,566,446,533,555,461,422,500,432,574,453,457,519,545,526,493]

# Disponibilidade de cada recurso
R = [324,235,294]

# Consumo de recurso para cada item
r = [[0,1,1],
     [3,2,3],
     [1,3,3],
     [3,1,0],
     [0,3,2],
     [0,3,0],
     [1,2,3],
     [1,0,2],
     [2,2,1],
     [1,1,1],
     [4,2,3],
     [1,1,3],
     [0,1,0],
     [1,2,1],
     [1,1,1],
     [1,4,4],
     [1,1,3],
     [2,4,0],
     [3,0,2],
     [0,0,2]]

####### Heurística construtiva #######

# Dicionário com os scores de cada item
dict_scores = dict()

# Para cada item

for i in I:
    
    # Computando score para cada item
    score = (p[i]/(sum([(r[i][j])/(R[j]) for j in J])))/ 1000

    dict_scores[i] = score
    
# Lista de priorização de itens
lista_items_scores = sorted(dict_scores, key=dict_scores.get, reverse=True)

# lista atualizada iterativamente, conforme os recursos são consumidos 
recursos_disponiveis = R.copy()

# Lista de soluções, para cada lista de scores retirando o primeiro elemento

lista_solucoes_fase1 = []

# Dicionário com a solução construída
S = dict()

### Início da Fase 1: atingir breakevens dos primeiros itens de maior score ###

while len(lista_items_scores) > 0:

    
    for i in lista_items_scores:

        # Quantidade necessária até o breakeven
        n_itens = np.ceil(st[i]/p[i])
        
        # Valor booleano que diz se todos os recursos estão disponíveis (inicia-se como True)
        disponibilidade_recursos = True
        
        for j in J:
            
            # Se o que eu preciso do recurso j for maior do que o que eu tenho disponível
            if (n_itens*r[i][j] > recursos_disponiveis[j]):
                
                # Se o parâmetro for falso, quer dizer que o recurso j não está disponível para atingir o breakeven!
                disponibilidade_recursos = False
        
        
        # Se TODOS os recursos estiverem disponíveis para atingir o breakeven, eles são consumidos
        if disponibilidade_recursos == True:
            
            for j in J:
                
                # Consumindo recursos disponíveis com o operador -= (subtrai e recebe)
                recursos_disponiveis[j] -= np.floor(n_itens*r[i][j])
                
                # Registrando produção dos itens na solução
                S[i] = n_itens
                
        # Se não, já atingiu-se o breakeven com todos os itens de maior score!
        else:
            
            break
       
    # Guardando solução
    lista_solucoes_fase1.append((S, recursos_disponiveis, FO(S)))
    
    # Reinicializando valores
    recursos_disponiveis = R.copy()
    S = dict()
    
    # Atualizando lista de scores
    lista_items_scores.pop(round(len(lista_items_scores)/2))
    

### Fim da fase 1 ###
    
### Início da fase 2: consumir recursos restantes ###

# Lista de soluções da fase 2:
    
lista_solucoes_fase2 = []

# Solução da fase 2

# Para cada item da solução

for solucao in lista_solucoes_fase1:
    
    
    # Melhor solução encontrada no início da iteração (a própria solução inicial)
    S_fase2 = solucao[0].copy()
    
    
    recursos_disponiveis = solucao[1].copy()
    
    # Se algum item foi produzido na solução em questão:

    if len(S_fase2)>0:
    
        for i in S_fase2.keys():
            
            # Fase 2.1:
            
            S_iteracao = solucao[0].copy()
            
            recursos_disponiveis = solucao[1].copy()
            
            qtd_produzida = np.floor(min([recursos_disponiveis[j]/r[i][j] for j in J if r[i][j] > 0]))
            
            # Atualizando solução
            S_iteracao[i] += qtd_produzida
            
            
            # Atualizando recursos disponíveis
            for j in J:
                
                # Consumindo recursos disponíveis com o operador -= (subtrai e recebe)
                recursos_disponiveis[j] -= qtd_produzida*r[i][j]
        
        
            
            # Fase 2.2:
            
            # Analisando se ainda é possível produzir itens de outros tipos
            itens_restantes = list(S_iteracao.keys())
            itens_restantes.remove(i)
            
            for item in itens_restantes:
                
                disponibilidade_recursos = True
                
                for j in J:
                    
                    # Se a quantidade disponível for menor do que a quantidade unitária
                    if recursos_disponiveis[j] < r[item][j]:
                        
                        disponibilidade_recursos = False
                
                # Se todos os recursos estiverem disponíveis
                if disponibilidade_recursos == True:
                    
                    qtd_produzida = np.floor(min([recursos_disponiveis[j]/r[item][j] for j in J if r[item][j] > 0]))
                    
                    # Atualizando solução
                    S_iteracao[item] += qtd_produzida
                   
                    # Atualizando recursos disponíveis
                    for j in J:
                        
                        # Consumindo recursos disponíveis com o operador -= (subtrai e recebe)
                        recursos_disponiveis[j] -= qtd_produzida*r[item][j]
            
        # Se a solução for melhor do que a melhor solução conhecida, ela se torna a melhor solução
        
            if FO(S_iteracao) > FO(S_fase2):
                
                S_fase2 = S_iteracao
                recursos = recursos_disponiveis
            
        lista_solucoes_fase2.append((S_fase2, recursos, FO(S_fase2)))
    

# Escolhendo, dentre as soluções obtidas, aquela com maior FO:
        
solucoes_finais = [s[2] for s in lista_solucoes_fase2]


# Melhor solução encontrada:
    
S_final = lista_solucoes_fase2[np.argmax(solucoes_finais)][0]


            
    
        
    
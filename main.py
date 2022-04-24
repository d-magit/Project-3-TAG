"""
24/04/2022

Projeto 3 - Teoria e Aplicação de Grafos - 2021.2

Universidade de Brasília - Instituto de Ciências Exatas - Departamento de Ciência da Computação (CiC)

Professor: Díbio Leandro Borges

O jogo Sudoku clássico propõe uma grade 9x9. Essa grade é dividida em 9 subgrades quadradas 3x3,
também chamadas de blocos. As figuras a seguir mostram EXEMPLOS de um Sudoku desse tipo, em
a) uma proposta de configuração inicial, e em b) uma solução. O objetivo do jogo é preencher com
dígitos de 1 a 9, sendo que nas linhas e colunas dos blocos não pode haver dígitos repetidos.
Pede-se nesse projeto o seguinte:
1) Modelar um jogo Sudoku 9x9 como um grafo; (1,0 pto)
2) O jogo deve proporcionar:
2.1) checar se uma proposta numérica for válida; (1,0 pto)
2.2) gerar soluções e apresentá-las em tela; (2,0 ptos)
2.3) gerar propostas aleatórias para futuros jogos; (1,0 pto)
3) A solução deve usar um algoritmo de coloração de grafos, e essa deve mostrar os passos da solução
(saídas intermediárias); (5,0 ptos)
"""
from random import randint

def init_graph():
    """Função de inicializar o grafo do tabuleiro de Sudoku."""
    # Inicializa o grafo
    graph = [{'index': i, 'adjacences': set(), 'colors': set(range(1, 10)), 'final_color': 0} for i in range(81)]
    
    # Produto cartesiano 3x3
    cart_prod = [(i, j) for i in range(3) for j in range(3)]
    # Função montadora de blocos
    blocks_factory = lambda j: list([9*i[0] + i[1] + 27*j[0] + 3*j[1] for i in cart_prod])
    # Função de adicionar adjacências
    add_adjacences = lambda l: [graph[i]['adjacences'].add(j) for k in l for i in k for j in k]

    # Monta todos os blocos
    add_adjacences(map(blocks_factory, cart_prod))
    # Monta todas as linhas
    add_adjacences(map(lambda y: list(range(y, 9 + y)), range(0, 81, 9)))
    # Monta todas as colunas
    add_adjacences(map(lambda x: list(range(x, 81 + x, 9)), range(9)))
    
    return graph



def start_new_game():
    """Função de inicializar um novo jogo de Sudoku."""
    def solve_and_validate_sudoku(test_subject, return_on_success, on_fail):
        """
        Função auxiliar para resolver e validar um tabuleiro de Sudoku.
        Resolve para 'test_subject' e retorna 'return_on_success' em caso de sucesso.
        Caso falhe, invoca a função on_fail e retorna seu resultado.
        """
        try:
            solve_sudoku(test_subject, False)
            if check_solution(test_subject) != -1:
                return on_fail()
            return return_on_success
        except:
            return on_fail()

    def get_solved_sudoku():
        """
        Tenta montar um tabuleiro inicial, colocando apenas uma cor aleatória em uma célula aleatória
        Após isso, resolve e retorna.
        """
        graph = init_graph()
        graph[randint(0, 80)]['final_color'] = randint(1,9)
        return solve_and_validate_sudoku(graph, graph, get_solved_sudoku)
    
    def mount_sudoku():
        """Tenta pegar 25 casas aleatórias de um Sudoku resolvido (valid_sudoku) e montar uma proposta válida"""
        graph = init_graph()
        test_graph = init_graph()
        color_indexes = list(set([randint(0, 80) for _ in range(40)]))[:25]
        for i in color_indexes:
            color = valid_sudoku[i]['final_color']
            graph[i]['final_color'] = color
            test_graph[i]['final_color'] = color
        return solve_and_validate_sudoku(test_graph, graph, mount_sudoku)

    # Adquire um Sudoku resolvido válido aleatório usando get_solved_sudoku
    valid_sudoku = get_solved_sudoku()
    # Monta proposta inicial válida a partir do Sudoku resolvido e retorna
    return mount_sudoku()



def get_table(graph):
    """Converte o grafo para uma lista que representa o tabuleiro (coloração)"""
    return [i['final_color'] for i in graph]



def solve_sudoku(table, is_print):
    """Função de solucionar o Sudoku."""
    # Cache de estados para printar posteriormente
    cached_states = []
    # Função lambda estática auxiliar, usada no passo 3 para escolher o nó que tenha maior número de adjacentes descoloridos
    get_colorless_adjacents_num = lambda node: len([i for i in node['adjacences'] if node['final_color'] == 0])
    # Cache de nós ainda não solucionados
    to_color_nodes = set(range(len(table)))
    def solve_sudoku_internal(vertices):
        """Função interna recursiva para solucionar o Sudoku."""
        # A cada iteração, se for para printar, adiciona o estado atual do grafo no cache
        if is_print:
            cached_states.append(get_table(table))

        # Passo 1:
        # - Pintar os vértices já coloridos e que não foram pintados, e remover a cor da lista de seus vizinhos.
        nonlocal to_color_nodes
        for node in vertices:
            color_set = set([node['final_color']])
            to_color_nodes -= set([node['index']])
            for i in node['adjacences']:
                table[i]['colors'] -= color_set

        # Passo 2:
        # - Se há vértices não coloridos, pegar os que tem menor possibilidade de cores.
        if (len(to_color_nodes) == 0):
            return
        less_colors = []
        curr_num = 9
        for node in table:
            if node['final_color'] != 0:
                continue
            free_color_num = len(node['colors'])
            if free_color_num == curr_num:
                less_colors.append(node)
            elif free_color_num < curr_num:
                curr_num = free_color_num
                less_colors = [node]

        # Passo 3:
        # - Se há vértices que só possuem uma cor, pegar essa cor e loopar.
        # - Se não, pegar o que tenha maior número de adjacentes descoloridos, colorir para sua primeira cor livre e loopar.
        if curr_num == 1:
            for node in less_colors:
                node['final_color'] = list(node['colors'])[0]
            solve_sudoku_internal(less_colors)
        else:
            less_colored_adjacents = sorted(less_colors, key = get_colorless_adjacents_num)[-1]
            less_colored_adjacents['final_color'] = sorted(list(less_colored_adjacents['colors']))[0]
            solve_sudoku_internal([less_colored_adjacents])
    
    # Inicializa recursão com nós iniciais já coloridos
    solve_sudoku_internal([i for i in table if i['final_color'] != 0])
    # Se for para printar, seleciona 10 estados aleatórios do algoritmo, e os printa em ordem
    if is_print:
        selected_indexes = set()
        max_state_index = len(cached_states) - 2
        while len(selected_indexes) < 10:
            selected_indexes.add(randint(1, max_state_index))
        for i in sorted(list(selected_indexes)):
            print(f"==| Resultado da iteração {i}:")
            beautify_sudoku(cached_states[i])



def check_solution(graph):
    """
    Função de checar a validade de uma solução do Sudoku. 
    Retorna -1 para Sudoku válido, 0 para Sudoku incompleto e 1 para Sudoku com coloração inválida.
    """
    for node in graph:
        final_color = node['final_color']
        if final_color == 0:
            return 0
        adjacent_colors = [graph[i]['final_color'] for i in node['adjacences'] - set([node['index']])]
        if final_color in adjacent_colors:
            return 1
    return -1



def beautify_sudoku(table):
    """Printa o sudoku na tela"""
    print("-"*31)
    for i in range(len(table)):
        if i == 0:
            print(f"| {table[i]}", end=' ')
            continue

        if i%3 == 0:
            print("|", end='')
        if i%27 == 0:
            print("\n" + "-"*31)
        if i%9 == 0:
            if i%27 != 0:
                print()
            print("|", end='')
        print(f" {table[i]}", end=' ')
    print("|\n" + "-"*31)



if __name__ == "__main__":
    graph = start_new_game()
    print("==| Proposta gerada:")
    beautify_sudoku(get_table(graph))

    solve_sudoku(graph, True)
    print("==| Resultado do algorítmo:")
    beautify_sudoku(get_table(graph))

    print("==| Resultado da checagem:")
    check = check_solution(graph)
    if check == -1:
        print('Sudoku resolvido com sucesso!')
    elif check == 0:
        print('Sudoku incompleto :c')
    else:
        print('Sudoku inválido :c')
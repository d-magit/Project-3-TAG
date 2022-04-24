# Projeto 3 - TAG-2021.2

## Informações

Projeto 3 - Teoria e Aplicação de Grafos - 2021.2

Universidade de Brasília - Instituto de Ciências Exatas - Departamento de Ciência da Computação (CiC)

Professor: Díbio Leandro Borges

Foi utilizado um algorítmo de coloração de grafos para resolução de Sudoku, encontrado em http://www.cs.kent.edu/~dragan/ST-Spring2016/SudokuGC.pdf (acesso dia 22/04/2022).

O programa irá printar, no início, a proposta inicial que ele mesmo gera.
Ao final do algorítmo, o estado do tabuleiro ao longo de 10 iterações aleatórias. 
E, por fim, mais uma vez, o estado final do Sudoku resolvido.

## Descrição

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
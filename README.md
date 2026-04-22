# Simulador de memória virtual

##  1. Objetivo
O projeto consiste no desenvolvimento de um simulador que modela o comportamento de uma MMU (Memory Management Unit). O foco principal é a abstração da memória virtual, a tradução de endereços para memória física e a gerência de substituição de páginas quando a RAM atinge sua capacidade máxima.

##  2. Overview
O simulador replica um sistema fictício com as seguintes especificações técnicas:
- **Memória Principal (RAM)**: 64 KB, organizada em 8 frames de 8 KB cada. 
- **Memória Virtual**: 1 MB, organizada em 128 páginas de 8 KB cada.
- **Tamanho de Página/Frame**: 8 KB ($2^{13}$ bytes).
- **Processos**: Suporte a múltiplos processos (mínimo 2) acessando o mesmo espaço de endereçamento virtual de forma isolada.
- **Algoritmo de Substituição**: FIFO (First-In, First-Out).

## 3. Componentes
O projeto está dividido em dois módulos principais para garantir a organização e clareza:
- `mmu.py`: Contém a classe `MMU`, responsável pela lógica bit-a-bit de tradução, detecção de Page Faults e execução do algoritmo FIFO usando uma fila de frames.
- `main.py`: Script de execução que contém a documentação interativa e os cenários de teste que demonstram a MMU em operação.

## 4. Tradução de emdereços
1. Isolamento da Página: O endereço virtual de 20 bits é dividido. Os 13 bits menos significativos representam o Offset, e os 7 bits restantes representam o Número da Página.
2. Consulta à Page Table: A MMU verifica se a combinação (PID, Página) possui um frame mapeado na RAM.
3. Cálculo Físico: Caso presente, o endereço físico é gerado pela fórmula: EndereçoFisico = (Frame x 8192) + Offset

## 5. Detalhes de Implementação 
A escolha do algoritmo FIFO visa a previsibilidade.
- A MMU mantém uma collections.deque que rastreia a ordem de ocupação dos frames físicos.
- Ao ocorrer um Page Fault com a RAM lotada, o frame no topo da fila (o mais antigo) é liberado, seu mapeamento na Tabela de Páginas é invalidado, e a nova página assume seu lugar, indo para o fim da fila.

## 6. Instruções de uso
- **Pré-requistios**
 - Python 3.8 ou superior instalado.

- **Como executar**
1. Clone ou baixe os arquivos `mmu.py` e `main.py` para o mesmo diretório.
2. Abra o terminal na pasta do projeto.
3. Execute o comando:
    `python3 main.py`


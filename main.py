from mmu import MMU
import time

def rodar_simulacao():
    mmu = MMU()
    
    print("="*50)
    print("SIMULADOR DE MEMÓRIA VIRTUAL - UNISINOS")
    print("ALGORITMO: FIFO | RAM: 64KB | VIRTUAL: 1MB")
    print("="*50)

    # Lista de acessos para demonstrar o funcionamento
    # Formato: (Processo_ID, Endereço_Virtual)
    acessos = [
        (1, 0x1000),   # P1 acessa Página 0 (Page Fault)
        (2, 0x2000),   # P2 acessa Página 1 (Page Fault)
        (1, 0x1500),   # P1 acessa Página 0 novamente (HIT)
        (1, 0x4000),   # P1 acessa Página 2
        (2, 0x6000),   # P2 acessa Página 3
        (1, 0x8000),   # P1 acessa Página 4
        (2, 0xA000),   # P2 acessa Página 5
        (1, 0xC000),   # P1 acessa Página 6
        (2, 0xE000),   # P2 acessa Página 7 -> Aqui a RAM enche (8 frames)
        (1, 0x10000),  # P1 acessa Página 8 -> FIFO deve expulsar a mais antiga (P1/Pag0)
        (1, 0x1000),   # P1 acessa Página 0 de novo -> Deve dar Page Fault novamente
    ]

    for pid, addr in acessos:
        mmu.traduzir_endereco(pid, addr)
        time.sleep(0.5) # Pausa para facilitar a leitura na apresentação

if __name__ == "__main__":
    rodar_simulacao()
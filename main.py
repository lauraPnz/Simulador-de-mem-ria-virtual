from mmu import MMU
import time

def rodar_simulacao():
    mmu = MMU()
    
    print("-"*50)
    print("SIMULADOR DE MEMÓRIA VIRTUAL")
    print("ALGORITMO: FIFO | RAM: 64KB | VIRTUAL: 1MB")
    print("-"*50)

    
    acessos = [
        (1, 0x1000),   
        (2, 0x2000),   
        (1, 0x1500),   
        (1, 0x4000),   
        (2, 0x6000),   
        (1, 0x8000),   
        (2, 0xA000),   
        (1, 0xC000),  
        (2, 0xE000),  
        (1, 0x10000),  
        (1, 0x1000),  
    ]

    for pid, addr in acessos:
        mmu.traduzir_endereco(pid, addr)
        time.sleep(1.0) 

if __name__ == "__main__":
    rodar_simulacao()

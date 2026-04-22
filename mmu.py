from collections import deque

# Configurações conforme o enunciado
TAM_MEMORIA_PRINCIPAL = 64 * 1024  # 64 KB
TAM_MEMORIA_VIRTUAL = 1024 * 1024  # 1 MB
TAM_PAGINA = 8 * 1024              # 8 KB

QTD_FRAMES = TAM_MEMORIA_PRINCIPAL // TAM_PAGINA  # 8 frames físicos
QTD_PAGINAS = TAM_MEMORIA_VIRTUAL // TAM_PAGINA    # 128 páginas virtuais

class MMU:
    def __init__(self):
        # Tabela de páginas: mapeia (PID, Página) -> Frame
        self.tabela_paginas = {}
        
        # Representação da RAM: Armazena tuplas (PID, Página) para saber quem ocupa cada frame
        self.frames_ram = [None] * QTD_FRAMES
        
        # Fila FIFO para gerenciar qual frame será substituído
        self.fila_fifo = deque(range(QTD_FRAMES))
        
        # Para fins de simulação: dados fictícios que estariam no "disco"
        self.disco_virtual = {} 

    def traduzir_endereco(self, pid, endereco_virtual):
        # Item 6: Cálculo de Página e Offset
        num_pagina = endereco_virtual // TAM_PAGINA
        offset = endereco_virtual % TAM_PAGINA
        chave = (pid, num_pagina)

        print(f"\n[CPU] Processo {pid} requisitou: {hex(endereco_virtual)}")
        print(f"[MMU] Mapeando: Página {num_pagina}, Offset {hex(offset)}")

        # Item 7: Detecção de Falta de Página
        if chave in self.tabela_paginas:
            frame = self.tabela_paginas[chave]
            endereco_fisico = (frame * TAM_PAGINA) + offset
            print(f"[MMU] HIT: Página encontrada no Frame {frame}")
            print(f" -> Endereço Físico: {hex(endereco_fisico)}")
            return True
        else:
            # Item 8 e 9: Tratamento e Substituição
            self._tratar_page_fault(pid, num_pagina)
            # Tenta novamente após carregar
            return self.traduzir_endereco(pid, endereco_virtual)

    def _tratar_page_fault(self, pid, num_pagina):
        print(f"[ALERTA] PAGE FAULT: Página {num_pagina} do Processo {pid} não está na RAM.")
        
        # FIFO decide qual frame sai
        frame_vitima = self.fila_fifo.popleft()
        
        # Se o frame estava ocupado, invalida o mapeamento antigo
        if self.frames_ram[frame_vitima] is not None:
            antigo_pid, antiga_pag = self.frames_ram[frame_vitima]
            print(f"[FIFO] RAM Lotada. Removendo Processo {antigo_pid}, Página {antiga_pag} do Frame {frame_vitima}")
            del self.tabela_paginas[(antigo_pid, antiga_pag)]

        # Carrega a nova página (Simulação de I/O)
        print(f"[RAM] Carregando nova página no Frame {frame_vitima}...")
        self.frames_ram[frame_vitima] = (pid, num_pagina)
        self.tabela_paginas[(pid, num_pagina)] = frame_vitima
        
        # Coloca o frame de volta no fim da fila (ele é agora o mais recente)
        self.fila_fifo.append(frame_vitima)
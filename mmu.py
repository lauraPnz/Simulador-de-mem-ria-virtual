from collections import deque

TAM_MEMORIA_PRINCIPAL = 64 * 1024
TAM_MEMORIA_VIRTUAL = 1024 * 1024
TAM_PAGINA = 8 * 1024

QTD_FRAMES = TAM_MEMORIA_PRINCIPAL // TAM_PAGINA
QTD_PAGINAS = TAM_MEMORIA_VIRTUAL // TAM_PAGINA

class MMU:
    def __init__(self):
        self.tabela_paginas = {}
        self.frames_ram = [None] * QTD_FRAMES
        self.fila_fifo = deque(range(QTD_FRAMES))
        self.disco_virtual = {}

    def traduzir_endereco(self, pid, endereco_virtual):
        num_pagina = endereco_virtual // TAM_PAGINA
        offset = endereco_virtual % TAM_PAGINA
        chave = (pid, num_pagina)

        print(f"\n[CPU] Processo {pid} requisitou: {hex(endereco_virtual)}")
        print(f"[MMU] Mapeando: Página {num_pagina}, Offset {hex(offset)}")

        if chave in self.tabela_paginas:
            frame = self.tabela_paginas[chave]
            endereco_fisico = (frame * TAM_PAGINA) + offset
            print(f"[MMU] HIT: Página encontrada no Frame {frame}")
            print(f" -> Endereço Físico: {hex(endereco_fisico)}")
            return True
        else:
            self._tratar_page_fault(pid, num_pagina)
            return self.traduzir_endereco(pid, endereco_virtual)

    def _tratar_page_fault(self, pid, num_pagina):
        print(f"[ALERTA] PAGE FAULT: Página {num_pagina} do Processo {pid} não está na RAM.")
        
        frame_vitima = self.fila_fifo.popleft()
        
        if self.frames_ram[frame_vitima] is not None:
            antigo_pid, antiga_pag = self.frames_ram[frame_vitima]
            print(f"[FIFO] RAM Lotada. Removendo Processo {antigo_pid}, Página {antiga_pag} do Frame {frame_vitima}")
            del self.tabela_paginas[(antigo_pid, antiga_pag)]

        print(f"[RAM] Carregando nova página no Frame {frame_vitima}...")
        self.frames_ram[frame_vitima] = (pid, num_pagina)
        self.tabela_paginas[(pid, num_pagina)] = frame_vitima
        self.fila_fifo.append(frame_vitima)

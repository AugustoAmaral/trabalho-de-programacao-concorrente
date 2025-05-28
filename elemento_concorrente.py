"""
Módulo para implementar programação concorrente com threads
Cada elemento (azul ou zombie) roda em sua própria thread
"""
import threading
import time
import random
from typing import List, Tuple
from queue import Queue

class ElementoConcorrente:
    def __init__(self, posicao: Tuple[int, int], tipo: int, tabuleiro_ref, lock: threading.Lock):
        """
        Inicializa um elemento concorrente
        
        Args:
            posicao: Posição inicial (linha, coluna)
            tipo: 1 para azul, 2 para zombie
            tabuleiro_ref: Referência ao tabuleiro compartilhado
            lock: Lock para sincronização
        """
        self.posicao = posicao
        self.tipo = tipo
        self.tabuleiro = tabuleiro_ref
        self.lock = lock
        self.ativo = True
        self.thread = None
        self.intervalo_movimento = random.uniform(0.1, 0.5)  # Velocidade aleatória
    
    def iniciar(self):
        """Inicia a thread do elemento"""
        self.thread = threading.Thread(target=self._executar, daemon=True)
        self.thread.start()
    
    def parar(self):
        """Para a execução do elemento"""
        self.ativo = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
    
    def _executar(self):
        """Loop principal da thread do elemento"""
        while self.ativo:
            try:
                if self.tipo == 1:  # Elemento azul
                    self._mover_azul()
                elif self.tipo == 2:  # Zombie
                    self._mover_zombie()
                
                time.sleep(self.intervalo_movimento)
            
            except Exception as e:
                print(f"Erro no elemento {self.tipo} em {self.posicao}: {e}")
                break
    
    def _mover_azul(self):
        """Lógica de movimento para elemento azul"""
        with self.lock:
            linha, coluna = self.posicao
            
            # Verifica se ainda existe no tabuleiro
            if (linha >= len(self.tabuleiro) or 
                coluna >= len(self.tabuleiro[0]) or 
                self.tabuleiro[linha][coluna] != 1):
                self.ativo = False
                return
            
            # Preferência por mover para a direita (objetivo)
            direcoes = [(0, 1), (-1, 0), (1, 0), (0, -1)]  # direita, cima, baixo, esquerda
            
            # Adiciona aleatoriedade mas mantém preferência pela direita
            if random.random() < 0.7:  # 70% chance de tentar ir para direita primeiro
                pass
            else:
                random.shuffle(direcoes)
            
            for dx, dy in direcoes:
                nova_linha = linha + dx
                nova_coluna = coluna + dy
                
                if self._posicao_valida(nova_linha, nova_coluna):
                    if self.tabuleiro[nova_linha][nova_coluna] == 0:
                        # Move para posição vazia
                        self.tabuleiro[linha][coluna] = 0
                        self.tabuleiro[nova_linha][nova_coluna] = 1
                        self.posicao = (nova_linha, nova_coluna)
                        break
    
    def _mover_zombie(self):
        """Lógica de movimento para zombie"""
        with self.lock:
            linha, coluna = self.posicao
            
            # Verifica se ainda existe no tabuleiro
            if (linha >= len(self.tabuleiro) or 
                coluna >= len(self.tabuleiro[0]) or 
                self.tabuleiro[linha][coluna] != 2):
                self.ativo = False
                return
            
            # Primeiro, infecta adjacentes
            self._infectar_adjacentes()
            
            # Depois tenta se mover
            direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(direcoes)
            
            for dx, dy in direcoes:
                nova_linha = linha + dx
                nova_coluna = coluna + dy
                
                if self._posicao_valida(nova_linha, nova_coluna):
                    destino = self.tabuleiro[nova_linha][nova_coluna]
                    
                    if destino == 0:  # Posição vazia
                        self.tabuleiro[linha][coluna] = 0
                        self.tabuleiro[nova_linha][nova_coluna] = 2
                        self.posicao = (nova_linha, nova_coluna)
                        break
                    elif destino == 1:  # Elemento azul - infecta
                        self.tabuleiro[linha][coluna] = 0
                        self.tabuleiro[nova_linha][nova_coluna] = 2
                        self.posicao = (nova_linha, nova_coluna)
                        break
    
    def _infectar_adjacentes(self):
        """Infecta elementos azuis adjacentes"""
        linha, coluna = self.posicao
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in direcoes:
            nova_linha = linha + dx
            nova_coluna = coluna + dy
            
            if (self._posicao_valida(nova_linha, nova_coluna) and 
                self.tabuleiro[nova_linha][nova_coluna] == 1):
                
                # Infecta o elemento azul
                self.tabuleiro[nova_linha][nova_coluna] = 2
    
    def _posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição é válida"""
        return (0 <= linha < len(self.tabuleiro) and 
                0 <= coluna < len(self.tabuleiro[0]))

class GerenciadorConcorrente:
    def __init__(self, tabuleiro_ref):
        """
        Gerencia todos os elementos concorrentes
        
        Args:
            tabuleiro_ref: Referência ao tabuleiro compartilhado
        """
        self.tabuleiro = tabuleiro_ref
        self.lock = threading.Lock()
        self.elementos = []
        self.executando = False
    
    def adicionar_elemento(self, posicao: Tuple[int, int], tipo: int):
        """Adiciona um novo elemento concorrente"""
        elemento = ElementoConcorrente(posicao, tipo, self.tabuleiro, self.lock)
        self.elementos.append(elemento)
        return elemento
    
    def iniciar_todos(self):
        """Inicia todas as threads dos elementos"""
        self.executando = True
        for elemento in self.elementos:
            elemento.iniciar()
    
    def parar_todos(self):
        """Para todas as threads dos elementos"""
        self.executando = False
        for elemento in self.elementos:
            elemento.parar()
        self.elementos.clear()
    
    def limpar_inativos(self):
        """Remove elementos que não estão mais ativos"""
        elementos_ativos = [e for e in self.elementos if e.ativo]
        elementos_removidos = len(self.elementos) - len(elementos_ativos)
        self.elementos = elementos_ativos
        return elementos_removidos
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas dos elementos concorrentes"""
        azuis = sum(1 for e in self.elementos if e.tipo == 1 and e.ativo)
        zombies = sum(1 for e in self.elementos if e.tipo == 2 and e.ativo)
        
        return {
            'elementos_azuis': azuis,
            'zombies': zombies,
            'total_threads': len(self.elementos),
            'threads_ativas': sum(1 for e in self.elementos if e.ativo)
        }

# Exemplo de uso do sistema concorrente
class JogoZombieConcorrente:
    def __init__(self, tamanho: int = 50):
        self.tamanho = tamanho
        self.tabuleiro = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
        self.gerenciador = GerenciadorConcorrente(self.tabuleiro)
        self.rodada = 0
    
    def inicializar_jogo(self, num_azuis: int = 10, num_zombies: int = 5):
        """Inicializa o jogo com elementos concorrentes"""
        # Limpa o estado anterior
        self.gerenciador.parar_todos()
        self.tabuleiro = [[0 for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        
        # Adiciona elementos azuis
        for _ in range(num_azuis):
            linha = random.randint(0, self.tamanho - 1)
            coluna = random.randint(0, 5)
            
            while self.tabuleiro[linha][coluna] != 0:
                linha = random.randint(0, self.tamanho - 1)
                coluna = random.randint(0, 5)
            
            self.tabuleiro[linha][coluna] = 1
            self.gerenciador.adicionar_elemento((linha, coluna), 1)
        
        # Adiciona zombies
        for _ in range(num_zombies):
            linha = random.randint(0, self.tamanho - 1)
            coluna = random.randint(0, self.tamanho - 1)
            
            while self.tabuleiro[linha][coluna] != 0:
                linha = random.randint(0, self.tamanho - 1)
                coluna = random.randint(0, self.tamanho - 1)
            
            self.tabuleiro[linha][coluna] = 2
            self.gerenciador.adicionar_elemento((linha, coluna), 2)
        
        # Inicia todas as threads
        self.gerenciador.iniciar_todos()
    
    def verificar_condicoes_fim(self) -> Tuple[bool, str]:
        """Verifica condições de fim do jogo"""
        estatisticas = self.gerenciador.obter_estatisticas()
        
        # Não há mais elementos azuis
        if estatisticas['elementos_azuis'] == 0:
            return True, "TODOS OS ELEMENTOS VIRARAM ZOMBIES!"
        
        # Verifica se algum azul chegou à direita
        for i in range(self.tamanho):
            if self.tabuleiro[i][self.tamanho - 1] == 1:
                return True, "ELEMENTO AZUL CHEGOU À DIREITA! VITÓRIA!"
        
        return False, ""
    
    def finalizar(self):
        """Finaliza o jogo parando todas as threads"""
        self.gerenciador.parar_todos()
"""
Módulo principal do jogo com a lógica de funcionamento
"""
import random
from typing import List, Tuple, Optional
from threading import Thread, Lock
import time

class JogoZombie:
    def __init__(self, tamanho: int = 50):
        self.tamanho = tamanho
        self.tabuleiro = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
        self.elementos_azuis = []
        self.elementos_zombies = []
        self.lock = Lock()  # Para programação concorrente
        self.jogo_ativo = True
        self.rodada = 0
        
        # Valores do tabuleiro:
        # 0 = vazio, 1 = azul, 2 = zombie
        
    def inicializar_jogo(self, num_azuis: int = 10, num_zombies: int = 5):
        """
        Inicializa o tabuleiro com elementos azuis e zombies
        
        Args:
            num_azuis: Número de elementos azuis
            num_zombies: Número de zombies
        """
        # Limpa o tabuleiro
        self.tabuleiro = [[0 for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.elementos_azuis = []
        self.elementos_zombies = []
        
        # Adiciona elementos azuis (começam na coluna esquerda)
        for _ in range(num_azuis):
            linha = random.randint(0, self.tamanho - 1)
            coluna = random.randint(0, 5)  # Começam nas primeiras colunas
            
            # Garante que a posição está vazia
            while self.tabuleiro[linha][coluna] != 0:
                linha = random.randint(0, self.tamanho - 1)
                coluna = random.randint(0, 5)
            
            self.tabuleiro[linha][coluna] = 1
            self.elementos_azuis.append((linha, coluna))
        
        # Adiciona zombies (posições aleatórias)
        for _ in range(num_zombies):
            linha = random.randint(0, self.tamanho - 1)
            coluna = random.randint(0, self.tamanho - 1)
            
            # Garante que a posição está vazia
            while self.tabuleiro[linha][coluna] != 0:
                linha = random.randint(0, self.tamanho - 1)
                coluna = random.randint(0, self.tamanho - 1)
            
            self.tabuleiro[linha][coluna] = 2
            self.elementos_zombies.append((linha, coluna))
    
    def posicao_valida(self, linha: int, coluna: int) -> bool:
        """Verifica se uma posição está dentro do tabuleiro"""
        return 0 <= linha < self.tamanho and 0 <= coluna < self.tamanho
    
    def mover_elemento(self, pos_atual: Tuple[int, int], tipo: int) -> Optional[Tuple[int, int]]:
        """
        Move um elemento para uma posição adjacente aleatória
        
        Args:
            pos_atual: Posição atual (linha, coluna)
            tipo: Tipo do elemento (1=azul, 2=zombie)
            
        Returns:
            Nova posição ou None se não conseguir mover
        """
        linha, coluna = pos_atual
        
        # Direções possíveis: cima, baixo, esquerda, direita
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(direcoes)
        
        for dx, dy in direcoes:
            nova_linha = linha + dx
            nova_coluna = coluna + dy
            
            if self.posicao_valida(nova_linha, nova_coluna):
                if self.tabuleiro[nova_linha][nova_coluna] == 0:
                    # Move para posição vazia
                    self.tabuleiro[linha][coluna] = 0
                    self.tabuleiro[nova_linha][nova_coluna] = tipo
                    return (nova_linha, nova_coluna)
                elif tipo == 2 and self.tabuleiro[nova_linha][nova_coluna] == 1:
                    # Zombie infecta elemento azul
                    self.tabuleiro[linha][coluna] = 0
                    self.tabuleiro[nova_linha][nova_coluna] = 2
                    return (nova_linha, nova_coluna)
        
        return None  # Não conseguiu mover
    
    def infectar_azuis_adjacentes(self, pos_zombie: Tuple[int, int]):
        """
        Infecta elementos azuis adjacentes ao zombie
        
        Args:
            pos_zombie: Posição do zombie
        """
        linha, coluna = pos_zombie
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in direcoes:
            nova_linha = linha + dx
            nova_coluna = coluna + dy
            
            if (self.posicao_valida(nova_linha, nova_coluna) and 
                self.tabuleiro[nova_linha][nova_coluna] == 1):
                
                # Converte azul em zombie
                self.tabuleiro[nova_linha][nova_coluna] = 2
                
                # Remove da lista de azuis e adiciona na de zombies
                if (nova_linha, nova_coluna) in self.elementos_azuis:
                    self.elementos_azuis.remove((nova_linha, nova_coluna))
                    self.elementos_zombies.append((nova_linha, nova_coluna))
    
    def atualizar_elementos(self):
        """Atualiza as posições de todos os elementos"""
        with self.lock:
            # Atualiza elementos azuis
            novos_azuis = []
            for pos in self.elementos_azuis[:]:
                nova_pos = self.mover_elemento(pos, 1)
                if nova_pos:
                    novos_azuis.append(nova_pos)
                else:
                    novos_azuis.append(pos)
            
            self.elementos_azuis = novos_azuis
            
            # Atualiza zombies
            novos_zombies = []
            for pos in self.elementos_zombies[:]:
                # Primeiro infecta adjacentes
                self.infectar_azuis_adjacentes(pos)
                
                # Depois move
                nova_pos = self.mover_elemento(pos, 2)
                if nova_pos:
                    novos_zombies.append(nova_pos)
                    # Infecta novamente na nova posição
                    self.infectar_azuis_adjacentes(nova_pos)
                else:
                    novos_zombies.append(pos)
            
            self.elementos_zombies = novos_zombies
    
    def verificar_condicoes_fim(self) -> Tuple[bool, str]:
        """
        Verifica se o jogo deve terminar
        
        Returns:
            (fim_jogo, motivo)
        """
        # Verifica se não há mais elementos azuis
        if not self.elementos_azuis:
            return True, "TODOS OS ELEMENTOS VIRARAM ZOMBIES!"
        
        # Verifica se algum elemento azul chegou à direita
        for linha, coluna in self.elementos_azuis:
            if coluna >= self.tamanho - 1:
                return True, "ELEMENTO AZUL CHEGOU À DIREITA! VITÓRIA!"
        
        return False, ""
    
    def executar_rodada(self):
        """Executa uma rodada do jogo"""
        self.rodada += 1
        self.atualizar_elementos()
        return self.verificar_condicoes_fim()
    
    def obter_estatisticas(self) -> dict:
        """Retorna estatísticas do jogo"""
        return {
            'rodada': self.rodada,
            'elementos_azuis': len(self.elementos_azuis),
            'zombies': len(self.elementos_zombies),
            'total_elementos': len(self.elementos_azuis) + len(self.elementos_zombies)
        }
"""
Módulo para exibir o tabuleiro no terminal (CLI)
"""
import os
import time
from typing import List

class TabuleiroCLI:
    def __init__(self):
        self.cores = {
            0: '⬜',  # Vazio
            1: '🔵',  # Elemento azul
            2: '🧟'   # Zombie
        }
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_tabuleiro(self, tabuleiro: List[List[int]], rodada: int = 0):
        """
        Exibe o tabuleiro no terminal com símbolos visuais
        
        Args:
            tabuleiro: Matrix 50x50 representando o jogo
            rodada: Número da rodada atual
        """
        self.limpar_tela()
        
        print(f"=== JOGO ZOMBIE - RODADA {rodada} ===")
        print("🔵 = Elemento Azul | 🧟 = Zombie | ⬜ = Vazio")
        print("Objetivo: Elementos azuis devem chegar à direita do tabuleiro!")
        print("-" * 60)
        
        # Exibe números das colunas (apenas algumas para referência)
        print("   ", end="")
        for j in range(0, 50, 10):
            print(f"{j:2d}", end="        ")
        print()
        
        # Exibe o tabuleiro linha por linha
        for i in range(len(tabuleiro)):
            # Número da linha
            print(f"{i:2d} ", end="")
            
            # Elementos da linha
            for j in range(len(tabuleiro[i])):
                print(self.cores[tabuleiro[i][j]], end="")
            
            print()  # Nova linha
        
        print("-" * 60)
        print("Pressione Ctrl+C para parar o jogo")
    
    def exibir_resultado(self, resultado: str, rodadas: int):
        """
        Exibe o resultado final do jogo
        
        Args:
            resultado: Mensagem do resultado
            rodadas: Número total de rodadas
        """
        self.limpar_tela()
        print("=" * 60)
        print("           RESULTADO FINAL")
        print("=" * 60)
        print(f"Resultado: {resultado}")
        print(f"Rodadas jogadas: {rodadas}")
        print("=" * 60)
    
    def pausar(self, segundos: float = 0.5):
        """Pausa a execução por alguns segundos"""
        time.sleep(segundos)
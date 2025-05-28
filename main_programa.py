"""
Programa principal - Executa o jogo zombie
"""
from tabuleiro_display import TabuleiroCLI
from jogo_logica import JogoZombie
import time
from threading import Thread

class GameRunner:
    def __init__(self):
        self.jogo = JogoZombie()
        self.display = TabuleiroCLI()
        self.executando = True
    
    def configurar_jogo(self):
        """Permite ao usuário configurar o jogo"""
        print("=== CONFIGURAÇÃO DO JOGO ===")
        print("Configuração padrão:")
        print("- Tabuleiro: 50x50")
        print("- Elementos azuis: 10")
        print("- Zombies: 5")
        
        usar_padrao = input("\nUsar configuração padrão? (s/n): ").lower().strip()
        
        if usar_padrao == 'n':
            try:
                num_azuis = int(input("Número de elementos azuis (1-20): "))
                num_azuis = max(1, min(20, num_azuis))
                
                num_zombies = int(input("Número de zombies (1-10): "))
                num_zombies = max(1, min(10, num_zombies))
                
                return num_azuis, num_zombies
            except ValueError:
                print("Valores inválidos, usando configuração padrão.")
                return 10, 5
        
        return 10, 5
    
    def executar_jogo(self):
        """Loop principal do jogo"""
        try:
            # Configuração
            num_azuis, num_zombies = self.configurar_jogo()
            
            # Inicialização
            self.jogo.inicializar_jogo(num_azuis, num_zombies)
            
            print(f"\nIniciando jogo com {num_azuis} elementos azuis e {num_zombies} zombies...")
            time.sleep(2)
            
            # Loop do jogo
            while self.executando:
                # Exibe o tabuleiro atual
                self.display.exibir_tabuleiro(self.jogo.tabuleiro, self.jogo.rodada)
                
                # Executa uma rodada
                fim_jogo, motivo = self.jogo.executar_rodada()
                
                # Verifica condições de fim
                if fim_jogo:
                    self.display.exibir_tabuleiro(self.jogo.tabuleiro, self.jogo.rodada)
                    self.display.pausar(1)
                    self.display.exibir_resultado(motivo, self.jogo.rodada)
                    break
                
                # Pausa entre rodadas
                self.display.pausar(0.3)
                
                # Limite de segurança para evitar loops infinitos
                if self.jogo.rodada > 1000:
                    self.display.exibir_resultado("JOGO INTERROMPIDO - MUITAS RODADAS", self.jogo.rodada)
                    break
        
        except KeyboardInterrupt:
            print("\n\nJogo interrompido pelo usuário.")
            estatisticas = self.jogo.obter_estatisticas()
            print(f"Estatísticas finais:")
            print(f"- Rodadas: {estatisticas['rodada']}")
            print(f"- Elementos azuis restantes: {estatisticas['elementos_azuis']}")
            print(f"- Zombies: {estatisticas['zombies']}")
        
        except Exception as e:
            print(f"Erro durante a execução: {e}")
        
        finally:
            print("Obrigado por jogar!")

def main():
    """Função principal"""
    print("🔵🧟 BEM-VINDO AO JOGO ZOMBIE! 🧟🔵")
    print()
    print("REGRAS:")
    print("- Elementos azuis (🔵) tentam chegar à direita do tabuleiro")
    print("- Zombies (🧟) infectam elementos azuis adjacentes")
    print("- O jogo termina quando todos viram zombies OU um azul chega à direita")
    print("- Todos os elementos se movem aleatoriamente a cada rodada")
    print()
    
    runner = GameRunner()
    runner.executar_jogo()

if __name__ == "__main__":
    main()
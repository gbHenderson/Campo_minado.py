# Aluno: Gabriel Henderson
# AD2: Programção com Interfaces Gráficas

from tkinter import *
from tkinter import messagebox
import random
janela = Tk()
tela_ini = Frame(janela, height=800, width=1800)
tela_jogo = Frame(janela, height=5000, width=5000, background="#a6949a")
jogo = Frame(tela_jogo, height=800, width=800, background="grey")


# Criação da classe do jogo.
class Jogo:
    # Função principal cujo, chama as outras funções e instância os elementos da partida.
    def __init__(self):
        self.foto = PhotoImage(file='bomba3.gif')
        self.dicas_lis = []
        self.minas = []
        self.minas_int = []
        self.jogadas = []
        self.m = -1
        self.resetadas = 0
        self.cont_dicas_real = 0
        self.muda_lis_dicas = 0
        self.cont_dicas2 = 0
        self.cont_dica = 0
        self.cont_dicas = 0
        self.vitoria = 1
        self.veio = False
        self.janela = janela
        self.tela_ini = tela_ini
        self.tela_jogo = tela_jogo
        self.jogo = jogo
        self.janela.title('Campo Minado')
        janela.state('zoomed')
        self.janela.resizable(False, False)
        janela.iconbitmap('bomba.ico')
        self.inicio()
        self.janela.mainloop()

    # Função da tela de ínicio, cujo é escolhida a dificuldade.
    def inicio(self):
        self.tela_ini.pack()
        Label(self.tela_ini, text="Campo Minado", font=("Javanese Text", 50)).place(relx=0.4, rely=0.05)
        Label(self.tela_ini, text="Escolha uma dificuldade:", font=("Arial", 20)).place(relx=0.3, rely=0.3)
        global dificuldade
        dificuldade = Entry(self.tela_ini)
        dificuldade.place(relx=0.47, rely=0.305, height=30)
        dificuldade.focus()
        enviar = Button(self.tela_ini, text="Começar", command=self.comeca)
        enviar.place(relx=0.55, rely=0.305)
        Label(self.tela_ini, text="OBS: A dificuldade deve ser um número inteiro que vai representar uma matriz quadrada",
              font=("Arial Italic", 20)).place(rely=0.5, relx=0.2)
        Label(self.tela_ini, text="Exemplo: A dificuldade 3 é uma matriz 3x3", font=("Arial Italic", 20))\
            .place(rely=0.55, relx=0.2)
        dificuldade.bind('<Return>', lambda e: self.comeca())

    # Função que gera as minas para a partida e coloca os valores numa lista.
    def gerar_minas(self, nivel):
        self.minas.clear()
        cont5 = 0
        # É criado um laço que cria casas aleatórias com a mina conforme a dificuldade.
        while cont5 < int(nivel):
            n1 = random.randint(1, int(nivel)*int(nivel))
            # Caso a casa já tenha bomba, sorteia outra casa.
            if "{}".format(n1) in self.minas:
                n1 = random.randint(1, int(nivel)*int(nivel))
                cont5 -= 1
            else:
                cord = "{}".format(n1)
                self.minas.append(cord)
                self.minas_int.append(int(cord))
            cont5 += 1

    # Função que cria a tela do jogo.
    def comeca(self):
        self.janela.configure(background="#a6949a")
        global nivel
        nivel = dificuldade.get()
        # Checa se a dificuldade foi preenchida.
        if nivel == "":
            messagebox.showerror("Erro", 'A dificuldade está vazia!')
        # Checa se a dificuldade é uma letra.
        if nivel.isalpha():
            messagebox.showerror("Erro", 'A dificuldade não pode ser em letras!')
        # Checa se a dificuldade é menor igual a 1.
        if int(nivel) <= 1:
            messagebox.showerror("Erro", 'A dificuldade não pode ser menor igual a 1!')
        # Caso a dificuldade seja um número é criado o layout do jogo com os botões e a tela.
        else:
            self.dicas = int(nivel) - 1
            # Fundo tela
            self.tela_ini.destroy()
            self.tela_jogo.pack()
            Label(self.tela_jogo, text="Faltam {} minas".format(nivel), font=("Arial Italic", 30), background="#a6949a")\
                .pack(pady=20)
            self.gera_jogo()
            # Botoes
            reinicia = Button(self.tela_jogo, text="Reset", font=("Arial Italic", 10), command=self.reseta)
            reinicia.place(y=100, x=150)
            sai = Button(self.tela_jogo, text="Sair", font=("Arial Italic", 10), command=self.sai)
            sai.place(y=100, x=50)
            global dica2
            dica2 = Button(self.tela_jogo, text="Dica", font=("Arial Italic", 10), command=self.dica)
            dica2.place(y=100, x=100)

    # Função caso aperte o botão "Sair".
    def sai(self):
        self.janela.destroy()

    # Função que chama o gerador de minas, ajusta o layout e gera a matriz com os botões para o jogador jogar.
    def gera_jogo(self):
        res_dica = Label(self.tela_jogo, text='Tem {} dicas!'.format(self.dicas), font=('arial', 25), background="#a6949a")
        res_dica.place(x=50, rely=0.91)
        self.gerar_minas(int(nivel))
        # Tela jogo.
        self.jogo.pack(pady=100)
        # Cria um laço que faz a matriz com botões enumerados da casa um até o quadrado da matriz.
        coluna = 1
        linha = 1
        for c in range(0, int(nivel)*int(nivel)):
            global botao
            botao = Button(jogo, bg='grey', text='+')
            botao.grid(row=linha, column=coluna, ipadx=5, ipady=2)
            # Chama uma função caso o jogador aperte qualquer botão
            botao['command'] = lambda selecionado = botao: self.botao_clicado(selecionado)
            if linha == int(nivel):
                coluna += 1
                linha = 0
            linha += 1

    # Função que faz os cálculos para dizer o número de minas ao redor, se o jogador perdeu ou se o jogador ganhou.
    def botao_clicado(self, b):
        cont = 0
        # Separa a classe do botão e deixa só o número do botão clicado para poder manipular o seu valor.
        casas = str(b)[23:]
        # Não existe o botão 1, começa apenas no 2. Então o botão 1 que tem nada após a casa 23 recebe o valor 1.
        if casas == '':
            casas = 1
        # Caso tenha resetados o jogo é feito esse cálculo para os valores dos botões corresponderem a valores da matriz
        if self.resetadas >= 1:
            casas = str(int(casas) - len(self.minas) * self.resetadas - self.cont_dicas2 - int(nivel) * int(nivel) * self.resetadas)
        # Condiconal para botões da dica serem manipulados para serem valores da matriz.
        if int(casas) > int(nivel) * int(nivel):
            try:
                self.m += 1
                casas = self.dicas_lis[self.m]
            except:
                pass
        if int(casas) > int(nivel) * int(nivel):
            pass
        if int(casas) not in self.jogadas and int(casas) <= int(nivel) * int(nivel):
            self.jogadas.append(int(casas))
        # Laço que faz o cálculo do botão apertado.
        acon = True
        for c in range(0, len(self.minas)):
            # Caso aperte numa casa com mina.
            if int(casas) == int(self.minas[c]):
                acon = False
                b['image'] = self.foto
                b['text'] = 'X'
                b['background'] = 'black'
                self.perdeu()
            if acon:
                # Bombas na primeira linha
                if (int(casas) - 1) % int(nivel) == 0:
                    if int(casas) + int(nivel) == int(self.minas[c]):
                        cont += 1
                    if int(casas) - int(nivel) == int(self.minas[c]):
                        cont += 1
                    if int(casas) + int(nivel) + 1 == int(self.minas[c]):
                        cont += 1
                    if int(casas) - int(nivel) + 1 == int(self.minas[c]):
                        cont += 1
                    if int(casas) + 1 == int(self.minas[c]):
                        cont += 1

                # Bombas na última linha
                elif int(casas) % int(nivel) == 0:
                    if int(casas) + int(nivel) == int(self.minas[c]):
                        cont += 1
                    if int(casas) - int(nivel) == int(self.minas[c]):
                        cont += 1
                    if int(casas) + int(nivel) - 1 == int(self.minas[c]):
                        cont += 1
                    if int(casas) - int(nivel) - 1 == int(self.minas[c]):
                        cont += 1
                    if int(casas) - 1 == int(self.minas[c]):
                        cont += 1

                # Restante das bombas
                else:
                    if int(casas) - 1 == int(self.minas[c]):
                        cont += 1
                    if int(casas) + 1 == int(self.minas[c]):
                        cont += 1
                    if int(casas) - (int(nivel) + 1) == int(self.minas[c]):
                        cont += 1
                    if int(casas) - int(nivel) == int(self.minas[c]):
                        cont += 1
                    if int(casas) - (int(nivel) - 1) == int(self.minas[c]):
                        cont += 1
                    if int(casas) + (int(nivel) + 1) == int(self.minas[c]):
                        cont += 1
                    if int(casas) + int(nivel) == int(self.minas[c]):
                        cont += 1
                    if int(casas) + (int(nivel) - 1) == int(self.minas[c]):
                        cont += 1
                b['text'] = '{}'.format(cont)
                b['background'] = 'green'
                acon = True
        # Faz o cálculo para ver se todas as casas sem minas foram apertadas e chama a função de vitória.
        if len(self.jogadas) == int(nivel) * int(nivel) - int(nivel):
            self.ganhou()

    # Função que cria uma mensagem na tela avisando que ganhou.
    def ganhou(self):
        ganhou_aviso = messagebox.askyesno("GANHOU!", 'Deseja jogar novamente?')
        if ganhou_aviso:
            self.reseta()
        if not ganhou_aviso:
            self.sai()

    # Função que cria uma mensagem na tela avisando que perdeu.
    def perdeu(self):
        self.mostra_bomba()
        perdeu_aviso = messagebox.askyesno("GAME OVER", 'Deseja jogar novamente?')
        if perdeu_aviso:
            self.reseta()
        if not perdeu_aviso:
            self.sai()

# Função que dá utilidade ao botão da dica.
    def dica(self):
        self.cont_dicas_real += 1
        res_dica = Label(self.tela_jogo, text='Tem {} dicas!'.format(self.dicas - 1), font=('arial', 25), background="#a6949a")
        res_dica.place(x=50, rely=0.9)
        # Verifica se ainda há dicas para o jogador, caso não tenha. É mostrado uma mensagem na tela.
        # As dicas são vão ao acordo de números de bombas possíveis, menos um número inteiro.
        if self.dicas == 0:
            self.veio = True
            global aca_dica
            aca_dica = Label(self.tela_jogo, text='Acabou as dicas!', font=('arial', 25), background="#a6949a")
            aca_dica.pack()
            dica2['state'] = DISABLED
        elif self.cont_dicas_real >= 2:
            res_dica = Label(self.tela_jogo, text='Tem {} dicas!'.format(self.dicas), font=('arial', 25),
                             background="#a6949a")
            res_dica.place(x=50, rely=0.9)
            if len(self.dicas_lis) == 0:
                pass
            if self.dicas_lis[self.muda_lis_dicas] in self.jogadas:
                self.cont_dicas_real = 1
                self.muda_lis_dicas += 1
            else:
                messagebox.showerror("Erro", 'Jogue na casa marcada antes de pedir mais dica.')
        if self.cont_dicas_real == 1:
            self.cont_dicas_real += 1
            res_dica = Label(self.tela_jogo, text='Tem {} dicas!'.format(self.dicas - 1), font=('arial', 25),
                             background="#a6949a")
            res_dica.place(x=50, rely=0.9)
            cont_loop = 0
            # Diminui o número de dicas e cria um laço para sortear uma casa sem mina.
            n11 = random.randint(1, int(nivel) * int(nivel))
            while True:
                # Caso sorteie uma casa numa casa que já tem mina, é gerado de novo.
                if "{}".format(n11) in self.minas:
                    while True:
                        n11 = random.randint(1, int(nivel) * int(nivel))
                        if '{}'.format(n11) not in self.minas:
                            break
                # Caso sorteie uma casa numa casa que já foi sorteada, gera de novo outra casa.
                if n11 in self.dicas_lis:
                    while True:
                        cont_loop += 0
                        n11 = random.randint(1, int(nivel) * int(nivel))
                        if n11 not in self.dicas_lis and '{}'.format(n11) not in self.minas:
                            break
                        if cont_loop > 100:
                            n11 = 0
                            break
                # Caso sorteie uma casa numa casa que já foi jogada, gera outra casa de novo.
                if n11 in self.jogadas:
                    while True:
                        cont_loop += 1
                        n11 = random.randint(1, int(nivel) * int(nivel))
                        if n11 not in self.jogadas and '{}'.format(n11) not in self.minas:
                            break
                        if cont_loop > 100:
                            n11 = 0
                            break
                else:
                    self.dicas -= 1
                    self.dicas_lis.append(n11)
                    break
            self.jogo.pack(pady=100)
            if n11 == 0:
                messagebox.showerror("Erro", 'Não é possível dar mais dicas!')
                dica2['state'] = DISABLED
            # Cria um botão azul e sem mina sobre os botões da matriz principal.
            coluna2 = 1
            linha2 = 1
            for c in range(0, int(nivel) * int(nivel)):
                if c == n11 - 1:
                    self.cont_dicas += 1
                    bo2 = Button(jogo, bg='lightblue', text='+')
                    bo2.grid(row=linha2, column=coluna2, ipadx=5, ipady=2)
                    bo2['command'] = lambda selecionado=bo2: self.botao_clicado((bo2))
                elif linha2 == int(nivel):
                    coluna2 += 1
                    linha2 = 0
                linha2 += 1

    # Função para mostrar todas as bombas do jogo, caso o jogador perca.
    def mostra_bomba(self):
        coluna3 = 1
        linha3 = 1
        for c in range(0, int(nivel) * int(nivel)):
            if len(self.minas_int) == 0:
                pass
            elif sorted(self.minas_int)[0] == c+1:
                bo3 = Button(jogo, bg='black', text='X', image=self.foto)
                bo3.grid(row=linha3, column=coluna3, ipadx=5, ipady=2)
                self.minas_int.remove(c+1)
            if linha3 == int(nivel):
                coluna3 += 1
                linha3 = 0
            linha3 += 1

    # Função para zerar todos os valores e resetar o jogo.
    def reseta(self):
        self.m = -1
        self.vitoria = 0
        self.dicas = int(nivel) - 1
        self.dicas_lis.clear()
        self.jogadas.clear()
        self.minas_int.clear()
        self.cont_dicas2 += self.cont_dicas
        self.cont_dicas = 0
        self.cont_dicas_real = 0
        self.muda_lis_dicas = 0
        self.resetadas += 1
        try:
            if self.veio:
                aca_dica.destroy()
                dica2['state'] = NORMAL
                self.gera_jogo()
            else:
                dica2['state'] = NORMAL
                self.gera_jogo()
        except:
            if self.veio:
                aca_dica.destroy()
                dica2['state'] = NORMAL
                self.gera_jogo()
            else:
                dica2['state'] = NORMAL
                self.gera_jogo()


Jogo()

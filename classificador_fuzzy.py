import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Configuração do sistema fuzzy
peso = ctrl.Antecedent(np.arange(0, 101, 1), 'peso')  # 0 a 100 kg
tamanho = ctrl.Antecedent(np.arange(0, 301, 10), 'tamanho')  # 0 a 300 litros
destino = ctrl.Consequent(np.arange(0, 101, 1), 'destino')

# Funções de pertinência refinadas para o peso (kg)
peso['leve'] = fuzz.trimf(peso.universe, [0, 0, 15])
peso['medio'] = fuzz.trimf(peso.universe, [10, 30, 50])
peso['pesado'] = fuzz.trimf(peso.universe, [40, 100, 100])

# Funções de pertinência refinadas para o volume (litros)
tamanho['pequeno'] = fuzz.trimf(tamanho.universe, [0, 0, 60])
tamanho['medio'] = fuzz.trimf(tamanho.universe, [50, 120, 180])
tamanho['grande'] = fuzz.trimf(tamanho.universe, [160, 300, 300])

# Funções de pertinência ajustadas para o destino
destino['motos'] = fuzz.trimf(destino.universe, [0, 0, 30])
destino['carros'] = fuzz.trimf(destino.universe, [25, 50, 70])
destino['caminhao'] = fuzz.trimf(destino.universe, [65, 100, 100])

# Regras fuzzy refinadas
regras = [
    ctrl.Rule(peso['leve'] & tamanho['pequeno'], destino['motos']),
    ctrl.Rule(peso['leve'] & tamanho['medio'], destino['carros']),
    ctrl.Rule(peso['leve'] & tamanho['grande'], destino['carros']),

    ctrl.Rule(peso['medio'] & tamanho['pequeno'], destino['carros']),
    ctrl.Rule(peso['medio'] & tamanho['medio'], destino['carros']),
    ctrl.Rule(peso['medio'] & tamanho['grande'], destino['caminhao']),

    ctrl.Rule(peso['pesado'] & tamanho['pequeno'], destino['carros']),
    ctrl.Rule(peso['pesado'] & tamanho['medio'], destino['caminhao']),
    ctrl.Rule(peso['pesado'] & tamanho['grande'], destino['caminhao']),
]

# Sistema fuzzy
sistema = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema)

# Função para processar os dados e exibir resultado
def calcular_destino():
    try:
        peso_val = float(entry_peso.get())
        tamanho_val = float(entry_tamanho.get())

        simulador.input['peso'] = peso_val
        simulador.input['tamanho'] = tamanho_val
        simulador.compute()

        resultado = simulador.output['destino']
        print(f"Peso inserido: {peso_val} kg, Volume inserido: {tamanho_val} L, Resultado fuzzy: {resultado:.2f}")

        if resultado < 30:
            destino_final = "Motos"
        elif resultado < 65:
            destino_final = "Carros"
        else:
            destino_final = "Caminhão"

        lbl_resultado.config(text=f"Destino sugerido: {destino_final} ({resultado:.2f})")

    except Exception as e:
        messagebox.showerror("Erro", f"Entrada inválida: {e}")

# Função para exibir o gráfico fuzzy
def mostrar_grafico():
    destino.view(sim=simulador)
    plt.show()

# Interface com Tkinter
janela = tk.Tk()
janela.title("Sistema de Logística Fuzzy")
janela.geometry("400x300")

tk.Label(janela, text="Peso (kg, de 0 a 100):").pack()
entry_peso = tk.Entry(janela)
entry_peso.pack()

tk.Label(janela, text="Volume do pacote (litros, até 300L):").pack()
entry_tamanho = tk.Entry(janela)
entry_tamanho.pack()

btn_calcular = tk.Button(janela, text="Calcular Destino", command=calcular_destino)
btn_calcular.pack(pady=10)

btn_grafico = tk.Button(janela, text="Mostrar Gráfico Fuzzy", command=mostrar_grafico)
btn_grafico.pack(pady=5)

lbl_resultado = tk.Label(janela, text="")
lbl_resultado.pack(pady=10)

janela.mainloop()

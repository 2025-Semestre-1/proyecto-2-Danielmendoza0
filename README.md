[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Et4r0lVo)
# [Proyecto2]
### Daniel Mendoza Morales 2025110674

### Estado del proyecto: [regular]
### Enlace del video:
Recordar que el video debe ser público para ser visto por el profesor



import tkinter as tk
import random

# Variables globales
tablero = []
canvas = None
PIEZAS = [
    [[1, 1], [1, 1]],        #O
    [[1, 1, 1, 1]],          # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],   # Z
    [[1,0,1], [1,1,1]],       # u
    [[0,1,0], [1,1,1],[0,1,0]]] # +


def mostrar_tablero():
    global canvas, tablero
    canvas.delete("all")

    tablero = [] 
    with open("matriz.txt", "r") as archivo:
        for linea in archivo:
            tablero.append(linea.strip().split(" "))

    for fila in range(len(tablero)):
        for col in range(len(tablero[0])):
            valor = tablero[fila][col]
            x1 = col * 20
            y1 = fila * 20
            x2 = x1 + 20
            y2 = y1 + 20

            color = "gray" if valor == "+" else "white"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    pieza_actual = random.choice(PIEZAS)
    fila_inicio = 1
    col_inicio = 4
    dibujar_pieza_matriz(fila_inicio, col_inicio, pieza_actual)


def dibujar_pieza_matriz(fila_base, col_base, pieza):
    for i in range(len(pieza)):
        for j in range(len(pieza[i])):
            if pieza[i][j] == 1:
                x1 = (col_base + j) * 20
                y1 = (fila_base + i) * 20
                x2 = x1 + 20
                y2 = y1 + 20
                canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="black")



ventana = tk.Tk()
ventana.title("TETRIS")
ventana.geometry("240x440")
ventana.resizable(0, 0)
ventana.config(bg="black")


canvas = tk.Canvas(ventana, width=240, height=440, bg="black")
canvas.pack()


mostrar_tablero()
ventana.mainloop()

import tkinter
import tkinter as tk
import random
from tkinter import messagebox

# Variables globaless
puntaje = 0
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

colores = ["cyan", "blue", "orange", "yellow", "green", "purple", "red"]

color_actual = random.choice(colores)
pieza_actual = random.choice(PIEZAS)
pos_fila = 1
pos_col = 4
nombreJugador = ""
velocidad = 500

ventana_datos = None



def mostrar_tablero():
    """
    Dibuja en el canvas el tablero actual leído desde el archivo "matriz.txt".
    Entrada: Ninguna
    Salida: Representación visual del tablero en el canvas.
    Restricciones: El archivo debe existir y tener el formato correcto.
    """


    global canvas, tablero, pieza_actual
    canvas.delete("all")
    tablero = []
    with open("matriz.txt", "r") as archivo:
        for linea in archivo:
            tablero = tablero + [linea.strip().split(",")]

    for fila in range(len(tablero)):
        for col in range(len(tablero[0])):
            valor = tablero[fila][col]
            x1 = col * 20
            y1 = fila * 20
            x2 = x1 + 20
            y2 = y1 + 20

            if valor == "+":
                color = "gray20"
            elif valor == "1":
                color = "gray61"
            else:
                color = "black"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

def guardar_partida():
    """
    Guarda el estado actual del juego en el archivo "partidaGuardada.txt".
    Entrada: Ninguna
    Salida: Archivo actualizado con los datos del juego
    Restricciones: nombreJugador debe estar definido, y el tablero debe tener datos válidos.
    """

    global puntaje,pos_fila,pos_col,nombreJugador,tablero,velocidad
    with open ("partidaGuardada.txt",'w') as archivo:
        archivo.write(nombreJugador + "\n")
        archivo.write(str(puntaje) + "\n")
        archivo.write(str(pos_fila) + "\n")
        archivo.write(str(pos_col) + "\n")
        archivo.write(str(velocidad) + "\n")

        for fila in tablero:
            archivo.write(",".join(fila) + "\n")

    messagebox.showinfo(title=":)", message="El juego de "+ nombreJugador + " se guardo correctamente")
def mostrar_controles():
    """
    Muestra una ventana con los controles del juego (teclas para moverse y rotar).
    Entrada: Ninguna
    Salida: Ventana emergente con una explicación de los controles
    """
    controles_ventana = tk.Toplevel()
    controles_ventana.title("Controles del Juego")
    controles_ventana.geometry("300x300")
    controles_ventana.configure(bg="black")
    controles_ventana.resizable(0,0)

    titulo = tk.Label(controles_ventana, text="Controles del Tetris", font=("Arial", 16, "bold"), fg="white", bg="black")
    titulo.pack(pady=10)

    movimiento = tk.Label(controles_ventana, text="Movimiento:\n🡰  Izquierda\n🡲  Derecha\n🡳  Abajo", font=("Arial", 12), fg="white", bg="black", justify="left")
    movimiento.pack(pady=5)

    rotacion = tk.Label(controles_ventana, text="Rotación:\n🡱  Rotar pieza", font=("Arial", 12), fg="white", bg="black", justify="left")
    rotacion.pack(pady=5)

    cerrar = tk.Button(controles_ventana, text="Cerrar", command=controles_ventana.destroy, font=("Arial", 12))
    cerrar.pack(pady=10)

def salir():
    messagebox.showinfo("Fin del Juego", f"¡{nombreJugador} Tu puntuacion fue: {puntaje}")
    guardar_puntuacion()
    ventana.quit()

def datos():
    """
   Muestra los datos del jugador (puntaje y botones) si no se ha creado ya.
   Entrada: Ninguna directa (usa globales: puntaje, ventana, ventana_datos, jugador_puntuaje_label)
   Salida: Muestra el puntaje y botones de "Guardar partida" y "Salir"
   Restricciones: Solo crea el panel si no existe, si ya existe actualiza el puntaje
    """
    global puntaje, ventana_datos, jugador_puntuaje_label

    if ventana_datos is None:
        ventana_datos = tk.LabelFrame(ventana, bg="Black", fg="white", text="Datos")
        ventana_datos.place(y=450,x=10, height=90,width=220)

        texto = tk.Label(ventana_datos, bg="black", fg="white", text="Puntuacion:")
        texto.place(x=10, y= 5)

        jugador_puntuaje_label = tk.Label(ventana_datos, bg="black",fg='white', text=puntaje)
        jugador_puntuaje_label.place(x=30, y=40)

        boton1 = tk.Button(ventana_datos, text="Guardar partida", command=guardar_partida)
        boton1.place(x=110,y=10)

        boton2 = tk.Button(ventana_datos, text="salir", command=salir)
        boton2.place(x=173, y=40)

        boton3 = tk.Button(ventana_datos, text="Controles", command=mostrar_controles)
        boton3.place(x=110, y=40)

    else:
        jugador_puntuaje_label.config(text=puntaje)


def mostrar_ranking():
    """
    Muestra una ventana emergente con el top 10 de puntuaciones desde un archivo.
    Entrada: Ninguna directa (lee archivo "puntuaciones.txt")
    Salida: Ventana nueva con los 10 jugadores con más puntos
    Restricciones: El archivo debe tener formato 'nombre,puntaje' por línea y puntaje debe ser convertible a entero
    """

    with open("puntuaciones.txt", "r") as archivo:
        lineas = archivo.readlines()

    jugadores = []
    for linea in lineas:
        partes = linea.strip().split(",")
        nombre = partes[0]
        puntuacion = int(partes[1])
        jugadores.append((nombre, puntuacion))

    jugadores.sort(key=lambda x: x[1], reverse=True)

    ventana = tk.Toplevel()
    ventana.title("Ranking - Top 10")
    ventana.geometry("300x300")

    titulo = tk.Label(ventana, text=" Top 10 Jugadores ", font=("Arial", 14, "bold"))
    titulo.pack(pady=10)

    for i, (nombre, puntuacion) in enumerate(jugadores[:10], start=1):
        texto = f"{i}.{nombre} - {puntuacion} pts"
        etiqueta = tk.Label(ventana, text=texto, font=("Arial", 12))
        etiqueta.pack(anchor="w", padx=20)


def dibujar_pieza_matriz(fila_base, col_base, pieza):
    """
    Dibuja la pieza actual en la matriz visual del juego (canvas).
    Entrada: fila_base (int), col_base (int), pieza (lista de listas con 0 y 1)
    Salida: Dibujo de la pieza en el canvas del juego
    Restricciones: pieza debe estar bien formada y contener solo valores 0 o 1
    """
    global color_actual
    for i in range(len(pieza)):
        for j in range(len(pieza[i])):
            if pieza[i][j] == 1:
                x1 = (col_base + j) * 20
                y1 = (fila_base + i) * 20
                x2 = x1 + 20
                y2 = y1 + 20
                canvas.create_rectangle(x1, y1, x2, y2, fill=color_actual, outline="black")



def eliminar_fila_llena():
    """
    Elimina filas llenas en el tablero, actualiza el puntaje y redibuja el juego.
    Entrada: Ninguna directa (usa globales: tablero, puntaje, pieza_actual, pos_fila, pos_col)
    Salida: Tablero actualizado, nuevo puntaje, dibujo actualizado
    Restricciones: No elimina filas que contengan '+', guarda estado en 'matriz.txt'
    """
    global tablero, puntaje

    filas_eliminadas = 0
    filas_a_mantener = []

    for fila in range(len(tablero) - 2, 0, -1):
        completa = True
        for col in range(1, len(tablero[fila]) - 1):
            if tablero[fila][col] != "1":
                completa = False
                break
            if tablero[fila][col] == "+":
                fila_puede_eliminarse = False
                break
        if completa:
            filas_eliminadas += 1
        else:
            filas_a_mantener.insert(0, tablero[fila])

    nuevo_tablero = []
    nuevo_tablero.append(tablero[0])

    for _ in range(filas_eliminadas):
        nuevo_tablero.append(["+"] + ["0"] * 10 + ["+"])


    nuevo_tablero.extend(filas_a_mantener)
    nuevo_tablero.append(tablero[len(tablero) - 1])

    tablero = nuevo_tablero
    puntaje += filas_eliminadas * 100
    actualizar_velocidad()

    with open("matriz.txt", "w") as archivo:
        for linea in tablero:
            archivo.write(",".join(linea) + "\n")
    datos()
    mostrar_tablero()
    dibujar_pieza_matriz(pos_fila,pos_col,pieza_actual)


def actualizar_velocidad():
    """
   Ajusta la velocidad de caída de las piezas según el puntaje actual.
   Entrada: Ninguna (usa variable global puntaje)
   Salida: Modifica variable global velocidad
   Restricciones: velocidad mínima es 100 ms
    """
    global velocidad, puntaje
    #muy loco llegar a los 1200
    if puntaje >= 1200:
        velocidad = 100


    elif puntaje >= 900:
        velocidad = 200
    elif puntaje >= 600:
        velocidad = 300
    elif puntaje >= 300:
        velocidad = 400
    else:
        velocidad = 500


def se_puede_mover(delta_fila, delta_col):
    """
   Determina si la pieza puede moverse a una posición nueva sin colisionar.
   Entrada: delta_fila (int), delta_col (int)
   Salida: True si el movimiento es válido, False si no
    Restricciones: No debe salirse del tablero o tocar obstáculos
    """

    global pos_fila, pos_col, pieza_actual

    nueva_fila = pos_fila + delta_fila
    nueva_col = pos_col + delta_col

    for i in range(len(pieza_actual)):
        for j in range(len(pieza_actual[i])):
            if pieza_actual[i][j] == 1:
                fila_real = nueva_fila + i
                col_real = nueva_col + j

                if col_real < 1 or col_real > 10 or fila_real > 20:
                    return False
    return True

def colision_abajo(delta_fila, delta_col):
    """
   Verifica si hay colisión en la parte inferior de la pieza al moverla.
   Entrada: delta_fila (int), delta_col (int)
   Salida: True si hay colisión, False si no
   Restricciones: Debe tener acceso a la matriz del tablero
    """

    global pos_fila, pos_col, pieza_actual

    nueva_fila = pos_fila + delta_fila
    nueva_col = pos_col + delta_col
    for i in range(len(pieza_actual)):
        for j in range(len(pieza_actual[i])):
            if pieza_actual[i][j] == 1:
                fila_real = nueva_fila + i
                col_real = nueva_col + j

                if fila_real >= 21:
                    return True

                if tablero[fila_real][col_real] == "1" or tablero[fila_real][col_real] == "+":
                    return True
    return False

def colison_lateral(delta_col):
    """
    Verifica si al mover lateralmente la pieza, colisiona con bloques ya colocados.
    Entrada: delta_col (int)
    Salida: True si hay colisión, False si no
    Restricciones: Solo detecta colisiones horizontales
    """

    global pos_fila, pos_col, pieza_actual

    nueva_col = pos_col + delta_col

    for i in range(len(pieza_actual)):
        for j in range(len(pieza_actual[i])):
            if pieza_actual[i][j] == 1:
                fila_real = pos_fila + i
                col_real = nueva_col + j

                if tablero[fila_real][col_real] == "1"or tablero[fila_real][col_real] == "+":
                    return True
    return False


def bloquear():
    """
    Coloca la pieza actual en el tablero como fija y genera una nueva pieza.
    Entrada: Ninguna
    Salida: Actualiza el tablero, puntaje, y color
    Restricciones: Verifica fin del juego al terminar
    """
    global pos_fila, pos_col, pieza_actual,tablero,color_actual,puntaje
    for i in range(len(pieza_actual)):
        for j in range(len(pieza_actual[i])):
            if pieza_actual[i][j] == 1:
                fila_real = pos_fila + i
                col_real = pos_col + j
                tablero[fila_real][col_real] = "1"

    pieza_actual = random.choice(PIEZAS)
    color_actual = random.choice(colores)
    pos_fila = 1
    pos_col = 4

    with open("matriz.txt","w") as archivo:
        for linea in tablero:
            archivo.write(",".join(linea) + "\n")

    eliminar_fila_llena()
    mostrar_tablero()
    dibujar_pieza_matriz(pos_fila, pos_col, pieza_actual)


    if verificar_fin_juego():
        return

def mover_figura(columna_x, fila_y):
    """
   Mueve la pieza actual una cantidad determinada en columnas y filas.
   Entrada: columna_x (int), fila_y (int)
   Salida: Mueve la pieza y actualiza el tablero
   Restricciones: Solo se mueve si se puede mover
    """
    global pos_fila,pos_col, pieza_actual
    if se_puede_mover(fila_y, columna_x):
        pos_fila += fila_y
        pos_col += columna_x
        mostrar_tablero()
        dibujar_pieza_matriz(pos_fila, pos_col, pieza_actual)


def bajar_automaticamente():
    """
   Controla la caída automática de la pieza actual.
   Entrada: Ninguna
   Salida: Reprograma su llamada a sí misma usando after()
    """


    global velocidad
    if not colision_abajo(1, 0):
        mover_figura(0, 1)
    else:
        bloquear()

    ventana.after(velocidad, bajar_automaticamente)


# Funciones para cada direccioen

def mover_izquierda(evento):
    """
   Evento de teclado para mover la pieza una columna a la izquierda.
   Entrada: evento de teclado
   Salida: Actualiza la posición de la pieza
   Restricciones: Solo se mueve si no hay colisión lateral
    """
    if not colison_lateral(-1):
        mover_figura(-1,0)

def mover_derecha(evento):
    """
    Evento de teclado para mover la pieza una columna a la derecha.
    Entrada: evento de teclado
    Salida: Actualiza la posición de la pieza
    Restricciones: Solo se mueve si no hay colisión lateral
    """
    if not colison_lateral(1):
        mover_figura(1, 0)

def mover_abajo(evento):
    """
    Evento de teclado para mover la pieza una fila hacia abajo manualmente.
    Entrada: evento de teclado
    Salida: Actualiza o bloquea la pieza
    Restricciones: Se bloquea si hay colisión al intentar mover abajo
    """
    if not colision_abajo(1,0):
        mover_figura(0, 1)
    else:
        bloquear()

def rotar_pieza(evento):
    """
    Evento de teclado para rotar la pieza actual 90 grados.
    Entrada: evento de teclado
    Salida: Actualiza la forma de la pieza si es posible
    Restricciones: No rota si colisiona o se sale del tablero
    """
    global pieza_actual, pos_fila, pos_col, tablero
    if pieza_actual == [[1, 1], [1, 1]]:
        return

    nueva_pieza = []
    for i in range(len(pieza_actual[0])):
        nueva_fila = []
        for j in range(len(pieza_actual) - 1, -1, -1):
            nueva_fila = nueva_fila + [pieza_actual[j][i]]
        nueva_pieza = nueva_pieza + [nueva_fila]

    puede_rotar = True
    for i in range(len(nueva_pieza)):
        for j in range(len(nueva_pieza[i])):
            if nueva_pieza[i][j] == 1:
                fila_real = pos_fila + i
                col_real = pos_col + j

                if col_real < 1 or col_real > 10 or fila_real > 20:
                    puede_rotar = False
                    break

                if tablero[fila_real][col_real] == "1" or tablero[fila_real][col_real] == "+":
                    puede_rotar = False
                    break
        if not puede_rotar:
            break

    if puede_rotar:
        pieza_actual = nueva_pieza
        mostrar_tablero()
        dibujar_pieza_matriz(pos_fila, pos_col, pieza_actual)


def verificar_fin_juego():
    """
   Verifica si el juego debe terminar por colisión en la fila superior.
   Entrada: Ninguna
   Salida: True si el juego termina, False si no
   Restricciones: Depende del estado de la fila 1 del tablero
    """

    global tablero, nombreJugador, puntaje

    for col in range(1, len(tablero[1]) - 1):
        if tablero[1][col] == "1":
            messagebox.showinfo("Fin del Juego", f"¡Game Over, {nombreJugador} Tu puntuacion fue: {puntaje}")
            guardar_puntuacion()

            with open("partidaGuardada.txt", "w") as archivo:
                archivo.write("1")

            ventana.quit()
            return True
    return False

def guardar_puntuacion():
    """
    Guarda el nombre del jugador y su puntaje actual en un archivo.
    Entrada: Ninguna directa (usa globales: nombreJugador, puntaje)
    Salida: Línea agregada en 'puntuaciones.txt' con formato 'nombre,puntaje'
    Restricciones: nombreJugador debe estar definido y puntaje debe ser entero
    """
    with open("puntuaciones.txt", "a") as archivo_puntuaciones:
        archivo_puntuaciones.write(f"{nombreJugador},{puntaje}\n")


def nuevo_juego():
    """
    Inicia una nueva partida con tablero limpio, pieza nueva y puntaje en 0.
    Entrada: Ninguna directa (usa y modifica varias globales: nombreJugador, tablero, puntaje, etc.)
    Salida: Interfaz reiniciada, juego listo para comenzar
    Restricciones: nombreJugador no puede estar vacío, sino se muestra error
    """
    global puntaje, pos_fila, pos_col, pieza_actual, color_actual, tablero,nombreJugador,velocidad

    if nombreJugador == "":
        messagebox.showerror(title="Error", message="ingrese su nombre antes de jugar")
        return

    velocidad = 500
    puntaje = 0
    pos_fila = 1
    pos_col = 4
    pieza_actual = random.choice(PIEZAS)
    color_actual = random.choice(colores)

    #tablero que se puede modificar para agregar los obstaculos
    tablero_inicial = [
        ["+", "+", "+", "+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "+", "+", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+wee", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "+"],
        ["+", "+", "+", "+", "+", "+", "+", "+", "+", "+", "+", "+"]
    ]

    with open("matriz.txt", "w") as archivo:
        for linea in tablero_inicial:
            archivo.write(",".join(linea) + "\n")


    for widget in ventana.winfo_children():
        widget.destroy()

    global canvas
    canvas = tk.Canvas(ventana, width=240, height=440, bg="black")
    canvas.pack()

    ventana.bind('<Left>', mover_izquierda)
    ventana.bind('<Right>', mover_derecha)
    ventana.bind('<Down>', mover_abajo)
    ventana.bind('<Up>', rotar_pieza)

    datos()
    mostrar_tablero()
    dibujar_pieza_matriz(pos_fila, pos_col, pieza_actual)
    bajar_automaticamente()

def reanudar_juego():
    """
    Carga una partida previamente guardada desde archivo y reinicia el estado del juego.
    Entrada: Ninguna directa (lee archivo 'partidaGuardada.txt')
    Salida: Juego restaurado al estado anterior con tablero y datos cargados
    Restricciones: El archivo debe contener datos válidos si es inválido, se muestra error
    """

    global puntaje, pos_fila, pos_col, pieza_actual, tablero,nombreJugador,velocidad

    with open("partidaGuardada.txt", "r") as verificacion:
        verificador = verificacion.readline()
        if verificador == "1":
            messagebox.showerror(title="ERROR", message="ERROR: no hay una partida guardada")
            return


    with open("partidaGuardada.txt", "r") as archivo:
        lineas = archivo.readlines()

    nombreJugador = lineas[0].strip()
    puntaje = int(lineas[1].strip())
    pos_fila = int(lineas[2].strip())
    pos_col = int(lineas[3].strip())
    velocidad = int(lineas[4].strip())

    tablero = []
    for linea in lineas[5:]:
        fila = linea.strip().split(",")
        tablero = tablero + [fila]


    with open("matriz.txt", "w") as archivo:
        for linea in tablero:
            archivo.write(",".join(linea) + "\n")


    for widget in ventana.winfo_children():
        widget.destroy()

    global canvas
    canvas = tk.Canvas(ventana, width=240, height=440, bg="black")
    canvas.pack()


    ventana.bind('<Left>', mover_izquierda)
    ventana.bind('<Right>', mover_derecha)
    ventana.bind('<Down>', mover_abajo)
    ventana.bind('<Up>', rotar_pieza)

    datos()
    mostrar_tablero()
    dibujar_pieza_matriz(pos_fila, pos_col, pieza_actual)
    bajar_automaticamente()




def menu():
    """
    Muestra el menú principal del juego con opciones para ingresar nombre, jugar, reanudar o salir.
    Entrada: Ninguna directa (define widgets en la ventana principal)
    Salida: Interfaz gráfica con botones y campo de entrada de nombre
    Restricciones: nombre no puede estar vacío al intentar guardarlo
    """

    def guardar_nombre():
        global nombreJugador

        nombreJugador = nombreEntry.get()
        if nombreJugador == "":
            messagebox.showerror(title="Error",message="El nombre no puede estar vacio")
            return
        messagebox.showinfo(title="Guardado", message="El nombre se guardo correctamente")

    for widget in ventana.winfo_children():
        widget.destroy()

    global canvas

    menu_frame = tk.Frame(ventana, bg="black")
    menu_frame.pack(expand=True)

    title_label = tk.Label(menu_frame, text="TETRIS", font=("Arial", 24, "bold"), fg="white", bg="black")
    title_label.pack(pady=20)

    nombreLabel = tk.Label(menu_frame, text="Ingrese su nombre", font= ("Arial", 14, "bold"),fg="white", bg="black")
    nombreLabel.pack(pady=10)

    nombreEntry = tk.Entry(menu_frame, font=("Arial",14,"bold"),fg="white", bg="black")
    nombreEntry.pack(pady=10)

    botonguardar = tk.Button(menu_frame, text="Guardar nombre", command=guardar_nombre,font=("Arial", 14), width=15, height=2,fg="white", bg="black")
    botonguardar.pack(pady=5)

    boton_jugar = tk.Button(menu_frame, text="Nuevo juego", command=nuevo_juego, font=("Arial", 14), width=15, height=2,fg="white", bg="black")
    boton_jugar.pack(pady=10)

    boton_reanudar = tk.Button(menu_frame, text="Reanudar partida", command=reanudar_juego, font=("Arial", 14), width=15, height=2,fg="white", bg="black")
    boton_reanudar.pack(pady=10)

    boton_rank = tk.Button(menu_frame, text="ver ranking", command=mostrar_ranking, font=("Arial", 14),width=15, height=2,fg="white", bg="black")
    boton_rank.pack(pady=10)


    boton_salir = tk.Button(menu_frame, text="Salir", command=ventana.quit, font=("Arial", 14), width=15, height=2,fg="white", bg="black")
    boton_salir.pack(pady=10)




ventana = tk.Tk()
ventana.title("TETRIS")
ventana.geometry("240x550")
ventana.config(bg="black")
ventana.resizable(0,0)


menu()
ventana.mainloop()


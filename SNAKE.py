import turtle
import time
import random

# Importas las fábricas que generan diferentes tipos de comida para la serpiente
from fabrica.fabrica_fit import FabricaComidaFit
from fabrica.fabrica_venenosa import FabricaComidaVenenosa
from fabrica.fabrica_grasa import FabricaComidaGrasa
from fabrica.fabrica_reyes import FabricaComidaReyes

# Configuración de la ventana principal del juego
wn = turtle.Screen()
wn.title("Snake con Abstract Factory")  # Título de la ventana
wn.bgcolor("black")                     # Fondo negro
wn.setup(width=600, height=600)        # Tamaño de la ventana
wn.tracer(0)                           # Desactiva la actualización automática para controlar cuándo refrescar

# Creación inicial de la serpiente con 3 segmentos blancos cuadrados
serpiente = [turtle.Turtle(shape="square") for _ in range(3)]
for segmento in serpiente:
    segmento.penup()                   # Para que no deje rastro al moverse
    segmento.color("white")            # Color blanco

direccion = "stop"  # Dirección inicial (serpiente está quieta)
puntaje = 0        # Puntuación inicial
velocidad = 0.1    # Velocidad inicial del juego (más bajo es más rápido)

# Configuración del marcador de puntaje en pantalla
pen = turtle.Turtle()
pen.hideturtle()   # Oculta el cursor que dibuja
pen.penup()
pen.color("white")
pen.goto(0, 260)   # Posición en la parte superior de la ventana
pen.write("Puntaje: 0", align="center", font=("Courier", 24, "normal"))  # Texto inicial

# Lista con las fábricas de comida disponibles
fabricas = [
    FabricaComidaFit(),
    FabricaComidaVenenosa(),
    FabricaComidaGrasa(),
    FabricaComidaReyes()
]

# Creación del objeto comida, que la serpiente debe comer
comida = turtle.Turtle()
comida.penup()
comida.shape("circle")

comida_tipo = None  # Variable para almacenar el tipo actual de comida

# Función para generar una nueva comida en posición aleatoria y de tipo aleatorio
def nueva_comida():
    global comida_tipo
    comida_tipo = random.choice(fabricas).crear_comida()  # Crear comida de una fábrica aleatoria
    comida.color(comida_tipo.color)                       # Cambiar color según tipo
    comida.goto(random.randint(-280, 280), random.randint(-280, 280))  # Posición aleatoria

nueva_comida()  # Llamada inicial para colocar la primera comida

# Función para mover la cabeza de la serpiente según la dirección actual
def mover():
    x = serpiente[0].xcor()
    y = serpiente[0].ycor()
    if direccion == "up":
        serpiente[0].sety(y + 20)
    elif direccion == "down":
        serpiente[0].sety(y - 20)
    elif direccion == "left":
        serpiente[0].setx(x - 20)
    elif direccion == "right":
        serpiente[0].setx(x + 20)

# Funciones para cambiar la dirección de la serpiente, evitando que pueda ir en dirección opuesta
def ir_arriba():
    global direccion
    if direccion != "down":
        direccion = "up"

def ir_abajo():
    global direccion
    if direccion != "up":
        direccion = "down"

def ir_izquierda():
    global direccion
    if direccion != "right":
        direccion = "left"

def ir_derecha():
    global direccion
    if direccion != "left":
        direccion = "right"

# Registrar las teclas para controlar la serpiente
wn.listen()
wn.onkey(ir_arriba, "Up")
wn.onkey(ir_abajo, "Down")
wn.onkey(ir_izquierda, "Left")
wn.onkey(ir_derecha, "Right")

# Bucle principal del juego que se ejecuta continuamente
while True:
    wn.update()  # Actualiza la pantalla (porque wn.tracer(0) está desactivado)
    mover()      # Mueve la cabeza según la dirección

    # Mueve el cuerpo de la serpiente, cada segmento a la posición del segmento anterior
    for i in range(len(serpiente) - 1, 0, -1):
        x = serpiente[i - 1].xcor()
        y = serpiente[i - 1].ycor()
        serpiente[i].goto(x, y)

    # Verifica si la serpiente comió la comida (distancia menor a 20)
    if serpiente[0].distance(comida) < 20:
        efecto = comida_tipo.efecto  # Obtiene el efecto especial de la comida
        puntaje += comida_tipo.puntaje  # Suma puntaje según la comida

        # Según el efecto, realiza una acción
        if efecto == "normal":  # Comida Fit: agrega un segmento
            nuevo = turtle.Turtle(shape="square")
            nuevo.color("white")
            nuevo.penup()
            serpiente.append(nuevo)

        elif efecto == "reduce" and len(serpiente) > 1:  # Comida venenosa: quita un segmento si puede
            eliminado = serpiente.pop()
            eliminado.hideturtle()
            eliminado.clear()

        elif efecto == "lenta":  # Comida grasosa: aumenta la velocidad (disminuye velocidad)
            velocidad += 0.05
            nuevo = turtle.Turtle(shape="square")
            nuevo.color("white")
            nuevo.penup()
            serpiente.append(nuevo)

        elif efecto == "rapida":  # Comida reyes: disminuye la velocidad (aumenta rapidez)
            velocidad = max(0.05, velocidad - 0.02)
            nuevo = turtle.Turtle(shape="square")
            nuevo.color("white")
            nuevo.penup()
            serpiente.append(nuevo)

        # Actualiza el puntaje en pantalla
        pen.clear()
        pen.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))
        nueva_comida()  # Genera nueva comida

    # Detecta si la serpiente choca con los bordes
    x = serpiente[0].xcor()
    y = serpiente[0].ycor()
    if abs(x) > 290 or abs(y) > 290:
        # Pregunta al usuario si quiere jugar otra vez
        respuesta = turtle.textinput("¡Has perdido!", "¿Deseas jugar otra vez? (si / no)")
        if respuesta and respuesta.lower() == "si":
            # Limpia la serpiente antigua y la reinicia
            for segmento in serpiente:
                segmento.goto(1000, 1000)  # Mueve fuera de pantalla
                segmento.clear()
                segmento.hideturtle()
            serpiente.clear()
            serpiente = [turtle.Turtle(shape="square") for _ in range(3)]
            for segmento in serpiente:
                segmento.penup()
                segmento.color("white")
            serpiente[0].goto(0, 0)
            direccion = "stop"
            puntaje = 0
            velocidad = 0.1
            pen.clear()
            pen.write("Puntaje: 0", align="center", font=("Courier", 24, "normal"))
            nueva_comida()
        else:
            wn.bye()  # Cierra la ventana y termina el programa
            break

    time.sleep(velocidad)  # Pausa para controlar la velocidad del juego

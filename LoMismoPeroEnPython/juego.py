import tkinter as tk
import random
import sqlite3

class Pokemon:
    def __init__(self, nombre, tipo, salud, ataque):
        self.nombre = nombre
        self.tipo = tipo
        self.salud = salud
        self.ataque = ataque
        self.nivel = 1
        self.experiencia = 0
        self.turno = False

    def recibir_danio(self, danio):
        self.salud -= danio

    def esta_vivo(self):
        return self.salud > 0

    def atacar_oponente(self, oponente):
        danio = random.randint(self.ataque // 2, self.ataque)
        oponente.recibir_danio(danio)

    def ataque_especial(self, oponente):
        danio = random.randint(self.ataque, self.ataque * 2)
        oponente.recibir_danio(danio)

    def curarse(self):
        cantidad_curacion = random.randint(10, 20)
        self.salud += cantidad_curacion

    def ganar_experiencia(self, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= self.nivel * 10:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.experiencia = 0
        self.salud += 10
        self.ataque += 5

def finalizar_turno():
    pokemon_jugador.turno = not pokemon_jugador.turno
    pokemon_oponente.turno = not pokemon_oponente.turno
    actualizar_estado_botones()
    if pokemon_jugador.turno:
        resultado_label.config(text=f"Turno de {pokemon_jugador.nombre}")
    else:
        resultado_label.config(text=f"Turno de {pokemon_oponente.nombre}")

def atacar():
    if pokemon_jugador.turno:
        pokemon_jugador.atacar_oponente(pokemon_oponente)
    else:
        pokemon_oponente.atacar_oponente(pokemon_jugador)
    pokemon_jugador.ganar_experiencia(1)
    pokemon_oponente.ganar_experiencia(1)
    actualizar_salud_etiquetas()
    comprobar_fin_del_juego()

def ataque_especial():
    if pokemon_jugador.turno:
        pokemon_jugador.ataque_especial(pokemon_oponente)
    else:
        pokemon_oponente.ataque_especial(pokemon_jugador)
    pokemon_jugador.ganar_experiencia(2)
    pokemon_oponente.ganar_experiencia(2)
    actualizar_salud_etiquetas()
    comprobar_fin_del_juego()

def curarse():
    if pokemon_jugador.turno:
        pokemon_jugador.curarse()
    else:
        pokemon_oponente.curarse()
    actualizar_salud_etiquetas()
    finalizar_turno()

def comprobar_fin_del_juego():
    if not pokemon_oponente.esta_vivo():
        resultado = f"{pokemon_jugador.nombre} gana la batalla!"
        resultado_label.config(text=resultado)
        guardar_resultado(pokemon_jugador.nombre, pokemon_oponente.nombre, resultado)
        inhabilitar_botones()
    elif not pokemon_jugador.esta_vivo():
        resultado = f"{pokemon_oponente.nombre} gana la batalla!"
        resultado_label.config(text=resultado)
        guardar_resultado(pokemon_jugador.nombre, pokemon_oponente.nombre, resultado)
        inhabilitar_botones()

def actualizar_salud_etiquetas():
    salud_label_jugador.config(text=f"{pokemon_jugador.nombre} ({pokemon_jugador.tipo}) - Nivel {pokemon_jugador.nivel}: {pokemon_jugador.salud} HP")
    salud_label_oponente.config(text=f"{pokemon_oponente.nombre} ({pokemon_oponente.tipo}) - Nivel {pokemon_oponente.nivel}: {pokemon_oponente.salud} HP")

def actualizar_estado_botones():
    atacar_boton.config(state=("disabled" if not pokemon_jugador.turno else "active"))
    ataque_especial_boton.config(state=("disabled" if not pokemon_jugador.turno else "active"))
    curarse_boton.config(state=("disabled" if not pokemon_jugador.turno else "active"))

def inhabilitar_botones():
    atacar_boton.config(state="disabled")
    ataque_especial_boton.config(state="disabled")
    curarse_boton.config(state="disabled")

# Crear una conexión a la base de datos SQLite
conn = sqlite3.connect("resultados_pokemon.db")
cursor = conn.cursor()

# Crear la tabla para almacenar resultados si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS resultados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jugador1 TEXT,
                    jugador2 TEXT,
                    resultado TEXT
                )''')

# Función para guardar resultados en la base de datos
def guardar_resultado(jugador1, jugador2, resultado):
    cursor.execute("INSERT INTO resultados (jugador1, jugador2, resultado) VALUES (?, ?, ?)", (jugador1, jugador2, resultado))
    conn.commit()

# Crear Pokémon para el jugador y el oponente
# Ejemplo de Pokémon disponibles (puedes agregar más):
pokemon_disponibles = [
    Pokemon("Charmander", "Fuego", 100, 20),
    Pokemon("Squirtle", "Agua", 100, 15),
    Pokemon("Bulbasaur", "Planta", 100, 18)
]

# Seleccionar aleatoriamente el Pokémon del oponente
pokemon_oponente = random.choice(pokemon_disponibles)

# Crear una ventana para el juego
ventana = tk.Tk()
ventana.title("Batalla Pokémon")

# Crear el marco principal
marco_principal = tk.Frame(ventana)
marco_principal.pack(padx=20, pady=20)

# Etiquetas de salud
salud_label_jugador = tk.Label(marco_principal, text="")
salud_label_oponente = tk.Label(marco_principal, text="")
salud_label_jugador.pack()
salud_label_oponente.pack()

# Botones de acciones
atacar_boton = tk.Button(marco_principal, text="Atacar", command=atacar)
ataque_especial_boton = tk.Button(marco_principal, text="Ataque Especial", command=ataque_especial)
curarse_boton = tk.Button(marco_principal, text="Curarse", command=curarse)
finalizar_turno_boton = tk.Button(marco_principal, text="Finalizar Turno", command=finalizar_turno)

atacar_boton.pack()
ataque_especial_boton.pack()
curarse_boton.pack()
finalizar_turno_boton.pack()

# Etiqueta de resultado
resultado_label = tk.Label(marco_principal, text="")
resultado_label.pack()

# Iniciar el juego con el turno del jugador
pokemon_jugador = random.choice(pokemon_disponibles)
salud_label_jugador.config(text=f"{pokemon_jugador.nombre} ({pokemon_jugador.tipo}) - Nivel {pokemon_jugador.nivel}: {pokemon_jugador.salud} HP")

# Actualizar el estado inicial de los botones
actualizar_estado_botones()

# Iniciar la interfaz gráfica
ventana.mainloop()

# Cerrar la conexión a la base de datos al finalizar el juego
conn.close()

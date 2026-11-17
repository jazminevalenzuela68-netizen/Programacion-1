"""Módulo de juego de Blackjack (Jugador vs Dealer).

Implementa la lógica y una interfaz gráfica mejorada (Tkinter con Canvas)
con fondo verde oscuro opaco, mensajes sin emojis y juego automático inicial.
"""

import random
import tkinter as tk

class JuegoBlackjack:
  """Clase principal para gestionar la interfaz gráfica visual y la lógica del Blackjack."""

  def __init__(self, root: tk.Tk) -> None:
    """Descripción breve: Inicializa la ventana principal de la aplicación y sus componentes gráficos.

    Descripción detallada: Configura los marcos, paneles de dibujo (Canvas) para las cartas,
    etiquetas de puntaje, botones de control y arranca la primera partida automáticamente.
    Parámetros: root (tk.Tk): Instancia de la ventana principal de Tkinter.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: app = JuegoBlackjack(tk.Tk())
    """
    self.root = root
    self.root.title("Blackjack - Jugador vs Banca")
    self.root.geometry("600x550")
    self.root.config(bg="#145a32")  

    self.baraja = []
    self.mano_jugador = []
    self.mano_dealer = []
    self.juego_activo = False

    # Título
    self.titulo_label = tk.Label(  root,  text="♠ BLACKJACK ♣",  font=("Arial", 18, "bold"),  bg="#145a32",  fg="white",)
    self.titulo_label.pack(pady=5)

    # --- ZONA DEL DEALER (BANCA) ---
    self.frame_dealer = tk.LabelFrame( root, text=" Dealer (Banca) ", font=("Arial", 11), bg="#145a32", fg="white"  )
    self.frame_dealer.pack(fill="x", padx=15, pady=5)
    self.canvas_dealer = tk.Canvas(
     self.frame_dealer, width=540, height=110, bg="#145a32", highlightthickness=0 )
    self.canvas_dealer.pack(padx=5, pady=5)
    self.label_dealer_puntos = tk.Label( self.frame_dealer, text="Puntos: ?", font=("Arial", 11, "bold"), bg="#145a32",  fg="white",)
    self.label_dealer_puntos.pack(anchor="w", padx=10, pady=2)

    # --- ZONA DEL JUGADOR ---
    self.frame_jugador = tk.LabelFrame( root, text=" Jugador ", font=("Arial", 11), bg="#145a32", fg="white"  )
    self.frame_jugador.pack(fill="x", padx=15, pady=5)
    self.canvas_jugador = tk.Canvas(
     self.frame_jugador, width=540, height=110, bg="#145a32", highlightthickness=0 )
    self.canvas_jugador.pack(padx=5, pady=5)
    self.label_jugador_puntos = tk.Label( self.frame_jugador, text="Puntos: 0",  font=("Arial", 11, "bold"),   bg="#145a32", fg="white",  )
    self.label_jugador_puntos.pack(anchor="w", padx=10, pady=2)

    # Mensajes de estado
    self.label_estado = tk.Label( root,  text="Partida iniciada. Tu turno...",   font=("Arial", 11, "italic"),   bg="#145a32", fg="#f1c40f",  )
    self.label_estado.pack(pady=5)

    # Panel de botones
    self.frame_botones = tk.Frame(root, bg="#145a32")
    self.frame_botones.pack(pady=5)
    self.btn_pedir = tk.Button( self.frame_botones, text="Pedir Carta", font=("Arial", 11), command=self.pedir_carta, width=12, )
    self.btn_pedir.grid(row=0, column=0, padx=5)
    self.btn_plantarse = tk.Button( self.frame_botones, text="Plantarse", font=("Arial", 11), command=self.plantarse, width=12,  )
    self.btn_plantarse.grid(row=0, column=1, padx=5)
    self.btn_nuevo = tk.Button(  self.frame_botones, text="Nuevo Juego",  font=("Arial", 11), command=self.iniciar_juego,  width=12,  bg="#d4ac0d",  fg="black",  )
    self.btn_nuevo.grid(row=0, column=2, padx=5)
    self.iniciar_juego()

  def crear_baraja(self) -> list:
    """Descripción breve: Crea y baraja un mazo estándar de 52 cartas con palos y valores.

    Descripción detallada: Genera combinaciones de denominaciones con sus
    respectivos palos (Corazones, Diamantes, Tréboles, Picas).
    Parámetros: Ninguno.
    Valor de retorno: list: Una lista de diccionarios con el 'nombre', 'palo' y
    'valor'.
    Excepciones: Ninguna.
        Caso correcto: baraja = juego.crear_baraja()
    """
    denominaciones = [
        ("2", 2),
        ("3", 3),
        ("4", 4),
        ("5", 5),
        ("6", 6),
        ("7", 7),
        ("8", 8),
        ("9", 9),
        ("10", 10),
        ("J", 10),
        ("Q", 10),
        ("K", 10),
        ("As", 11),
    ]
    palos = ["♥", "♦", "♣", "♠"]
    baraja = []

    for nombre, valor in denominaciones:
      for palo in palos:
        baraja.append({"nombre": nombre, "palo": palo, "valor": valor})
    random.shuffle(baraja)
    return baraja

  def calcular_puntos(self, mano: list) -> int:
    """Descripción breve: Calcula la puntuación total de una mano de cartas ajustando los Ases.

    Descripción detallada: Suma los valores y reduce el As de 11 a 1 si se excede
    de 21.
    Parámetros: mano (list): Lista de cartas en la mano.
    Valor de retorno: int: Puntuación total optimizada.
    Excepciones: Ninguna.
        Caso correcto: puntos = juego.calcular_puntos(mano_jugador)
    """
    puntos = 0
    ases = 0
    for carta in mano:
      puntos += carta["valor"]
      if carta["nombre"] == "As":
        ases += 1

    while puntos > 21 and ases > 0:
      puntos -= 10
      ases -= 1
    return puntos

  def es_blackjack_natural(self, mano: list) -> bool:
    """Descripción breve: Verifica si una mano corresponde a un Blackjack natural.

    Descripción detallada: Comprueba si la mano tiene 2 cartas y suma 21.
    Parámetros: mano (list): Lista de cartas a evaluar.
    Valor de retorno: bool: True si es Blackjack natural, False en caso
    contrario.
    Excepciones: Ninguna.
        Caso correcto: es_bj = juego.es_blackjack_natural(mano)
    """
    if len(mano) == 2 and self.calcular_puntos(mano) == 21:
      return True
    return False

  def iniciar_juego(self) -> None:
    """Descripción breve: Inicia una nueva ronda del juego de Blackjack.

    Descripción detallada: Restablece la baraja, reparte dos cartas iniciales,
    actualiza los dibujos de las cartas y evalúa Blackjacks naturales.
    Parámetros: Ninguno.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: juego.iniciar_juego()
    """
    self.baraja = self.crear_baraja()
    self.mano_jugador = []
    self.mano_dealer = []
    self.juego_activo = True

    self.mano_jugador.append(self.baraja.pop())
    self.mano_dealer.append(self.baraja.pop())
    self.mano_jugador.append(self.baraja.pop())
    self.mano_dealer.append(self.baraja.pop())

    self.actualizar_interfaz(mostrar_todo_dealer=False)

    self.btn_pedir.config(state="normal")
    self.btn_plantarse.config(state="normal")
    self.label_estado.config(text="Partida iniciada. ¿Pedir carta o plantarse?")

    jugador_bj = self.es_blackjack_natural(self.mano_jugador)
    dealer_bj = self.es_blackjack_natural(self.mano_dealer)

    if jugador_bj or dealer_bj:
      self.finalizar_por_blackjack_natural(jugador_bj, dealer_bj)

  def dibujar_cartas(self, canvas: tk.Canvas, mano: list, ocultar_primera: bool ) -> None:
    """Descripción breve: Dibuja de manera gráfica las cartas en un componente Canvas.
    Descripción detallada: Limpia el área de dibujo y genera rectángulos blancos
    simulando cartas con sus respectivos valores y colores.
    Parámetros:
        canvas (tk.Canvas): El lienzo donde se dibujarán las cartas.
        mano (list): Lista de diccionarios de las cartas a mostrar.
        ocultar_primera (bool): Si es True, dibuja la primera carta del dealer
        como reverso.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: juego.dibujar_cartas(self.canvas_jugador,
        self.mano_jugador, False)
    """
    canvas.delete("all")
    ancho_carta = 70
    alto_carta = 100
    espacio = 20
    inicio_x = 10
    inicio_y = 10

    for i, carta in enumerate(mano):
      x1 = inicio_x + i * (ancho_carta + espacio)
      y1 = inicio_y
      x2 = x1 + ancho_carta
      y2 = y1 + alto_carta

      if i == 0 and ocultar_primera:
        canvas.create_rectangle(  x1, y1, x2, y2, fill="#0e3a1f", outline="white", width=2)
        canvas.create_text( x1 + ancho_carta / 2,  y1 + alto_carta / 2, text="?", font=("Arial", 24, "bold"),  fill="white",  )
      else:
        canvas.create_rectangle( x1, y1, x2, y2, fill="white", outline="#bdc3c7", width=2)
        color = "red" if carta["palo"] in ["♥", "♦"] else "black"
        canvas.create_text(x1 + 12, y1 + 15,  text=carta["nombre"], font=("Arial", 11, "bold"), fill=color,)
        canvas.create_text(x1 + ancho_carta / 2,y1 + alto_carta / 2 + 5, text=carta["palo"],  font=("Arial", 22),fill=color,  )

  def actualizar_interfaz(self, mostrar_todo_dealer: bool) -> None:
    """Descripción breve: Actualiza los elementos visuales gráficos y de puntaje.

    Descripción detallada: Llama a la función de dibujo para las manos y
    actualiza los marcadores de puntos.
    Parámetros: mostrar_todo_dealer (bool): Define si se muestran todas las
    cartas de la banca.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: juego.actualizar_interfaz(False)
    """
    self.dibujar_cartas( self.canvas_jugador, self.mano_jugador, ocultar_primera=False )
    puntos_jugador = self.calcular_puntos(self.mano_jugador)
    self.label_jugador_puntos.config(text=f"Puntos: {puntos_jugador}")

    self.dibujar_cartas( self.canvas_dealer, self.mano_dealer,  ocultar_primera=not mostrar_todo_dealer, )
    if mostrar_todo_dealer:
      puntos_dealer = self.calcular_puntos(self.mano_dealer)
      self.label_dealer_puntos.config(text=f"Puntos: {puntos_dealer}")
    else:
      self.label_dealer_puntos.config(text="Puntos: ?")

  def pedir_carta(self) -> None:
    """Descripción breve: Permite al jugador solicitar una carta adicional a la baraja.

    Descripción detallada: Añade una carta a la mano del jugador, redibuja su
    interfaz gráfica y comprueba si excede 21 puntos.
    Parámetros: Ninguno.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: juego.pedir_carta()
    """
    if not self.juego_activo:
      return

    self.mano_jugador.append(self.baraja.pop())
    puntos_jugador = self.calcular_puntos(self.mano_jugador)
    self.actualizar_interfaz(mostrar_todo_dealer=False)

    if puntos_jugador > 21:
      self.juego_activo = False
      self.actualizar_interfaz(mostrar_todo_dealer=True)
      self.label_estado.config(text="Te pasaste de 21. Gana la banca.")
      self.desactivar_botones()
    elif puntos_jugador == 21:
      self.plantarse()

  def plantarse(self) -> None:
    """Descripción breve: Finaliza el turno del jugador y ejecuta el turno del dealer.

    Descripción detallada: El dealer pide cartas automáticamente si suma menos
    de 17 puntos y se determina el ganador.
    Parámetros: Ninguno.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: juego.plantarse()
    """
    if not self.juego_activo:
      return
    self.juego_activo = False
    self.desactivar_botones()

    while self.calcular_puntos(self.mano_dealer) < 17:
      self.mano_dealer.append(self.baraja.pop())

    self.actualizar_interfaz(mostrar_todo_dealer=True)

    puntos_jugador = self.calcular_puntos(self.mano_jugador)
    puntos_dealer = self.calcular_puntos(self.mano_dealer)

    if puntos_dealer > 21:
      self.label_estado.config( text="La banca se pasó de 21. ¡Has ganado la partida! :D")
    elif puntos_jugador > puntos_dealer:
      self.label_estado.config( text="¡Victoria! Tienes màs puntos que la banca.")
    elif puntos_jugador < puntos_dealer:
      self.label_estado.config( text="La banca tiene mejor puntuación. Gana la banca")
    else:
      self.label_estado.config(text="Empate.  Nadie gana la ronda ._. ")

  def finalizar_por_blackjack_natural( self, jugador_bj: bool, dealer_bj: bool ) -> None:
    """Descripción breve: Resuelve la partida inmediatamente por Blackjack natural.

    Descripción detallada: Revela todas las cartas gráficamente y muestra mensajes
    si se obtiene Blackjack natural.
    Parámetros:
        jugador_bj (bool): True si el jugador tiene Blackjack natural.
        dealer_bj (bool): True si el dealer tiene Blackjack natural.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: juego.finalizar_por_blackjack_natural(True, False)
    """
    self.juego_activo = False
    self.actualizar_interfaz(mostrar_todo_dealer=True)
    self.desactivar_botones()

    if jugador_bj and dealer_bj:
      self.label_estado.config( text="Empate. Ambos obtuvieron Blackjack :) .")
    elif dealer_bj:
      self.label_estado.config( text="El dealer consiguió Blackjack. Gano la banca." )
    elif jugador_bj:
      self.label_estado.config( text="¡Blackjack! Has ganado :D.")

  def desactivar_botones(self) -> None:
    """Descripción breve: Desactiva los botones de acción al concluir la partida.

    Descripción detallada: Cambia el estado de los botones a deshabilitados.
    Parámetros: Ninguno.
    Valor de retorno: None
    Excepciones: Ninguna.
        Caso correcto: juego.desactivar_botones()
    """
    self.btn_pedir.config(state="disabled")
    self.btn_plantarse.config(state="disabled")

if __name__ == "__main__":
  root = tk.Tk()
  app = JuegoBlackjack(root)
  root.mainloop()
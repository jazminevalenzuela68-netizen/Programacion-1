def InvertirCadena(cadena):
  """Función: invertir_cadena

  Descripción:
      Recibe una cadena de caracteres y construye una nueva cadena
      organizando los caracteres en orden inverso (de derecha a izquierda).

  Parámetros:
      cadena (str): Texto o cadena de caracteres original provista por el usuario.

  Retorno:
      str: La cadena de caracteres con los elementos invertidos.
  """
  CadenaInvertida = ""
#programa que recibe una cadena de caracteres y devuelve la cadena pero inversa
  # Recorremos la cadena original en sentido inverso:
  # - len(cadena) - 1: Posición del último carácter.
  # - -1: Límite del ciclo (se detiene antes de llegar a -1).
  # - -1: Paso decreciente (avanza hacia atrás).
  for i in range(len(cadena) - 1, -1, -1):
    # Concatenamos cada carácter correspondiente a la nueva cadena
    CadenaInvertida += cadena[i]

  return CadenaInvertida


print("\n--- INVERTIR CADENA ---")
texto_usuario = input("Ingresa una cadena de texto: ")

# Llamamos a la función documentada
texto_invertido = InvertirCadena(texto_usuario)
print(f"La cadena invertida es: '{texto_invertido}'")
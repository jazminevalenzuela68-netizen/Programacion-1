# Programa principal
if __name__ == "__main__":
  n = int(input("¿Cuántos números deseas capturar?: "))
  numeros = []

  # Captura de números
  for i in range(n):
    num = int(input(f"Ingresa el número {i + 1}: "))
    numeros.append(num)

  # Construcción de la lista sin repeticiones
  lista_unica = []
  for numero in numeros:
    if numero not in lista_unica:
      lista_unica.append(numero)

  # Resultados
  print("\nLista original:", numeros)
  print("Lista sin repeticiones:", lista_unica)
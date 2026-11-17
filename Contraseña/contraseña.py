def ContrasenaSegura(contrasena: str) -> bool:
    """Devuelve True si la contraseña cumple todos los criterios de seguridad."""
    if len(contrasena) < 5:
        return False
    tiene_mayuscula = False
    tiene_minuscula = False
    tiene_digito = False
    tiene_especial = False
    for caracter in contrasena:
        if caracter.isupper():
            tiene_mayuscula = True
        elif caracter.islower():
            tiene_minuscula = True
        elif caracter.isdigit():
            tiene_digito = True
        else:
            tiene_especial = True
    return (
        tiene_mayuscula
        and tiene_minuscula
        and tiene_digito
        and tiene_especial
    )
# Ejemplos de prueba
print(contrasenaSegura("Hola1!"))  # True
print(contrasenaSegura("hola1!"))  # False: no tiene mayúscula
print(contrasenaSegura("HOLA1!"))  # False: no tiene minúscula
print(contrasenaSegura("Hola!!"))  # False: no tiene dígito
print(contrasenaSegura("Ho1!"))    # False: tiene menos de 5 caracteres
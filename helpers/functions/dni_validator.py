import re

def validar_dni(dni):
    # Verificar que el dni consista únicamente de dígitos y que no exceda los 8 caracteres
    if re.match("^[0-9]{1,8}$", dni):
        return True
    else:
        return False
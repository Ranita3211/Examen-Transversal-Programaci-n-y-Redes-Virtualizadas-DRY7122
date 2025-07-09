try:
    vlan = int(input("Ingresa el número de VLAN: "))

    if 1 <= vlan <= 1005:
        print("Es una VLAN del rango normal (1-1005).")
    elif 1006 <= vlan <= 4094:
        print("Es una VLAN del rango extendido (1006-4094).")
    else:
        print("Número de VLAN inválido. Debe estar entre 1 y 4094.")
except ValueError:
    print("Entrada inválida. Debes ingresar un número entero.")

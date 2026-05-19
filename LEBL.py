from fileinput import close

from matplotlib import patches  # Para dibujar rectángulos en el gráfico


class Gate:
    def __init__(self, name, id, ocupado):
        self.name = name
        self.id = id
        self.ocupado = False


class BoardingArea:
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.gates = []


class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding = []
        self.airlines = []
        self.gates = []


class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


def SetGates(area, init_gate, end_gate, prefix):
    if init_gate > end_gate:
        print("Error")
        return -1

    current = init_gate

    area.gates = []

    while end_gate >= current:
        gate_name = prefix + str(current)
        gate = Gate(gate_name, current, False)
        area.gates.append(gate)
        current += 1
    return 0


def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"
    try:
        f = open(filename, "r")
    except FileNotFoundError:
        return -1
    terminal.airlines = []
    line = f.readline()
    while line != "":
        linestrip = line.strip()
        if linestrip != "":
            parts = linestrip.split("\t")
            if len(parts) >= 2:
                airline_name = parts[0]
                airline_code = parts[1]
                terminal.airlines.append((airline_name, airline_code))
            else:
                print(f"Line format: {line}")
        line = f.readline()
    f.close()
    return 0


def LoadAirportStructure(filename="Terminals.txt"):

    try:
        # Intenta abrir el archivo en modo lectura ("r")
        f = open(filename, "r")
    except FileNotFoundError:
        # Si el archivo no existe, responde al enunciado devolviendo un código de error (0)
        return 0

    # Crea el objeto base del aeropuerto de Barcelona (clase BarcelonaAP)
    bcn = BarcelonaAP("LEBL")

    # Lee y descarta la primera línea (habitualmente títulos o encabezados del archivo)
    f.readline()

    # Lee la primera línea de datos reales para iniciar el bucle
    line = f.readline()

    # El bucle se ejecutará línea por línea hasta que se llegue al final del archivo ("")
    while line != "":
        # Limpia los espacios en blanco y saltos de línea al inicio y final
        line_stripped = line.strip()

        # Si la línea no está vacía, procedemos a procesarla
        if line_stripped != "":
            # Divide la línea en una lista de palabras usando los espacios como separador
            parts = line_stripped.split()

            # Verifica que la línea tenga datos suficientes y que corresponda a una "Terminal"
            if len(parts) >= 3 and parts[0] == "Terminal":
                try:
                    # Extrae el nombre (ej. "T1") y la cantidad de zonas de embarque
                    terminal_name = parts[1]
                    num_areas = int(parts[2])

                    # Instancia el objeto de la clase Terminal con su respectivo nombre
                    terminal = Terminal(terminal_name)
                    j = 0
                    # Lee  tantas líneas como zonas de embarque indicó tener la terminal
                    while j < num_areas:
                        area_line = f.readline()

                        # Si el archivo se corta inesperadamente, detiene el bucle interno
                        if area_line == "":
                            j = num_areas
                        else:
                            area_stripped = area_line.strip()
                            if area_stripped != "":
                                area_parts = area_stripped.split()

                                # Valida que la línea contenga los datos mínimos de la zona
                                if len(area_parts) >= 7:

                                    area_name = area_parts[1]
                                    area_type = area_parts[2]

                                    try:
                                        # Extrae y convierte a entero los números de las puertas
                                        init_gate = int(area_parts[4])
                                        end_gate = int(area_parts[6])

                                        # Crea el objeto de la zona de embarque
                                        area = BoardingArea(area_name, area_type)


                                        SetGates(area, init_gate, end_gate, area_name)

                                        # Añade la zona de embarque estructurada a la terminal actual
                                        terminal.boarding.append(area)

                                    except ValueError:
                                        print(
                                            f"Error crítico: El número de áreas para la terminal no es un entero válido.")


                            # Avanza al siguiente índice de zona de embarque
                            j += 1

                    LoadAirlines(terminal, terminal_name)

                    # Añade la terminal completamente armada con sus zonas y aerolíneas al aeropuerto bcn
                    bcn.terminals.append(terminal)

                except ValueError:
                    print("errror")
                    # Si los datos numéricos de la terminal fallan, la ignora



        # Lee la siguiente línea para continuar el bucle principal
        line = f.readline()


    f.close()

    # Devuelve el objeto del aeropuerto totalmente construido (se asume de la última línea recortada)
    return bcn


def GateOccupancy(bcn):
    if not bcn or bcn == 0 or bcn == -1:
        print("Error")
        return []
    result = []
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]# recorremos las terminales
        j = 0
        while j < len(terminal.boarding):
            area = terminal.boarding[j]# recorremos la zona de embarque de cada terminal
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]# recorremos las gates de cada zona de embarque y vemos si estan ocupadas
                if gate.ocupado:
                    status = "Occupied"
                else:
                    status = "Free"
                result.append((gate.name, status, gate.id))# lo añadimos a la lista inicial
                k += 1
            j += 1
        i += 1
    return result# luego usaremos esta lista para crear el plot


def IsAirlineInTerminal(terminal, name):
    # 1. Validaciones iniciales de seguridad
    if name == "" or name == None:
        print("Error")
        return -1

    if not terminal.airlines:
        print("Error")
        return False

    # Pasamos la búsqueda a minúsculas para evitar problemas de "Avianca" vs "avianca"
    busqueda = name.lower().strip()

    # 2. Bucle de búsqueda flexible (Opción 2 sin comas)
    i = 0
    while i < len(terminal.airlines):
        aerolinea_actual = terminal.airlines[i]

        # Pasamos también los datos almacenados a minúsculas
        airline_name = str(aerolinea_actual[0]).lower().strip()
        airline_code = str(aerolinea_actual[1]).lower().strip()

        # COMPROBACIÓN INTELIGENTE usando 'in':
        # Verifica si el nombre guardado está dentro de la búsqueda, o al revés.
        if (airline_name in busqueda) or (airline_code in busqueda) or (busqueda in airline_name):
            return True  # ¡Coincidencia encontrada!

        i += 1

    return False


def SearchTerminal(bcn, name):
    # 1. Validación de seguridad por si el objeto del aeropuerto no es válido
    if not bcn or bcn == 0 or bcn == -1:
        print("Error")
        return 0

    i = 0
    # 2. Recorremos todas las terminales del aeropuerto
    while i < len(bcn.terminals):
        terminal_actual = bcn.terminals[i]

        # 3. Comprobamos si la aerolínea está en esta terminal.
        # .strip().lower() evita fallos si el usuario escribió espacios o minúsculas.
        if IsAirlineInTerminal(terminal_actual, name.strip()) == True:
            # Si la encuentra, devuelve inmediatamente el nombre de la terminal (ej: "T1")
            return terminal_actual.name

        i += 1

    # 4. Si recorrió todo el aeropuerto y NO la encontró en ninguna parte, devuelve 0
    return 0


def AssignGate(bcn, aircraft):
    # 1. Listas de códigos para identificar las zonas
    schengenArea = ["a", "b", "c", "m", "r", "s", "u"]
    # (Cualquier otra cosa como "d", "e", "w", "y" será No-Schengen)

    # 2. Primero buscamos el nombre del terminal de la aerolínea
    nombre_terminal = SearchTerminal(bcn, aircraft.airline)

    if nombre_terminal == "":
        print("Error: Aerolínea no encontrada")
        return -1

    # 3. Recorremos los terminales para encontrar el objeto terminal
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        if terminal.name == nombre_terminal:
            # 4. Recorremos las zonas de embarque
            j = 0
            while j < len(terminal.boarding):
                area = terminal.boarding[j]

                # Miramos si el nombre del área (ej: "a") está en la lista Schengen
                area_es_schengen = False
                n = 0
                while n < len(schengenArea):
                    if area.name == schengenArea[n]:
                        area_es_schengen = True
                    n += 1

                # Miramos si el destino del avión está en la lista Schengen
                avion_es_schengen = False
                m = 0
                while m < len(schengenArea):
                    if aircraft.origin == schengenArea[m]:
                        avion_es_schengen = True
                    m += 1

                # Si ambos son del mismo tipo (los dos True o los dos False)
                if area_es_schengen == avion_es_schengen:

                    # 5. Buscamos la primera puerta libre en esta área
                    k = 0
                    while k < len(area.gates):
                        puerta = area.gates[k]

                        if puerta.ocupado == False:
                            # Actualizamos la puerta según el enunciado
                            puerta.ocupado = True
                            puerta.aircraft = aircraft  # Guardamos el avión en la puerta
                            return 0  # Éxito

                        k += 1
                j += 1
        i += 1

    # Si termina todo y no encontró hueco
    print("Error: No hay puertas libres de ese tipo")
    return -1



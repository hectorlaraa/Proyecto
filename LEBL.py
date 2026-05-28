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


def PlotAirportSchematic(bcn, ax, terminal_filter=""):
    # Limpiamos el gráfico y ocultamos los ejes numéricos
    ax.clear()
    ax.axis('off')

    y_offset = 0  # Controla la altura a la que se dibuja cada terminal

    # Recorremos las terminales con un bucle while básico
    i = 0
    cantidad_terminales = len(bcn.terminals)

    while i < cantidad_terminales:
        terminal = bcn.terminals[i]

        # Cambiamos el NONE: Si el filtro es un texto vacío, o si el nombre coincide con el filtro...
        if terminal_filter == "" or terminal.name == terminal_filter:

            # 1. Dibujar la línea principal del Terminal (Tronco horizontal)
            ax.plot([0, max(len(terminal.boarding) * 2, 2)], [y_offset, y_offset], lw=6, color="#54217E")
            ax.text(-0.5, y_offset, terminal.name, fontsize=12, fontweight='bold', va='center')

            # Recorremos las áreas con un while básico
            a_idx = 0
            cantidad_areas = len(terminal.boarding)

            while a_idx < cantidad_areas:
                area = terminal.boarding[a_idx]

                x_area = a_idx * 2 + 1
                num_gates = len(area.gates)
                y_bottom = y_offset - (num_gates * 0.5) - 0.5

                # 2. Dibujar el pilar del Área de Embarque (Tronco vertical)
                ax.plot([x_area, x_area], [y_offset, y_bottom], lw=4, color="#54217E")
                ax.text(x_area, y_bottom - 0.5, area.name, fontsize=10, ha='center', fontweight='bold')

                # Recorremos las puertas con un while básico
                g_idx = 0
                cantidad_puertas = len(area.gates)

                while g_idx < cantidad_puertas:
                    gate = area.gates[g_idx]

                    y_gate = y_offset - (g_idx + 1) * 0.5

                    # 3. Dibujar la "rama" de la puerta
                    ax.plot([x_area, x_area + 0.5], [y_gate, y_gate], lw=2, color="#54217E")

                    # Etiqueta de la puerta
                    ax.text(x_area + 0.25, y_gate + 0.1, gate.name, fontsize=6, ha='center')

                    color = "#ff0000" if gate.ocupado else "#00ff00"
                    ax.plot([x_area + 0.55, x_area + 0.75], [y_gate, y_gate], lw=2, color=color)

                    if gate.ocupado and gate.aircraft != "":
                        ax.text(x_area - 0.2, y_gate, gate.aircraft.aircraft, fontsize=8, color='red', ha='right',
                                va='center')

                    # Avanzamos a la siguiente puerta
                    g_idx += 1

                # Avanzamos a la siguiente área
                a_idx += 1

            # Calculamos el espacio para la siguiente terminal de forma manual y simple
            if len(terminal.boarding) > 0:
                # Buscamos el máximo de puertas a mano para evitar funciones complejas
                max_gates = 0
                m = 0
                while m < len(terminal.boarding):
                    if len(terminal.boarding[m].gates) > max_gates:
                        max_gates = len(terminal.boarding[m].gates)
                    m += 1
                y_offset -= (max_gates * 0.5 + 3)
            else:
                y_offset -= 3

        # Avanzamos a la siguiente terminal
        i += 1

    ax.autoscale_view()


def AssignNightGates(bcn, aircrafts):
    '''Asigna puertas a los aviones nocturnos (solo tienen salida)'''
    # 1. Seguridad: comprobamos que las variables existan
    if not bcn or bcn == 0 or bcn == -1:
        print("Error: Aeropuerto no cargado.")
        return -1
    if not aircrafts:
        print("Error: Lista de vuelos vacía.")
        return -1

    i = 0
    asignados = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]

        # 2. Comprobamos si NO tiene llegada (es un avión nocturno)
        # Usamos getattr por seguridad extra por si el atributo no existiera
        if getattr(aircraft, 'arrival', None) is None or aircraft.arrival == "":

            # TRUCO: Como tu AssignGate busca el 'origin' para saber si es Schengen,
            # le copiamos temporalmente el 'destination' al 'origin' para que no falle.
            if getattr(aircraft, 'origin', None) is None:
                aircraft.origin = aircraft.destination

            # Llamamos a tu función de asignar
            AssignGate(bcn, aircraft)
            asignados += 1

        i += 1

    print(f"Se han asignado {asignados} aviones nocturnos con éxito.")
    return 0


def FreeGate(bcn, id_avion):
    '''Libera la puerta buscando el ID del avión'''
    if not bcn or bcn == 0 or bcn == -1:
        return -1

    # Pasamos a mayúsculas para evitar fallos tontos al escribir
    id_buscado = id_avion.strip().upper()

    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        j = 0
        while j < len(terminal.boarding):
            area = terminal.boarding[j]

            k = 0
            while k < len(area.gates):
                gate = area.gates[k]

                # Si está ocupado y tiene el avión guardado...
                if gate.ocupado == True and hasattr(gate, 'aircraft') and gate.aircraft is not None:

                    # Comparamos el ID del avión con el que buscamos
                    if gate.aircraft.aircraft.strip().upper() == id_buscado:
                        gate.ocupado = False
                        gate.aircraft = None
                        return 0  # ¡Encontrado y liberado!

                k += 1
            j += 1
        i += 1

    return -1  # Si termina los bucles y no lo encuentra
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


def SetGates(area, init_gate, end_gate,
             prefix):  # Definimos la función para asignar las puertas a cada zona de embarque, recibiendo el número inicial y final de las puertas y el prefijo de estas.
    if init_gate > end_gate:  # Si el numero incial de puertas es mayor que el final significa que el formato del archivo no es correcot
        print("Error")
        return -1

    current = init_gate

    area.gates = []

    while end_gate >= current:  # Mientras el número final de puertas sea mayor o igual que el número actual, vamos creando las puertas con su respectivo nombre (prefijo + número) y añadiéndolas a la zona de embarque. El número de puerta se va incrementando en cada iteración.
        gate_name = prefix + str(current)
        gate = Gate(gate_name, current, False)
        area.gates.append(gate)
        current += 1
    return 0


def LoadAirlines(terminal, t_name):  # Definimos la función para cargar las aerolíneas de cada terminal.
    filename = f"{t_name}_Airlines.txt"
    try:  # Intentamos abrir el archivos, pero en caso de no ser posible, el programa no avisará.
        f = open(filename, "r")
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return -1
    terminal.airlines = []  # Creamos una lista vacía para almacenar las aerolíneas de la terminal y luego vamos leyendo el archivo línea por línea, extrayendo el nombre y código de cada aerolínea y añadiéndolos a la lista de aerolíneas de la terminal.
    line = f.readline()  # Leemos la primera línea del archivo
    while line != "":  # Mientras la línea no esté vacía, el blucle se seguirá ejecutando.
        linestrip = line.strip()
        if linestrip != "":  # Separamos las líneas que no estén vacías y las asignamos a la terminal correspondiente. Si el formato de la línea no es correcto, se indicará por pantalla.
            parts = linestrip.split("\t")
            if len(parts) >= 2:
                airline_name = parts[0]
                airline_code = parts[1]
                terminal.airlines.append((airline_name,
                                          airline_code))  # Con append añadimos la aerolínea a la lista de aerolíneas de la terminal.
            else:
                print(f"Line format: {line}")
        line = f.readline()  # Para leer la línea siguiente y continuar el bucle.
    f.close()
    return 0


def LoadAirportStructure(
        filename="Terminals.txt"):  # Definimos la función para cargar la estructura del aeropuerto, recibiendo el nombre del archivo que contiene la información de las terminales y zonas de embarque.

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


def GateOccupancy(bcn):  # Definimos la fucnión para comprobar la ocupación de las gates del aeropuerto.
    if not bcn or bcn == 0 or bcn == -1:  # Si el objeto del aeropuerto no es válido, el programa lo indicará
        print("Error")
        return []
    result = []
    i = 0
    while i < len(
            bcn.terminals):  # Buicle para recorrer las terminales del aeropuerto, luego las zonas de embarque de cada terminal y finalmente las gates de cada zona de embarque, comprobando si están ocupadas o no y añadiendo esta información a una lista que se devolverá al final.
        terminal = bcn.terminals[i]  # recorremos las terminales
        j = 0
        while j < len(terminal.boarding):
            area = terminal.boarding[j]  # recorremos la zona de embarque de cada terminal
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]  # recorremos las gates de cada zona de embarque y vemos si estan ocupadas
                if gate.ocupado:
                    status = "Occupied"
                else:
                    status = "Free"
                result.append((gate.name, status, gate.id))  # lo añadimos a la lista inicial
                k += 1
            j += 1
        i += 1
    return result  # luego usaremos esta lista para crear el plot


def IsAirlineInTerminal(terminal, name):  # Función para determinar si la aerolínea se encuentra en la terminal.
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

        # Verifica si el nombre guardado está dentro de la búsqueda, o al revés.
        if (airline_name in busqueda) or (airline_code in busqueda) or (busqueda in airline_name):
            return True

        i += 1

    return False


def SearchTerminal(bcn,
                   name):  # Función para buscar el terminal de una aerolínea concreta, recibiendo el objeto del aeropuerto y el nombre de la aerolínea a buscar.
    # 1. Validación de seguridad por si el objeto del aeropuerto no es válido
    if not bcn or bcn == 0 or bcn == -1:
        print("Error")
        return 0

    i = 0
    # 2. Recorremos todas las terminales del aeropuerto
    while i < len(bcn.terminals):
        terminal_actual = bcn.terminals[i]

        # 3. Comprobamos si la aerolínea está en esta terminal.
        if IsAirlineInTerminal(terminal_actual, name.strip()) == True:
            # Si la encuentra, devuelve inmediatamente el nombre de la terminal (ej: "T1")
            return terminal_actual.name

        i += 1

    # 4. Si recorrió todo el aeropuerto y NO la encontró en ninguna parte, devuelve 0
    return 0


def AssignGate(bcn,
               aircraft):  # Función para asignar una puerta a un avión, recibiendo el objeto del aeropuerto y el objeto del avión a asignar.
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


def PlotAirportSchematic(bcn, ax,
                         terminal_filter=""):  # Función para dibujar un esquema del aeropuerto, recibiendo el objeto del aeropuerto, el objeto del gráfico (ax) y un filtro opcional para mostrar solo una terminal concreta.
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
            # La línea llega hasta la última área + el ancho de la rama de la puerta (0.75)
            x_end = (len(terminal.boarding) - 1) * 2 + 1 + 0.75 if terminal.boarding else 2
            ax.plot([0, x_end], [y_offset, y_offset], lw=6, color="#54217E")
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

                    if gate.ocupado and gate.aircraft is not None:
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

    ax.relim()


def AssignNightGates(bcn,
                     aircrafts):  # Función para asignar puertas a los aviones nocturnos, recibiendo el objeto del aeropuerto y la lista de vuelos.
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
            if getattr(aircraft, 'origin', None) is None:
                aircraft.origin = aircraft.destination

            # Llamamos a tu función de asignar
            AssignGate(bcn, aircraft)
            asignados += 1

        i += 1

    print(f"Se han asignado {asignados} aviones nocturnos con éxito.")
    return 0


def FreeGate(bcn, id_avion):  # Libera la gate ocupada por un avión concreto indicado por el ususario.
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


def AssignGatesAtTime(bcn, aircrafts,
                      time):  # Función para asignar las gates a los aviones que despegan a una hora concreta, recibiendo el objeto del aeropuerto, la lista de vuelos y la hora a comprobar.

    if not bcn or bcn == 0 or bcn == -1:  # Si el objeto del aeropuerto no es válido, el programa lo indicará
        print("Error: Aeropuerto no cargado.")
        return -1
    h = int(time.split(":")[
                0])  # Extraemos la hora de la cadena de texto (ej: "14:00" -> 14) para compararla con las horas de despegue y llegada de los aviones.
    notassigned = 0
    for aircraft in aircrafts:  # Primero liberamos las gates de los aviones que despegan a esa hora, para luego asignar las gates a los aviones que llegan a esa hora. De esta forma, si un avión llega a las 14:00 y otro despega a las 14:00, el avión que llega podrá ocupar la gate que deja libre el avión que despega.
        if aircraft.departure and int(aircraft.departure.split(":")[0]) == h:
            FreeGate(bcn, aircraft.aircraft)
    for aircraft in aircrafts:  # Luego asignamos las gates a los aviones que llegan a esa hora, y si no se les puede asignar una gate, aumentamos el contador de "notassigned" para saber cuántos aviones no han podido ser asignados a una gate a esa hora concreta.
        if aircraft.arrival and int(aircraft.arrival.split(":")[0]) == h:
            if AssignGate(bcn, aircraft):
                notassigned += 1
    return notassigned


def PlotDayOccupancy(bcn, aircrafts,
                     ax):  # Recibe el aeropuerto, la lista de vuelos y el objeto ax. El estado inicial de bcn corresponde al inicio del día (solo aviones nocturnos). Recorre las 24 horas llamando a AssignGatesAtTime y acumula las gates ocupadas por terminal y los vuelos no asignados cada hora.
    if not bcn or bcn == 0 or bcn == -1:
        print("Error: Aeropuerto no cargado.")
        return -1

    notassigned = []  # Lista para almacenar los vuelos no asignados en cada hora.
    occupancyT1 = []  # Lista para almacenar las gates ocupadas en T1 en cada hora.
    occupancyT2 = []  # Lista para almacenar las gates ocupadas en T2 en cada hora.

    for h in range(24):  # Recorremos las 24 horas del día.
        hour = str(h) + ":00"
        a = AssignGatesAtTime(bcn, aircrafts,
                              hour)  # Liberamos las gates de los aviones que despegan y asignamos las de los que llegan en esta hora.
        notassigned.append(max(a, 0))  # Si hay error (-1) lo tratamos como 0 para no distorsionar el gráfico.

        count1 = 0
        for area in bcn.terminals[0].boarding:  # Contamos gates ocupadas en T1 tras procesar la hora.
            for gate in area.gates:
                if gate.ocupado:
                    count1 += 1
        occupancyT1.append(count1)

        count2 = 0
        for area in bcn.terminals[1].boarding:  # Contamos gates ocupadas en T2 tras procesar la hora.
            for gate in area.gates:
                if gate.ocupado:
                    count2 += 1
        occupancyT2.append(count2)

    hours = list(range(24))
    ax.bar(hours, notassigned, color='#e57d90', alpha=0.6, label='Not assigned',
           zorder=2)  # Barras para los vuelos no asignados.
    ax.plot(hours, occupancyT1, color='#1e9faa', marker='o', linewidth=2, label='T1 gates occupied',
            zorder=3)  # Línea para T1.
    ax.plot(hours, occupancyT2, color='#32612d', marker='o', linewidth=2, label='T2 gates occupied',
            zorder=3)  # Línea para T2.
    ax.set_xlabel('Hour of the day')
    ax.set_ylabel('Gates occupied / Flights not assigned')
    ax.set_title('Gate occupancy throughout the day')
    ax.set_xticks(hours)
    ax.legend()
    return 0
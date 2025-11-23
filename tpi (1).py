import csv
import os


ARCHIVO_PAISES="paises_data.csv"

paises = []

# --- Funciones de Utilidad y Core ---


def cargar_datos_desde_archivo():
    global paises
    paises.clear()
    if not os.path.exists(ARCHIVO_PAISES):
        # Crear el archivo con cabecera si no existe
        with open(ARCHIVO_PAISES, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["nombre", "poblacion", "superficie en km2", "continente"])
        return
    
    with open(ARCHIVO_PAISES, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    for i in range(1, len(lineas)):
        linea = lineas[i].strip()
        if not linea:
            continue

        partes = linea.split(',')
        if len(partes) != 4:
            continue

        nombre = partes[0].strip()
        poblacion_str = partes[1].strip()
        superficie_str = partes[2].strip()
        continente = partes[3].strip()

        if poblacion_str.isdigit() and superficie_str.isdigit():
            paises.append({
                'nombre': nombre,
                'poblacion': int(poblacion_str),
                'superficie': int(superficie_str),
                'continente': continente
            })

def guardar_datos_en_archivo(): 
    global paises
    with open(ARCHIVO_PAISES, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["nombre", "poblacion", "superficie en km2", "continente"])
        for pais in paises:
            escritor.writerow([pais['nombre'], pais['poblacion'], pais['superficie'], pais['continente']])

def mostrar_pais(pais):#Muestro un pais ok
    
    print("-------------------------")
    print(f"  Nombre: {pais['nombre']}")
    print(f"  Población: {pais['poblacion']:}")
    print(f"  Superficie: {pais['superficie']:} km²")
    print(f"  Continente: {pais['continente']}")
    print("-------------------------")

def mostrar_lista_paises(lista_paises): #Muestro todos los paises ok
    
    if not lista_paises:
        print("\nℹERROR. No se encontraron países para mostrar.")#ERROR
        return
    
    print(f"\n--- Listado de {len(lista_paises)} Países ---")
    for pais in lista_paises:
        mostrar_pais(pais)
    print("------------------------------------------")

def solicitar_int(mensaje): #Manejo de error numerico ok
    
    while True:
        valor_str = input(mensaje)
        es_digito = False
        
        # Verificación básica si todos los caracteres son dígitos y no está vacío
        if valor_str and valor_str.isdigit():
            es_digito = True
        
        if es_digito:
            return int(valor_str)
        else:
            print("ERROR. Por favor, ingrese un número entero positivo.")

# --- Funcionalidades del Menú (Resto de funciones) ---

def menu_principal(): #Menu principal 
 
    print("\n" + "="*40)
    print("         Sistema de Gestión de Países")
    print("="*40)
    print("1. Cargar datos desde CSV")
    print("2. Agregar país")
    print("3. Actualizar Población/Superficie de País")
    print("4. Buscar país por nombre")
    print("5. Filtrar países")
    print("6. Ordenar países")
    print("7. Mostrar estadísticas")
    print("8. Mostrar todos los países")
    print("0. Salir")
    print("="*40)
    opcion = input("Ingrese su opción: ")
    return opcion

def agregar_pais(): #op2 Agregar pais ok archivo
    cargar_datos_desde_archivo()
 
    print("\n--- Agregar Nuevo País ---")
    
    nombre = input("Nombre del País (No vacío): ").strip()
    while not nombre:
        print("ERROR. El nombre del país no puede estar vacío.")
        nombre = input("Nombre del País (No vacío): ").strip()

    poblacion = solicitar_int("Población (entero positivo): ")

    superficie = solicitar_int("Superficie en km² (entero positivo): ")
    
    continente = input("Continente (No vacío): ").strip()
    while not continente:
        print("ERROR. El continente no puede estar vacío.")
        continente = input("Continente (No vacío): ").strip()

    nuevo_pais = {
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    }
    paises.append(nuevo_pais)
    guardar_datos_en_archivo()
    print(f"\n País '{nombre}' agregado exitosamente.")

def actualizar_pais():#op3 actualiza informacion ok archivo 
    cargar_datos_desde_archivo()
    if not paises:
        print("\nℹ ERROR. No hay datos cargados para actualizar.")
        return

    nombre_buscado = input("Ingrese el nombre exacto del país a actualizar: ").strip()
    
    pais_encontrado = None
    indice_encontrado = -1

    for i in range(len(paises)):
        if paises[i]['nombre'].lower() == nombre_buscado.lower():
            pais_encontrado = paises[i]
            indice_encontrado = i
            break
    
    if pais_encontrado:
        print(f"\nPaís encontrado: {pais_encontrado['nombre']}")
        mostrar_pais(pais_encontrado)

        print("--- Para actualizar Población, ingrese un número. Deje vacío para NO cambiar. ---")
        nueva_pob_str = solicitar_int("Nueva Población: ")

        if nueva_pob_str:
             paises[indice_encontrado]['poblacion'] = int(nueva_pob_str)
             print("Población actualizada.")
        else:
            print(f"\n Datos de {nombre_buscado} actualizados.")

        print("--- Para actualizar Superficie, ingrese un número. Deje vacío para NO cambiar. ---")
        nueva_sup = solicitar_int("Nueva Superficie: ")

        if nueva_sup:
             paises[indice_encontrado]['superficie'] = int(nueva_sup)
             print("Superficie actualizada.")
        else:
            print(f"\n Datos de {nombre_buscado} actualizados.")

    else:
        print(f"\n País '{nombre_buscado}' no encontrado.")
    guardar_datos_en_archivo()

def buscar_pais(): #op4 Buscar pais ok
    cargar_datos_desde_archivo()
    if not paises:
        print("\nℹ ERROR. No hay datos cargados para buscar.")
        return

    termino = input("Ingrese el nombre o parte del nombre del país a buscar: ").strip().lower()
    if not termino:
        print(" Debe ingresar un término de búsqueda.")
        return

    resultados = []
    for pais in paises:
        if termino in pais['nombre'].lower(): 
            resultados.append(pais)

    mostrar_lista_paises(resultados)

def filtrar_paises(): #op5 FIltrar ok
    cargar_datos_desde_archivo()
    
    if not paises:
        print("\nℹERROR. No hay datos cargados para filtrar.")
        return
    
    while True:
        print("\n--- Opciones de Filtrado ---")
        print("1. Filtrar por Continente")
        print("2. Filtrar por Rango de Población")
        print("3. Filtrar por Rango de Superficie")
        print("0. Volver al Menú Principal")
        
        opcion = input("Ingrese la opción de filtro: ")

        if opcion == '1':
            filtro_continente()
        elif opcion == '2':
            filtro_rango_poblacion()
        elif opcion == '3':
            filtro_rango_superficie()
        elif opcion == '0':
            break
        else:
            print("ERROR. Opción inválida.")

def filtro_continente(): #filtro por continente
    cargar_datos_desde_archivo()
    continente_buscado = input("Ingrese el nombre del Continente: ").strip().lower()
    
    resultados = []
    for pais in paises:
        if pais['continente'].lower() == continente_buscado:
            resultados.append(pais)
            
    print(f"\n--- Resultados del Filtro por Continente: {continente_buscado.upper()} ---")
    mostrar_lista_paises(resultados)

def filtro_rango_poblacion(): #Filtro por poblacion
    cargar_datos_desde_archivo()
    print("Filtro por Rango de Población")
    min_pob = solicitar_int("Población Mínima (entero): ")
    max_pob = solicitar_int("Población Máxima (entero): ")
    
    if min_pob > max_pob:
        min_pob, max_pob = max_pob, min_pob 
        
    resultados = []
    for pais in paises:
        if min_pob <= pais['poblacion'] <= max_pob:
            resultados.append(pais)
            
    print(f"\n--- Resultados del Filtro: Población entre {min_pob:,} y {max_pob:,} ---")
    mostrar_lista_paises(resultados)

def filtro_rango_superficie(): #filtro por superficie
    cargar_datos_desde_archivo()


    print("Filtro por Rango de Superficie")
    min_sup = solicitar_int("Superficie Mínima (entero): ")
    max_sup = solicitar_int("Superficie Máxima (entero): ")

    if min_sup > max_sup:
        min_sup, max_sup = max_sup, min_sup 

    resultados = []
    for pais in paises:
        if min_sup <= pais['superficie'] <= max_sup:
            resultados.append(pais)

    print(f"\n--- Resultados del Filtro: Superficie entre {min_sup:,} y {max_sup:,} km² ---")
    mostrar_lista_paises(resultados)

def ordenar_paises(): #op6 Ordenar paises
    cargar_datos_desde_archivo()

    if not paises:
        print("\nℹERROR. No hay datos cargados para ordenar.")
        return

    lista_a_ordenar = paises[:] 
    
    while True:
        print("\n--- Opciones de Ordenamiento ---")
        print("1. Por Nombre (A-Z)")
        print("2. Por Población (Ascendente o Descendente)")
        print("3. Por Superficie (Ascendente o Descendente)")
        print("0. Volver al Menú Principal")

        opcion = input("Ingrese la opción de ordenamiento: ")

        if opcion == '1':
            ordenar_por_nombre(lista_a_ordenar)
            mostrar_lista_paises(lista_a_ordenar)
        elif opcion == '2':
            ordenar_por_poblacion(lista_a_ordenar)
            mostrar_lista_paises(lista_a_ordenar)
        elif opcion == '3':
            ordenar_por_superficie(lista_a_ordenar)
            mostrar_lista_paises(lista_a_ordenar)
        elif opcion == '0':
            break
        else:
            print("ERROR. Opción inválida.")

def ordenar_por_nombre(lista):
    
    n = len(lista)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if lista[j]['nombre'].lower() > lista[j+1]['nombre'].lower():
                temp = lista[j]
                lista[j] = lista[j+1]
                lista[j+1] = temp
    print("\n Lista ordenada por Nombre (A-Z).")

def ordenar_por_poblacion(lista):
    while True:
        print("\nSeleccione el orden para Superficie:")
        print("1. Ascendente (Menor a Mayor)")
        print("2. Descendente (Mayor a Menor)")
        opcion = input("Opción: ")
        
        if opcion == '1' or opcion == '2':
            orden_ascendente = (opcion == '1')
            n = len(lista)
            for i in range(n - 1):
                for j in range(0, n - i - 1):
                    intercambiar = False
                    
                    if orden_ascendente:
                        if lista[j]['poblacion'] > lista[j+1]['poblacion']:
                            intercambiar = True
                    else: 
                        if lista[j]['poblacion'] < lista[j+1]['poblacion']:
                            intercambiar = True
                            
                    if intercambiar:
                        temp = lista[j]
                        lista[j] = lista[j+1]
                        lista[j+1] = temp
                        
            print(f"\n Lista ordenada por Poblacion ({'Ascendente' if orden_ascendente else 'Descendente'}).")
            break
        else:
            print("ERROR. Opción inválida.")

def ordenar_por_superficie(lista):
    
    
    while True:
        print("\nSeleccione el orden para Superficie:")
        print("1. Ascendente (Menor a Mayor)")
        print("2. Descendente (Mayor a Menor)")
        opcion = input("Opción: ")
        
        if opcion == '1' or opcion == '2':
            orden_ascendente = (opcion == '1')
            n = len(lista)
            for i in range(n - 1):
                for j in range(0, n - i - 1):
                    intercambiar = False
                    
                    if orden_ascendente:
                        if lista[j]['superficie'] > lista[j+1]['superficie']:
                            intercambiar = True
                    else: 
                        if lista[j]['superficie'] < lista[j+1]['superficie']:
                            intercambiar = True
                            
                    if intercambiar:
                        temp = lista[j]
                        lista[j] = lista[j+1]
                        lista[j+1] = temp
                        
            print(f"\n Lista ordenada por Superficie ({'Ascendente' if orden_ascendente else 'Descendente'}).")
            break
        else:
            print("ERROR. Opción inválida.")

def mostrar_estadisticas():
    cargar_datos_desde_archivo()
    
    if not paises:
        print("\nℹERROR. No hay datos cargados para calcular estadísticas.")
        return

    print("\n--- Estadísticas de Países ---")
    
    total_poblacion = 0
    total_superficie = 0
    conteo_continentes = {}

    mayor_pob = paises[0]
    menor_pob = paises[0]
    
    for pais in paises:
        total_poblacion += pais['poblacion']
        total_superficie += pais['superficie']
        
        if pais['poblacion'] > mayor_pob['poblacion']:
            mayor_pob = pais
        if pais['poblacion'] < menor_pob['poblacion']:
            menor_pob = pais
            
        continente = pais['continente']
        if continente in conteo_continentes:
            conteo_continentes[continente] += 1
        else:
            conteo_continentes[continente] = 1
    
    num_paises = len(paises)
    
    print(f" País con **Mayor Población**: {mayor_pob['nombre']} ({mayor_pob['poblacion']:,})")
    print(f" País con **Menor Población**: {menor_pob['nombre']} ({menor_pob['poblacion']:,})")

    promedio_poblacion = total_poblacion / num_paises
    print(f" **Promedio de Población**: {int(promedio_poblacion):,} habitantes.")

    promedio_superficie = total_superficie / num_paises
    print(f" **Promedio de Superficie**: {int(promedio_superficie):,} km².")

    print("\n **Cantidad de Países por Continente**:")
    for continente, cantidad in conteo_continentes.items():
        print(f"  - {continente}: {cantidad} países")
        
    print("------------------------------------------")

def main(): #MENU PRINCIPAL
   # cargar_datos_desde_archivo()

    # Si el archivo no existe, se crea con solo la cabecera.

    print(f"Sistema inicializado. Países cargados desde archivo: {len(paises)}")

    while True:
        opcion = menu_principal()
        
        if opcion == '1':
            # Vuelve a leer desde el CSV (por si fue modificado externamente)
            cargar_datos_desde_archivo()
        elif opcion == '2':
            agregar_pais()
        elif opcion == '3':
            actualizar_pais()
        elif opcion == '4':
            buscar_pais()
        elif opcion == '5':
            filtrar_paises()
        elif opcion == '6':
            ordenar_paises()
        elif opcion == '7':
            mostrar_estadisticas()
        elif opcion == '8':
            mostrar_lista_paises(paises)
        elif opcion == '0':
            print("\n ¡Gracias por usar el Sistema de Gestión de Países! Saliendo...")
            break
        else:
            print("\nERROR. Opción no válida. Por favor, seleccione una opción del menú.")


if __name__ == "__main__":
    main()
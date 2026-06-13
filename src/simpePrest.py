import os
import csv
from datetime import datetime, timedelta

# Nombres de los archivos planos para los datos
ARCHIVOS = {
    'usuarios': 'usuarios.txt',
    'inventario': 'inventario.txt',
    'prestamos': 'prestamos.txt',
    'ventas': 'ventas.txt'
}

# Inicializar archivos si no existen
for archivo in ARCHIVOS.values():
    if not os.path.exists(archivo):
        with open(archivo, 'w', encoding='utf-8') as f:
            pass


def leer_usuarios():
    usuarios = {}
    if not os.path.exists(ARCHIVOS['usuarios']): return usuarios
    with open(ARCHIVOS['usuarios'], 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                doc, nom, ape, correo, dias = linea.strip().split('|')
                usuarios[doc] = {
                    'nombre': nom, 'apellido': ape, 
                    'correo': correo, 'dias_permitidos': int(dias)
                }
    return usuarios

def guardar_usuario(doc, nom, ape, correo, dias):
    with open(ARCHIVOS['usuarios'], 'a', encoding='utf-8') as f:
        f.write(f"{doc}|{nom}|{ape}|{correo}|{dias}\n")

def leer_inventario():
    inventario = {}
    if not os.path.exists(ARCHIVOS['inventario']): return inventario
    with open(ARCHIVOS['inventario'], 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                id_item, nombre, categoria, precio, estado = linea.strip().split('|')
                inventario[id_item] = {
                    'nombre': nombre, 'categoria': categoria, 
                    'precio': float(precio), 'estado': estado
                }
    return inventario

def guardar_item(id_item, nombre, categoria, precio, estado):
    with open(ARCHIVOS['inventario'], 'a', encoding='utf-8') as f:
        f.write(f"{id_item}|{nombre}|{categoria}|{precio}|{estado}\n")

def leer_prestamos():
    prestamos = []
    if not os.path.exists(ARCHIVOS['prestamos']): return prestamos
    with open(ARCHIVOS['prestamos'], 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                id_item, documento, fecha_p, estado = linea.strip().split('|')
                prestamos.append({
                    'id_item': id_item, 'documento': documento,
                    'fecha_prestamo': datetime.strptime(fecha_p, "%Y-%m-%d"),
                    'estado': estado # 'Activo' o 'Devuelto' o 'Vendido'
                })
    return prestamos

def actualizar_prestamos_archivo(prestamos):
    with open(ARCHIVOS['prestamos'], 'w', encoding='utf-8') as f:
        for p in prestamos:
            f.write(f"{p['id_item']}|{p['documento']}|{p['fecha_prestamo'].strftime('%Y-%m-%d')}|{p['estado']}\n")

def guardar_venta(id_item, documento, subtotal, total):
    with open(ARCHIVOS['ventas'], 'a', encoding='utf-8') as f:
        f.write(f"{id_item}|{documento}|{subtotal}|{total}|{datetime.now().strftime('%Y-%m-%d')}\n")

def leer_ventas():
    ventas = []
    if not os.path.exists(ARCHIVOS['ventas']): return ventas
    with open(ARCHIVOS['ventas'], 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                id_item, doc, sub, tot, fecha = linea.strip().split('|')
                ventas.append({'id_item': id_item, 'documento': doc, 'subtotal': float(sub), 'total': float(tot), 'fecha': fecha})
    return ventas

# VALIDACIONES DE INFORMACIÓN


def validar_nombre_apellido(texto, tipo):
    if len(texto) < 3:
        print(f" Error: El {tipo} no puede tener menos de 3 letras.")
        return False
    if any(char.isdigit() for char in texto):
        print(f" Error: El {tipo} no puede contener números.")
        return False
    return True

def validar_documento(doc):
    if not doc.isdigit():
        print(" Error: El documento solo permite números.")
        return False
    if not (3 <= len(doc) <= 15):
        print(" Error: El documento debe tener entre 3 y 15 dígitos.")
        return False
    return True

def validar_correo(correo):
    if "@" in correo and correo.endswith(".com"):
        return True
    print(" Error: El correo debe incluir una '@' y terminar en '.com'.")
    return False


# LÓGICA CORE DEL NEGOCIO


def registrar_usuario():
    print("\n--- REGISTRAR NUEVO usuario ---")
    nombre = input("Nombre: ").strip()
    if not validar_nombre_apellido(nombre, "nombre"): return

    apellido = input("Apellido: ").strip()
    if not validar_nombre_apellido(apellido, "apellido"): return

    documento = input("Documento de identidad: ").strip()
    if not validar_documento(documento): return

    usuarios = leer_usuarios()
    if documento in usuarios:
        print(" Error: Este usuario ya se encuentra registrado.")
        return

    correo = input("Correo electrónico: ").strip()
    if not validar_correo(correo): return

    print("Opciones de tiempo de préstamo: 5, 10, 15 o 30 días.")
    try:
        dias = int(input("Seleccione los días permitidos: "))
        if dias not in [5, 10, 15, 30]:
            print(" Error: Valor de días no permitido.")
            return
    except ValueError:
        print(" Error: Debe ingresar un número entero.")
        return

    guardar_usuario(documento, nombre, apellido, correo, dias)
    print(f" ¡Usuario {nombre} {apellido} registrado exitosamente!")

def registrar_item():
    print("\n---  REGISTRAR ÍTEM EN INVENTARIO ---")
    nombre = input("Nombre del artículo: ").strip()
    if len(nombre) < 3:
        print(" Error: El nombre no puede tener menos de 3 letras.")
        return

    print("Categorías disponibles:")
    categorias = ["Videojuegos", "Libros", "Música y video", "Herramientas", "Dinero", "Misceláneo y varios"]
    for idx, cat in enumerate(categorias, 1):
        print(f"{idx}. {cat}")
    
    try:
        opc_cat = int(input("Seleccione la categoría (1-6): "))
        if not (1 <= opc_cat <= 6):
            print(" Categoría inválida.")
            return
        categoria_sel = categorias[opc_cat - 1]
    except ValueError:
        print(" Entrada inválida.")
        return

    try:
        precio = float(input("Precio de compra / adquisición: "))
        if precio <= 0:
            print(" El precio debe ser mayor a cero.")
            return
    except ValueError:
        print(" Entrada inválida para precio.")
        return

    # Lógica  para Calidad/Estado
    print("Estado del ítem (Evaluación Difusa):")
    print("1. Malo / Muy usado\n2. Regular\n3. Excelente / Como nuevo")
    estado_opc = input("Seleccione (1-3): ")
    estados_difusos = {"1": "Desgastado (Bajo)", "2": "Aceptable (Medio)", "3": "Óptimo (Alto)"}
    estado_sel = estados_difusos.get(estado_opc, "Aceptable (Medio)")

    # Creación del ID único 
    inv = leer_inventario()
    prefijo = categoria_sel[:3].upper()
    conteo = sum(1 for item in inv.values() if item['categoria'] == categoria_sel) + 1
    id_item = f"{prefijo}{conteo:03d}"

    guardar_item(id_item, nombre, categoria_sel, precio, estado_sel)
    print(f" Ítem guardado con éxito. ID Asignado: {id_item}")

def registrar_prestamo():
    print("\n--- REGISTRAR PRÉSTAMO ---")
    doc_cliente = input("Ingrese el documento del usuario: ").strip()
    usuarios = leer_usuarios()
    
    if doc_cliente not in usuarios:
        print("El préstamo no se puede realizar. MJ, debes registrar primero a este usuario.")
        return

    inventario = leer_inventario()
    prestamos = leer_prestamos()

    # Obtener cuáles ítems ya están ocupados en préstamos activos
    items_ocupados = {p['id_item'] for p in prestamos if p['estado'] == 'Activo'}

    print("\n--- Artículos en Inventario Disponibles ---")
    disponibles = False
    for id_i, data in inventario.items():
        if id_i not in items_ocupados:
            print(f"ID: {id_i} | Nombre: {data['nombre']} | Cat: {data['categoria']} | Estado: {data['estado']}")
            disponibles = True
    
    if not disponibles:
        print("No hay artículos disponibles en el inventario actual.")
        return

    id_a_prestar = input("\nIngrese el ID del ítem que desea llevar: ").strip().upper()
    if id_a_prestar not in inventario:
        print("El ID del ítem no existe.")
        return
    if id_a_prestar in items_ocupados:
        print("Este artículo ya se encuentra prestado actualmente.")
        return

    # Entrada de simulación de fecha para pruebas precisas, o fecha actual por defecto
    cambiar_fecha = input("¿Desea simular una fecha anterior para este préstamo? (s/n): ").strip().lower()
    fecha_prestamo = datetime.now()
    if cambiar_fecha == 's':
        f_str = input("Ingrese la fecha (AAAA-MM-DD): ").strip()
        try:
            fecha_prestamo = datetime.strptime(f_str, "%Y-%m-%d")
        except ValueError:
            print("Formato incorrecto. Se usará la fecha de hoy.")

    prestamos.append({
        'id_item': id_a_prestar,
        'documento': doc_cliente,
        'fecha_prestamo': fecha_prestamo,
        'estado': 'Activo'
    })
    actualizar_prestamos_archivo(prestamos)
    print(f"Préstamo registrado con éxito del ítem {id_a_prestar} a {usuarios[doc_cliente]['nombre']}.")

def registrar_devolucion():
    print("\n--- REGISTRAR Y CERTIFICAR DEVOLUCIÓN ---")
    doc_cliente = input("Ingrese el documento del usuario: ").strip()
    usuarios = leer_usuarios()
    
    if doc_cliente not in usuarios:
        print("Usuario no encontrado.")
        return

    prestamos = leer_prestamos()
    inventario = leer_inventario()
    
    prestamos_activos = [p for p in prestamos if p['documento'] == doc_cliente and p['estado'] == 'Activo']

    if not prestamos_activos:
        print("El usuario no tiene préstamos activos asignados en este momento.")
        return

    print("\nPréstamos activos del usuario:")
    for idx, p in enumerate(prestamos_activos):
        item_info = inventario.get(p['id_item'], {'nombre': 'Desconocido'})
        print(f"{idx + 1}. ID Ítem: {p['id_item']} - {item_info['nombre']} (Prestado el: {p['fecha_prestamo'].strftime('%Y-%m-%d')})")

    try:
        opc = int(input("Seleccione el ítem a devolver: "))
        if not (1 <= opc <= len(prestamos_activos)):
            print("Opción incorrecta.")
            return
        prestamo_sel = prestamos_activos[opc - 1]
    except ValueError:
        print("Entrada inválida.")
        return

    # Calcular cuántos días lleva el préstamo
    dias_transcurridos = (datetime.now() - prestamo_sel['fecha_prestamo']).days
    usuario_meta = usuarios[doc_cliente]

    # Regla: Si pasa de 30 días, se vende de forma obligatoria y genera factura en vez de devolución normal
    if dias_transcurridos > 30:
        print(f"\n ¡Alerta! El artículo ha estado prestado por {dias_transcurridos} días (Mayor a 30 días).")
        print("Por políticas del programa, debe procederse con la FACTURACIÓN DE VENTA OBLIGATORIA.")
        procesar_venta_forzada(prestamo_sel, usuario_meta, inventario.get(prestamo_sel['id_item']))
        return

    # Marcar como devuelto en la lista y actualizar archivo
    for p in prestamos:
        if p['id_item'] == prestamo_sel['id_item'] and p['estado'] == 'Activo':
            p['estado'] = 'Devuelto'
            break
    actualizar_prestamos_archivo(prestamos)

    # Generar Certificado de Devolución en TXT plano
    nombre_doc = f"{usuario_meta['nombre']}_{datetime.now().strftime('%Y%m%d')}_{prestamo_sel['id_item']}.txt"
    with open(nombre_doc, 'w', encoding='utf-8') as cert:
        cert.write("==================================================\n")
        cert.write("           CERTIFICADO DE DEVOLUCIÓN              \n")
        cert.write(f"           SOFTWARE: simplePrestamos              \n")
        cert.write("==================================================\n")
        cert.write(f"Prestador / Amigo: {usuario_meta['nombre']} {usuario_meta['apellido']}\n")
        cert.write(f"Documento: {doc_cliente}\n")
        cert.write(f"ID del Artículo: {prestamo_sel['id_item']}\n")
        cert.write(f"Fecha Inicial de Préstamo: {prestamo_sel['fecha_prestamo'].strftime('%Y-%m-%d')}\n")
        cert.write(f"Fecha Efectiva de Devolución: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        cert.write(f"Total Días en Posesión: {dias_transcurridos} días\n")
        cert.write("--------------------------------------------------\n")
        cert.write("Estado: Artículo retornado a MJ en condiciones óptimas.\n")
        cert.write("Gracias por ser un buen amigo.\n")
        cert.write("==================================================\n")

    print(f"Devolución procesada correctamente. Certificado generado con éxito: '{nombre_doc}'")

def procesar_venta_forzada(prestamo, usuario, item_data):
    if not item_data: return
    subtotal = item_data['precio']
    impuesto_conchudez = subtotal * 0.23 # Impuesto del 23%
    total = subtotal + impuesto_conchudez

    # Modificar estado del préstamo a 'Vendido'
    prestamos = leer_prestamos()
    for p in prestamos:
        if p['id_item'] == prestamo['id_item'] and p['estado'] == 'Activo':
            p['estado'] = 'Vendido'
            break
    actualizar_prestamos_archivo(prestamos)

    # Registrar en base de datos de ventas
    guardar_venta(prestamo['id_item'], prestamo['documento'], subtotal, total)

    # Generar Factura de Venta TXT
    nombre_factura = f"Factura_{usuario['nombre']}_{prestamo['id_item']}.txt"
    with open(nombre_factura, 'w', encoding='utf-8') as fact:
        fact.write("==================================================\n")
        fact.write("           FACTURA DE VENTA ADQUISICIÓN           \n")
        fact.write("==================================================\n")
        fact.write(f"Cliente: {usuario['nombre']} {usuario['apellido']}\n")
        fact.write(f"Documento: {prestamo['documento']}\n")
        fact.write(f"Artículo: {item_data['nombre']} (ID: {prestamo['id_item']})\n")
        fact.write(f"Fecha de Préstamo: {prestamo['fecha_prestamo'].strftime('%Y-%m-%d')}\n")
        fact.write(f"Fecha de Facturación: {datetime.now().strftime('%Y-%m-%d')}\n")
        fact.write("--------------------------------------------------\n")
        fact.write(f"Motivación: Superar el límite máximo de 30 días con el artículo.\n")
        fact.write("--------------------------------------------------\n")
        fact.write(f"Subtotal (Valor Compra): ${subtotal:,.2f}\n")
        fact.write(f"Impuesto por Conchudez (23%): ${impuesto_conchudez:,.2f}\n")
        fact.write(f"TOTAL A PAGAR: ${total:,.2f}\n")
        fact.write("==================================================\n")
    
    print(f"Factura emitida de forma digital bajo el nombre: '{nombre_factura}'")

def consultar_items_vencidos_30_dias():
    print("\n--- ARTÍCULOS CON MÁS DE 30 DÍAS DE PRÉSTAMO (POR VENDER / VENDIDOS) ---")
    prestamos = leer_prestamos()
    inventario = leer_inventario()
    usuarios = leer_usuarios()
    
    encontrados = False
    for p in prestamos:
        if p['estado'] == 'Activo':
            dias = (datetime.now() - p['fecha_prestamo']).days
            if dias > 30:
                user = usuarios.get(p['documento'], {'nombre': 'Desconocido'})
                item = inventario.get(p['id_item'], {'nombre': 'Desconocido'})
                print(f" ALERTA: Ítem ID: {p['id_item']} ('{item['nombre']}') prestado a {user['nombre']} por {dias} días.")
                encontrados = True

    if not encontrados:
        print("Ningún artículo activo supera los 30 días de retraso en este momento.")

def consultar_articulos_prestados():
    print("\n---CONSULTAR ESTADO GENERAL DE PRÉSTAMOS ---")
    prestamos = leer_prestamos()
    inventario = leer_inventario()
    usuarios = leer_usuarios()

    activos = [p for p in prestamos if p['estado'] == 'Activo']
    if not activos:
        print("No existen préstamos activos en el sistema actualmente.")
        return

    # Calcular días vigentes y ordenar descendientemente (de mayor cantidad de días a menor)
    lista_ordenada = []
    for p in activos:
        dias = (datetime.now() - p['fecha_prestamo']).days
        lista_ordenada.append((dias, p))

    lista_ordenada.sort(key=lambda x: x[0], reverse=True)

    print(f"{'Días':<6} | {'ID Item':<8} | {'Artículo':<20} | {'Prestado a':<20} | {'Estado Alertas'}")
    print("-" * 75)
    
    datos_csv = []
    for dias, p in lista_ordenada:
        item = inventario.get(p['id_item'], {'nombre': 'Desconocido'})
        user = usuarios.get(p['documento'], {'nombre': 'Desconocido'})
        
        # Generar Alertas según los requerimientos solicitados
        alerta = "Dentro del tiempo"
        if dias >= 30:
            alerta = "Requiere Venta Obligatoria (>30 días)"
        elif dias >= 20:
            alerta = "Notificación de recuperación enviada (>=20 días)"

        print(f"{dias:<6} | {p['id_item']:<8} | {item['nombre'][:20]:<20} | {user['nombre'][:20]:<20} | {alerta}")
        datos_csv.append([dias, p['id_item'], item['nombre'], user['nombre'], alerta])

    # Exportación automática del estado actual a formato CSV 
    with open('reporte_prestamos.csv', 'w', newline='', encoding='utf-8') as f_csv:
        escritor = csv.writer(f_csv)
        escritor.writerow(['Dias_Transcurridos', 'ID_Item', 'Nombre_Item', 'Nombre_usuario', 'Estado_Alertas'])
        escritor.writerows(datos_csv)
    print("\n Los datos estadísticos anteriores se han exportado con éxito al archivo 'reporte_prestamos.csv'.")

# MÓDULO ADMINISTRADOR


def modulo_administrador():
    print("\n--- ACCESO DE ADMINISTRACIÓN ---")
    
    ADMIN_USER = "aleja"
    ADMIN_PASS = "1234"

    user = input("Usuario Administrador: ")
    contra = input("Contraseña: ")

    if user != ADMIN_USER or contra != ADMIN_PASS:
        print(" Credenciales inválidas. Acceso restringido.")
        return

    while True:
        print("\n--- SUBMENÚ DE ADMINISTRACIÓN ---")
        print("1. Total de préstamos registrados")
        print("2. Total de ítems devueltos")
        print("3. Total de ventas realizadas e ingresos acumulados")
        print("4. Listado completo de usuarios registrados")
        print("5. Reporte de comportamiento (Mayor/Menor cantidad de préstamos)")
        print("6. Volver al menú principal")
        
        opc = input("Seleccione un reporte (1-6): ").strip()
        prestamos = leer_prestamos()
        usuarios = leer_usuarios()
        ventas = leer_ventas()

        if opc == "1":
            print(f"\n Total de préstamos registrados históricamente: {len(prestamos)}")
        elif opc == "2":
            devueltos = sum(1 for p in prestamos if p['estado'] == 'Devuelto')
            print(f"\n Total de ítems devueltos satisfactoriamente: {devueltos}")
        elif opc == "3":
            total_dinero = sum(v['total'] for v in ventas)
            print(f"\n Total de ventas realizadas: {len(ventas)}")
            print(f" Total pago neto recaudado (Con impuesto del 23%): ${total_dinero:,.2f}")
        elif opc == "4":
            print("\n LISTADO COMPLETO DE USUARIOS:")
            for doc, d in usuarios.items():
                print(f"- Doc: {doc} | {d['nombre']} {d['apellido']} | Correo: {d['correo']} | Plazo Máx: {d['dias_permitidos']} días")
        elif opc == "5":
            if not usuarios:
                print("No hay usuarios en la plataforma.")
                continue
            conteos = {doc: 0 for doc in usuarios}
            for p in prestamos:
                if p['documento'] in conteos:
                    conteos[p['documento']] += 1
            
            max_doc = max(conteos, key=conteos.get)
            min_doc = min(conteos, key=conteos.get)
            
            print(f"\n usuario con mayor flujo de préstamos: {usuarios[max_doc]['nombre']} ({conteos[max_doc]} préstamos)")
            print(f" usuario con menor flujo de préstamos: {usuarios[min_doc]['nombre']} ({conteos[min_doc]} préstamos)")
        elif opc == "6":
            break
        else:
            print("Opción no encontrada.")

# MENÚ PRINCIPAL DEL SISTEMA

def menu_principal():
    while True:
        print("\n" + "="*40)
        print("       BIENVENIDO A simplePrestamos      ")
        print("="*40)
        print("1. Registrar Usuario")
        print("2. Registrar Nuevo Ítem al Inventario")
        print("3. Registrar Préstamo")
        print("4. Registrar Devolución de Artículo")
        print("5. Consultar ítems con más de 30 días")
        print("6. Consultar Estado General de Préstamos")
        print("7. Módulo Administrador")
        print("8. Salir del Sistema")
        print("="*40)
        
        opcion = input("Seleccione una opción (1-8): ").strip()
        
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            registrar_item()
        elif opcion == "3":
            registrar_prestamo()
        elif opcion == "4":
            registrar_devolucion()
        elif opcion == "5":
            consultar_items_vencidos_30_dias()
        elif opcion == "6":
            consultar_articulos_prestados()
        elif opcion == "7":
            modulo_administrador()
        elif opcion == "8":
            print("\n ¡Gracias por usar simplePrestamos! Cerrando sistema de forma segura.")
            break
        else:
            print("Opción inválida. Intente de nuevo por favor.")

if __name__ == "__main__":
    menu_principal()
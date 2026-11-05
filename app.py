from datetime import datetime
import os
import flet as ft
from supabase import create_client, Client

# ---------------------------------------------------------
# CONFIGURACIÓN DE SUPABASE
# ---------------------------------------------------------
SUPABASE_URL = "https://rnjatfnurjyyoisgypas.supabase.co"
SUPABASE_KEY = "sb_publishable_HDPN1VhDwAagVadTwevJuw_2egFZMx4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Archivo local para recordar la sesión
SESSION_FILE = "session.txt"

def main(page: ft.Page):
    page.title = "Control de Quesería - Acceso Socios"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "grey_50"
    
    usuario_actual = {"nombre": None}
    pedazo_en_curso_id = {"id": 0}
    
    body_container = ft.Container(expand=True, padding=15)
    page.add(body_container)

    def mostrar_snack(mensaje, color):
        page.snack_bar = ft.SnackBar(ft.Text(mensaje, color="white"), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # ---------------------------------------------------------
    # FUNCIONES DE SESIÓN LOCAL (ARCHIVO)
    # ---------------------------------------------------------
    def guardar_sesion_local(username):
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                f.write(username)
        except Exception as ex:
            print(f"Error guardando sesión: {ex}")

    def leer_sesion_local():
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception:
                return None
        return None

    def borrar_sesion_local():
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except Exception as ex:
                print(f"Error borrando sesión: {ex}")

    # ---------------------------------------------------------
    # 1. PANTALLA DE LOGIN
    # ---------------------------------------------------------
    def cargar_pantalla_login():
        page.appbar = ft.AppBar(
            title=ft.Text("Control de Ventas", color="white", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor="amber",
        )
        page.navigation_bar = None
        
        txt_user = ft.TextField(label="Usuario", prefix_icon=ft.Icons.PERSON_OUTLINE, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        
        def iniciar_sesion(e):
            user = txt_user.value.strip().lower() if txt_user.value else ""
            pwd = txt_pass.value.strip() if txt_pass.value else ""
            if not user or not pwd:
                mostrar_snack("Completa usuario y contraseña", "red")
                return
            try:
                response = supabase.table("usuarios").select("*").eq("username", user).eq("password", pwd).execute()
                if response.data and len(response.data) > 0:
                    usuario_actual["nombre"] = user
                    guardar_sesion_local(user)
                    cargar_pantalla_principal()
                else:
                    mostrar_snack("Usuario o contraseña incorrectos", "red")
            except Exception as ex:
                mostrar_snack(f"Error: {ex}", "red")

        body_container.content = ft.Column(
            [
                ft.Container(height=30),
                ft.Row([ft.Icon(ft.Icons.STORE, size=50, color="amber")], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Bienvenido", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("Inicia sesión en tu cuenta de socio", size=14, color="grey", text_align=ft.TextAlign.CENTER),
                ft.Container(height=20),
                txt_user,
                txt_pass,
                ft.Container(height=10),
                ft.Button("Iniciar Sesión", icon=ft.Icons.LOGIN, on_click=iniciar_sesion, bgcolor="amber", color="white"),
                ft.OutlinedButton("Registrarse", icon=ft.Icons.PERSON_ADD, on_click=lambda e: cargar_pantalla_registro()),
                ft.TextButton("¿Olvidaste tu contraseña?", on_click=lambda e: cargar_pantalla_recuperar()),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        page.update()

    # ---------------------------------------------------------
    # 2. PANTALLA DE REGISTRO
    # ---------------------------------------------------------
    def cargar_pantalla_registro():
        page.appbar = ft.AppBar(
            title=ft.Text("Control de Ventas", color="white", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor="amber",
            leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: cargar_pantalla_login()),
        )
        txt_nuevo_user = ft.TextField(label="Nuevo Usuario", prefix_icon=ft.Icons.PERSON_ADD_OUTLINED, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_pregunta_personalizada = ft.TextField(label="Pregunta Secreta", prefix_icon=ft.Icons.HELP_OUTLINE, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_respuesta = ft.TextField(label="Respuesta Secreta", prefix_icon=ft.Icons.SECURITY, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_nuevo_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        
        def ejecutar_registro(e):
            user = txt_nuevo_user.value.strip().lower() if txt_nuevo_user.value else ""
            pregunta = txt_pregunta_personalizada.value.strip() if txt_pregunta_personalizada.value else ""
            respuesta = txt_respuesta.value.strip().lower() if txt_respuesta.value else ""
            pwd = txt_nuevo_pass.value.strip() if txt_nuevo_pass.value else ""
            
            if not user or not pregunta or not respuesta or not pwd:
                mostrar_snack("Completa todos los campos", "red")
                return
            try:
                supabase.table("usuarios").insert({
                    "username": user,
                    "pregunta": pregunta,
                    "respuesta": respuesta,
                    "password": pwd
                }).execute()
                mostrar_snack("¡Registrado con éxito!", "green")
                cargar_pantalla_login()
            except Exception as ex:
                mostrar_snack(f"Error: {ex}", "red")

        body_container.content = ft.Column(
            [
                ft.Container(height=10),
                ft.Text("Crear Cuenta", size=22, weight=ft.FontWeight.BOLD),
                txt_nuevo_user,
                txt_pregunta_personalizada,
                txt_respuesta,
                txt_nuevo_pass,
                ft.Container(height=10),
                ft.Button("Registrarse", icon=ft.Icons.CHECK, on_click=ejecutar_registro, bgcolor="amber", color="white"),
                ft.OutlinedButton("Volver al Login", icon=ft.Icons.ARROW_BACK, on_click=lambda e: cargar_pantalla_login()),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
        page.update()

    # ---------------------------------------------------------
    # 2.B RECUPERACIÓN DE CONTRASEÑA
    # ---------------------------------------------------------
    def cargar_pantalla_recuperar():
        page.appbar = ft.AppBar(
            title=ft.Text("Control de Ventas", color="white", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor="amber",
            leading=ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda e: cargar_pantalla_login()),
        )
        txt_user_rec = ft.TextField(label="Usuario", prefix_icon=ft.Icons.PERSON_OUTLINE, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_lbl_pregunta = ft.Text("Ingresa tu usuario para ver tu pregunta", size=14, color="grey", weight=ft.FontWeight.BOLD)
        txt_respuesta_rec = ft.TextField(label="Tu Respuesta Secreta", prefix_icon=ft.Icons.SECURITY, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white", visible=False)
        txt_nueva_pass = ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_RESET, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white", visible=False)
        btn_verificar_user = ft.Button("Buscar Usuario", icon=ft.Icons.SEARCH, bgcolor="amber", color="white")
        btn_cambiar_pass = ft.Button("Cambiar Contraseña", icon=ft.Icons.CHECK, bgcolor="green", color="white", visible=False)
        
        datos_rec = {"respuesta_correcta": None}
        
        def buscar_usuario(e):
            user = txt_user_rec.value.strip().lower() if txt_user_rec.value else ""
            if not user:
                mostrar_snack("Introduce tu usuario", "red")
                return
            try:
                res = supabase.table("usuarios").select("pregunta, respuesta").eq("username", user).execute()
                if res.data and len(res.data) > 0:
                    datos_rec["respuesta_correcta"] = res.data[0]["respuesta"]
                    txt_lbl_pregunta.value = f"Pregunta: {res.data[0]['pregunta']}"
                    txt_respuesta_rec.visible = True
                    txt_nueva_pass.visible = True
                    btn_cambiar_pass.visible = True
                    btn_verificar_user.visible = False
                    txt_user_rec.read_only = True
                    page.update()
                else:
                    mostrar_snack("El usuario no existe", "red")
            except Exception as ex:
                mostrar_snack(f"Error: {ex}", "red")

        def confirmar_cambio(e):
            user = txt_user_rec.value.strip().lower() if txt_user_rec.value else ""
            resp_ingresada = txt_respuesta_rec.value.strip().lower() if txt_respuesta_rec.value else ""
            nueva_pwd = txt_nueva_pass.value.strip() if txt_nueva_pass.value else ""
            if not resp_ingresada or not nueva_pwd:
                mostrar_snack("Completa los campos", "red")
                return
            if resp_ingresada == datos_rec["respuesta_correcta"]:
                try:
                    supabase.table("usuarios").update({"password": nueva_pwd}).eq("username", user).execute()
                    mostrar_snack("¡Contraseña actualizada!", "green")
                    cargar_pantalla_login()
                except Exception as ex:
                    mostrar_snack(f"Error: {ex}", "red")
            else:
                mostrar_snack("Respuesta incorrecta", "red")

        btn_verificar_user.on_click = buscar_usuario
        btn_cambiar_pass.on_click = confirmar_cambio

        body_container.content = ft.Column(
            [
                ft.Container(height=10),
                txt_user_rec,
                txt_lbl_pregunta,
                txt_respuesta_rec,
                txt_nueva_pass,
                ft.Container(height=10),
                btn_verificar_user,
                btn_cambiar_pass,
                ft.OutlinedButton("Cancelar", icon=ft.Icons.CANCEL, on_click=lambda e: cargar_pantalla_login()),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        )
        page.update()

    # ---------------------------------------------------------
    # 3. PANTALLA PRINCIPAL
    # ---------------------------------------------------------
    def cargar_pantalla_principal():
        def cerrar_sesion(e):
            borrar_sesion_local()
            usuario_actual["nombre"] = None
            cargar_pantalla_login()

        page.appbar = ft.AppBar(
            title=ft.Text("Acceso de Socios", color="white", weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor="amber",
            actions=[ft.IconButton(ft.Icons.LOGOUT, icon_color="white", on_click=cerrar_sesion, tooltip="Cerrar Sesión")],
        )
        
        vista_principal = ft.Container(expand=True)
        
        txt_fecha = ft.TextField(
            label="Fecha de la Venta",
            value=datetime.now().strftime("%Y-%m-%d"),
            read_only=True,
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            border=ft.OutlineInputBorder(border_radius=12),
            filled=True,
            bgcolor="white",
            expand=True,
        )
        
        date_picker = ft.DatePicker(
            on_change=lambda e: setattr(txt_fecha, "value", date_picker.value.strftime("%Y-%m-%d")) or page.update() if date_picker.value else None,
            first_date=datetime(2025, 1, 1),
            last_date=datetime(2030, 12, 31)
        )
        if date_picker not in page.overlay:
            page.overlay.append(date_picker)
            
        btn_calendario = ft.IconButton(icon=ft.Icons.DATE_RANGE, icon_color="amber", on_click=lambda e: setattr(date_picker, "open", True) or page.update())
        
        txt_cliente = ft.TextField(label="Nombre del Cliente", prefix_icon=ft.Icons.PERSON, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_producto = ft.TextField(label="Tipo de Queso / Producto", prefix_icon=ft.Icons.SHOPPING_BAG, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_peso = ft.TextField(label="Peso (Ej: 1.5kg o 700g)", prefix_icon=ft.Icons.SCALE, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_precio_total = ft.TextField(label="Precio Total a Cobrar ($)", keyboard_type=ft.KeyboardType.NUMBER, prefix_icon=ft.Icons.ATTACH_MONEY, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        
        dd_metodo_pago = ft.Dropdown(
            label="Método de Pago",
            options=[ft.dropdown.Option("Efectivo"), ft.dropdown.Option("Transferencia"), ft.dropdown.Option("Tarjeta (POS)")],
            value="Efectivo", border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white"
        )
        dd_estado = ft.Dropdown(
            label="Estado (Pago / Deuda)",
            options=[ft.dropdown.Option("Pagado"), ft.dropdown.Option("Fiado / Deuda")],
            value="Pagado", border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white"
        )
        
        txt_buscar = ft.TextField(label="Buscar por nombre de cliente...", prefix_icon=ft.Icons.SEARCH, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_total_fiado = ft.Text("Total en deudas pendientes: $ 0", size=15, weight=ft.FontWeight.BOLD, color="red")
        
        txt_id_pagar = ft.TextField(label="Nº de Registro a Pagar", border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white", keyboard_type=ft.KeyboardType.NUMBER)
        txt_id_borrar_venta = ft.TextField(label="Nº a Borrar", border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white", keyboard_type=ft.KeyboardType.NUMBER)
        
        mapa_ventas_ids = {}
        tabla_historial = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nº")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Peso")),
                ft.DataColumn(ft.Text("Total ($)")),
                ft.DataColumn(ft.Text("Pago")),
                ft.DataColumn(ft.Text("Estado")),
            ],
            rows=[]
        )

        def mostrar_vista_cuaderno(e=None):
            nonlocal mapa_ventas_ids
            mapa_ventas_ids = {}
            filtro = txt_buscar.value.strip().lower() if txt_buscar and txt_buscar.value else ""
            
            filas_tabla = []
            suma_fiados = 0
            
            try:
                res = supabase.table("ventas").select("*").eq("usuario", usuario_actual["nombre"]).order("id", desc=False).execute()
                registros = res.data or []
                suma_fiados = sum(int(reg["total"]) for reg in registros if reg["estado"] == "Fiado / Deuda")
                txt_total_fiado.value = f"Total en deudas pendientes: $ {suma_fiados:,}".replace(",", ".")
                
                contador = 1
                for reg in registros:
                    db_id = reg["id"]
                    cliente = reg["nombre_cliente"]
                    if filtro and filtro not in cliente.lower():
                        contador += 1
                        continue
                    mapa_ventas_ids[contador] = db_id
                    color_estado = "green" if reg["estado"] == "Pagado" else "red"
                    
                    fila = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(contador))),
                            ft.DataCell(ft.Text(reg["fecha"])),
                            ft.DataCell(ft.Text(cliente)),
                            ft.DataCell(ft.Text(reg["producto"])),
                            ft.DataCell(ft.Text(reg["peso_txt"])),
                            ft.DataCell(ft.Text(f"$ {int(reg['total']):,}".replace(",", "."))),
                            ft.DataCell(ft.Text(reg["metodo_pago"])),
                            ft.DataCell(ft.Container(content=ft.Text(reg["estado"], color="white", size=11, weight=ft.FontWeight.BOLD), bgcolor=color_estado, padding=5, border_radius=6)),
                        ]
                    )
                    filas_tabla.append(fila)
                    contador += 1
                
                tabla_historial.rows = filas_tabla
                if tabla_historial.page:
                    tabla_historial.update()
            except Exception as ex:
                print(f"Error cargando tabla de ventas: {ex}")

            def guardar_venta(ev):
                try:
                    c_val = txt_cliente.value.strip() if txt_cliente.value else ""
                    p_val = txt_producto.value.strip() if txt_producto.value else ""
                    pes_val = txt_peso.value.strip() if txt_peso.value else ""
                    pre_val = txt_precio_total.value.strip() if txt_precio_total.value else ""
                    if not c_val or not p_val or not pes_val or not pre_val:
                        mostrar_snack("Completa todos los campos de la venta", "red")
                        return
                    total = int(pre_val)
                    estado_v = dd_estado.value
                    metodo_f = "Pendiente (-)" if estado_v == "Fiado / Deuda" else dd_metodo_pago.value
                    
                    supabase.table("ventas").insert({
                        "usuario": usuario_actual["nombre"],
                        "fecha": txt_fecha.value,
                        "nombre_cliente": c_val,
                        "producto": p_val,
                        "peso_txt": pes_val,
                        "total": total,
                        "metodo_pago": metodo_f,
                        "estado": estado_v,
                        "inventario_id": pedazo_en_curso_id["id"]
                    }).execute()
                    
                    pedazo_en_curso_id["id"] = 0
                    txt_cliente.value = ""
                    txt_producto.value = ""
                    txt_peso.value = ""
                    txt_precio_total.value = ""
                    
                    mostrar_snack("¡Venta registrada con éxito!", "green")
                    mostrar_vista_cuaderno(None)
                except Exception as ex:
                    mostrar_snack(f"Error al guardar: {ex}", "red")

            def marcar_como_pagado(ev):
                if not txt_id_pagar.value.strip():
                    return
                try:
                    num = int(txt_id_pagar.value.strip())
                    if num in mapa_ventas_ids:
                        db_id = mapa_ventas_ids[num]
                        supabase.table("ventas").update({"estado": "Pagado", "metodo_pago": "Efectivo"}).eq("id", db_id).execute()
                        txt_id_pagar.value = ""
                        mostrar_snack("¡Marcado como pagado!", "green")
                        mostrar_vista_cuaderno(None)
                except Exception as ex:
                    mostrar_snack(f"Error: {ex}", "red")

            def borrar_venta(ev):
                if not txt_id_borrar_venta.value.strip():
                    return
                try:
                    num = int(txt_id_borrar_venta.value.strip())
                    if num in mapa_ventas_ids:
                        db_id = mapa_ventas_ids[num]
                        res = supabase.table("ventas").select("inventario_id").eq("id", db_id).execute()
                        if res.data and len(res.data) > 0:
                            inv_id = res.data[0]["inventario_id"]
                            supabase.table("ventas").delete().eq("id", db_id).execute()
                            if inv_id and inv_id > 0:
                                supabase.table("pedazos_inventario").update({"estado": "Disponible"}).eq("id", inv_id).execute()
                            txt_id_borrar_venta.value = ""
                            mostrar_snack("Venta eliminada", "orange")
                            mostrar_vista_cuaderno(None)
                except Exception as ex:
                    mostrar_snack(f"Error: {ex}", "red")

            txt_buscar.on_change = mostrar_vista_cuaderno
            
            # Campos organizados verticalmente para que entren perfectamente en la pantalla del teléfono
            vista_principal.content = ft.Column(
                [
                    ft.Text("Registrar Venta (Formato Cuaderno)", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([txt_fecha, btn_calendario], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    txt_cliente,
                    txt_producto,
                    txt_peso,
                    txt_precio_total,
                    dd_metodo_pago,
                    dd_estado,
                    ft.Button("Registrar en el Cuaderno", icon=ft.Icons.CHECK, on_click=guardar_venta, bgcolor="amber", color="white"),
                    ft.Divider(),
                    ft.Text("Actualizar o Borrar Registros", size=16, weight=ft.FontWeight.BOLD),
                    txt_id_pagar,
                    ft.OutlinedButton("Marcar como Pagado", icon=ft.Icons.TASK_ALT, on_click=marcar_como_pagado),
                    txt_id_borrar_venta,
                    ft.OutlinedButton("Eliminar Venta", icon=ft.Icons.DELETE, on_click=borrar_venta, style=ft.ButtonStyle(color="red")),
                    ft.Divider(),
                    ft.Row([ft.Text("Historial de Registros", size=16, weight=ft.FontWeight.BOLD), txt_total_fiado], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    txt_buscar,
                    # Tabla envuelta en scroll horizontal para deslizar libremente de lado a lado
                    ft.Row([tabla_historial], scroll=ft.ScrollMode.AUTO),
                    ft.Container(height=250), # Espacio inferior para que el teclado no tape los campos
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
            )
            page.update()

        # ---------------------------------------------------------
        # VISTA INVENTARIO MÓVIL
        # ---------------------------------------------------------
        txt_nombre_barra = ft.TextField(label="Nombre / Tipo de Barra", hint_text="Ej: Barra Llanero 10kg", border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_peso_pedazo = ft.TextField(label="Peso del Pedazo Cortado", hint_text="Ej: 1.2kg o 750g", border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        txt_precio_pedazo = ft.TextField(label="Precio del Pedazo ($)", hint_text="Ej: 9000", keyboard_type=ft.KeyboardType.NUMBER, border=ft.OutlineInputBorder(border_radius=12), filled=True, bgcolor="white")
        
        mapa_inventario_ids = {}
        tabla_inventario = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nº")),
                ft.DataColumn(ft.Text("Barra / Origen")),
                ft.DataColumn(ft.Text("Peso")),
                ft.DataColumn(ft.Text("Precio ($)")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )

        def mostrar_vista_inventario(e=None):
            nonlocal mapa_inventario_ids
            mapa_inventario_ids = {}
            filas_inv = []
            
            try:
                res = supabase.table("pedazos_inventario").select("*").eq("usuario", usuario_actual["nombre"]).order("id", desc=False).execute()
                pedazos = res.data or []
                contador = 1
                for p in pedazos:
                    db_id = p["id"]
                    barra = p["nombre_barra"]
                    peso = p["peso_txt"]
                    precio = p["precio"]
                    estado = p["estado"]
                    mapa_inventario_ids[contador] = db_id
                    
                    def vender_directo(ev, pid=db_id, pbarra=barra, ppeso=peso, pprecio=precio):
                        txt_producto.value = pbarra
                        txt_peso.value = ppeso
                        txt_precio_total.value = str(pprecio)
                        pedazo_en_curso_id["id"] = pid
                        supabase.table("pedazos_inventario").update({"estado": "Vendido"}).eq("id", pid).execute()
                        mostrar_snack("Pedazo cargado para venta", "green")
                        mostrar_vista_cuaderno(None)
                        
                    def eliminar_pedazo(ev, pid=db_id):
                        supabase.table("pedazos_inventario").delete().eq("id", pid).execute()
                        mostrar_snack("Pedazo eliminado", "orange")
                        mostrar_vista_inventario(None)
                        
                    color_est = "green" if estado == "Disponible" else "red"
                    
                    btn_vender = ft.Button("Vender", icon=ft.Icons.SHOPPING_CART, on_click=vender_directo, bgcolor="amber", color="white", disabled=(estado == "Vendido"))
                    btn_eliminar = ft.IconButton(icon=ft.Icons.DELETE, icon_color="red", on_click=eliminar_pedazo)
                    
                    fila = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(contador))),
                            ft.DataCell(ft.Text(barra)),
                            ft.DataCell(ft.Text(peso)),
                            ft.DataCell(ft.Text(f"$ {int(precio):,}".replace(",", "."))),
                            ft.DataCell(ft.Container(content=ft.Text(estado, color="white", size=11), bgcolor=color_est, padding=5, border_radius=6)),
                            ft.DataCell(ft.Row([btn_vender, btn_eliminar])),
                        ]
                    )
                    filas_inv.append(fila)
                    contador += 1
                
                tabla_inventario.rows = filas_inv
                if tabla_inventario.page:
                    tabla_inventario.update()
            except Exception as ex:
                print(f"Error inventario: {ex}")

            def agregar_pedazo(ev):
                if not txt_nombre_barra.value or not txt_peso_pedazo.value or not txt_precio_pedazo.value:
                    mostrar_snack("Completa los datos del inventario", "red")
                    return
                try:
                    precio = int(txt_precio_pedazo.value.strip())
                    supabase.table("pedazos_inventario").insert({
                        "usuario": usuario_actual["nombre"],
                        "nombre_barra": txt_nombre_barra.value.strip(),
                        "peso_txt": txt_peso_pedazo.value.strip(),
                        "precio": precio,
                        "estado": "Disponible"
                    }).execute()
                    txt_nombre_barra.value = ""
                    txt_peso_pedazo.value = ""
                    txt_precio_pedazo.value = ""
                    mostrar_snack("¡Pedazo agregado a vitrina!", "green")
                    mostrar_vista_inventario(None)
                except Exception as ex:
                    mostrar_snack(f"Error: {ex}", "red")

            vista_principal.content = ft.Column(
                [
                    ft.Text("Cargar Pedazos de Queso (Picar Barra)", size=16, weight=ft.FontWeight.BOLD),
                    txt_nombre_barra,
                    txt_peso_pedazo,
                    txt_precio_pedazo,
                    ft.Button("Agregar Pedazo a Vitrina", icon=ft.Icons.ADD_SHOPPING_CART, on_click=agregar_pedazo, bgcolor="amber", color="white"),
                    ft.Divider(),
                    ft.Text("Stock de Pedazos en Vitrina", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([tabla_inventario], scroll=ft.ScrollMode.AUTO),
                    ft.Container(height=250),
                ],
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
            )
            page.update()

        btn_cuaderno = ft.Button("📖 Cuaderno", on_click=mostrar_vista_cuaderno, bgcolor="amber", color="white")
        btn_inventario = ft.Button("📦 Inventario", on_click=mostrar_vista_inventario, bgcolor="amber", color="white")
        
        mostrar_vista_cuaderno(None)
        body_container.content = ft.Column(
            [
                ft.Row([btn_cuaderno, btn_inventario], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=10),
                vista_principal,
            ],
            expand=True,
        )
        page.update()

    # ---------------------------------------------------------
    # COMPROBAR AL INICIAR SI EXISTE SESIÓN GUARDADA EN ARCHIVO
    # ---------------------------------------------------------
    usuario_guardado = leer_sesion_local()
    if usuario_guardado:
        usuario_actual["nombre"] = usuario_guardado
        cargar_pantalla_principal()
    else:
        cargar_pantalla_login()

if __name__ == "__main__":
    ft.run(main)

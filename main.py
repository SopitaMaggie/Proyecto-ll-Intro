import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from usuario import registrar_jugador, iniciar_sesion, obtener_ranking
from juego import Partida, BaseCentral
from defensor import Torre, Muro
from atacante import Unidad

FACCIONES = {
    "olimpo": {
        "nombre": "Olimpo",
        "descripcion": "Poder divino y rayos del cielo",
        "color_a": "#6aaa3c",
        "color_b": "#5e9c33",
        "color_preview": "#4a8c3f",
    },
    "oscura": {
        "nombre": "Oscura",
        "descripcion": "Sombras y neblina como escudo",
        "color_a": "#3a2060",
        "color_b": "#2e1850",
        "color_preview": "#5e35b1",
    },
    "volcan": {
        "nombre": "Volcán",
        "descripcion": "Fuego y lava protegen la base",
        "color_a": "#7d2c14",
        "color_b": "#5e2010",
        "color_preview": "#b5381d",
    }
}
#ventada de inicio
def vtn_principal():  # vtn= es ventana
    vtn = tk.Tk()
    vtn.title("Defensa y Asalto")
    vtn.geometry("1300x800")
    vtn.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/inicio.png").resize((1300, 800)))
    img_jugar = ImageTk.PhotoImage(Image.open("Imagenes/btn_jugar.png").resize((600, 350)))
    img_registrar = ImageTk.PhotoImage(Image.open("Imagenes/btn_login.png").resize((600, 350)) )
    img_ranking = ImageTk.PhotoImage(Image.open("Imagenes/btn_ranking.png").resize((600, 350)))
    img_info = ImageTk.PhotoImage(Image.open("Imagenes/btn_info.png").resize((600, 350)) )
    img_salir = ImageTk.PhotoImage( Image.open("Imagenes/btn_salir.png").resize((600, 350)))

    canvas = tk.Canvas(vtn, width=1300, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    X_BOTONES = 670
    Y_INICIAL = 360
    ESPACIO = 85

    canvas.create_image(X_BOTONES, Y_INICIAL, image=img_jugar)
    canvas.create_image(X_BOTONES, Y_INICIAL + ESPACIO, image=img_registrar)
    canvas.create_image(X_BOTONES, Y_INICIAL + ESPACIO * 2, image=img_ranking)
    canvas.create_image(X_BOTONES, Y_INICIAL + ESPACIO * 3, image=img_info)
    canvas.create_image(X_BOTONES, Y_INICIAL + ESPACIO * 4, image=img_salir)

    def Zclick(x1, y1, x2, y2, funcion):  # zona donde se hace click
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))
        return zona

    Zclick(430, 325, 910, 395, lambda: vtn_iniciar_sesion(vtn))
    Zclick(430, 410, 910, 480, lambda: vtn_registrarse(vtn))
    Zclick(430, 495, 910, 565, lambda: vtn_ranking(vtn))
    Zclick(430, 580, 910, 650, lambda: vtn_informacion(vtn))
    Zclick(430, 665, 910, 735, vtn.destroy)
    canvas.img_fondo = img_fondo
    canvas.img_jugar = img_jugar
    canvas.img_registrar = img_registrar
    canvas.img_ranking = img_ranking
    canvas.img_info = img_info
    canvas.img_salir = img_salir
    vtn.mainloop()

# Resgistrarse
def vtn_registrarse(principal):
    win = tk.Toplevel(principal)
    win.title("Registrarse")
    win.geometry("1300x800")
    win.resizable(False, False)
    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/fondo_registrar.png").resize((1300, 800)))
    img_btn_registrar = ImageTk.PhotoImage(Image.open("Imagenes/registrar.png").resize((800, 400)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 300)))

    canvas = tk.Canvas(win, width=1300, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    entry_user = tk.Entry(
        win,
        font=("Arial", 18),
        bg="#020b1d",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0,
        highlightthickness=0
    )
    canvas.create_window(
        680,
        310,
        width=500,
        height=28,
        window=entry_user
    )

    # Contraseña
    entry_pass = tk.Entry(
        win,
        font=("Arial", 18),
        bg="#020b1d",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0,
        highlightthickness=0,
        show="*"
    )
    canvas.create_window(
        680,
        410,
        width=500,
        height=28,
        window=entry_pass
    )

    # Nombre opcional
    entry_nombre = tk.Entry(
        win,
        font=("Arial", 18),
        bg="#020b1d",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0,
        highlightthickness=0
    )
    canvas.create_window(
        680,
        510,
        width=500,
        height=28,
        window=entry_nombre
    )

    canvas.create_image(650, 620, image=img_btn_registrar)
    canvas.create_image(650, 730, image=img_btn_volver)

    def registrar():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        nombre = entry_nombre.get().strip()
        if username == "" or password == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Usuario y contraseña son obligatorios.",
                parent=win
            )
            return
        if nombre == "":
            nombre = username
        jugador, msg = registrar_jugador(username, password, nombre)
        if jugador:
            messagebox.showinfo(
                "Registro exitoso",
                "Usuario registrado correctamente.\nYa puedes iniciar sesión.",
                parent=win
            )
            win.destroy()
            vtn_iniciar_sesion(principal)
        else:
            messagebox.showerror(
                "Error",
                msg,
                parent=win
            )
    def volver_menu():
        win.destroy()
    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))
    Zclick(500, 575, 800, 665, registrar)
    Zclick(540, 700, 760, 760, volver_menu)
    entry_user.bind("<Return>", lambda e: entry_pass.focus())
    entry_pass.bind("<Return>", lambda e: entry_nombre.focus())
    entry_nombre.bind("<Return>", lambda e: registrar())
    entry_user.focus()
    win.img_fondo = img_fondo
    win.img_btn_registrar = img_btn_registrar
    win.img_btn_volver = img_btn_volver

# inicio sesion
def vtn_iniciar_sesion(principal):
    win = tk.Toplevel(principal)
    win.title("Iniciar sesión")
    win.geometry("1300x800")
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/jugar_fondo.png").resize((1300, 800)))
    img_caja_usuario = ImageTk.PhotoImage(Image.open("Imagenes/caja_usuario.png").resize((700, 300)))
    img_caja_password = ImageTk.PhotoImage(Image.open("Imagenes/caja_password.png").resize((700, 300)) )
    img_btn_inicio = ImageTk.PhotoImage(Image.open("Imagenes/btn_inicio.png").resize((600, 400)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 300)))
    img_btn_registrar = ImageTk.PhotoImage(Image.open("Imagenes/registrar.png").resize((400, 250)))
    canvas = tk.Canvas(
        win,
        width=1300,
        height=800,
        highlightthickness=0
    )
    canvas.pack(fill="both", expand=True)
    canvas.create_image(
        0,
        0,
        image=img_fondo,
        anchor="nw"
    )
    canvas.create_image(
        780,
        660,
        image=img_btn_registrar)
    canvas.create_image(
        500,
        340,
        image=img_caja_usuario)
    canvas.create_image(
        500,
        435,
        image=img_caja_password)
    canvas.create_image(
        650,
        555,
        image=img_btn_inicio)
    canvas.create_image(
        650,
        730,
        image=img_btn_volver)
    entry_user = tk.Entry(
        win,
        font=("Arial", 18),
        bg="#001122",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0,
        highlightthickness=0
    )
    canvas.create_window(
        540,  # mover un poco a la derecha
        325,
        width=320,  # más largo
        height=28,
        window=entry_user
    )
    entry_pass = tk.Entry(
        win,
        font=("Arial", 18),
        bg="#001122",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0,
        highlightthickness=0,
        show="*"
    )
    canvas.create_window(
        540,  # misma posición horizontal
        420,
        width=320,  # más largo
        height=28,
        window=entry_pass
    )
    def login():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()

        if username == "" or password == "":
            messagebox.showwarning(
                "Campos vacíos",
                "Debes escribir usuario y contraseña.",
                parent=win
            )
            return
        jugador, msg = iniciar_sesion(username, password)
        if jugador:
            win.destroy()
            vtn_menu_juego(principal, jugador)
        else:
            messagebox.showerror(
                "Usuario no encontrado",
                "No existe este usuario o la contraseña es incorrecta.\n\nRegistra un usuario nuevo o revisa los datos.",
                parent=win
            )
    def abrir_registro():
        win.destroy()
        vtn_registrarse(principal)
    def volver_menu():
        win.destroy()
    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline="",
            fill=""
        )
        canvas.tag_bind(
            zona,
            "<Button-1>",
            lambda e: funcion()
        )
        canvas.tag_bind(
            zona,
            "<Enter>",
            lambda e: canvas.config(cursor="hand2")
        )
        canvas.tag_bind(
            zona,
            "<Leave>",
            lambda e: canvas.config(cursor="")
        )
    Zclick(375, 505, 925, 600, login)
    Zclick(370, 645, 930, 705, abrir_registro)
    Zclick(540, 700, 760, 760, volver_menu)
    Zclick(650,605,875,675,abrir_registro)
    entry_user.bind("<Return>", lambda e: entry_pass.focus())
    entry_pass.bind("<Return>", lambda e: login())
    entry_user.focus()
    win.img_fondo = img_fondo
    win.img_caja_usuario = img_caja_usuario
    win.img_caja_password = img_caja_password
    win.img_btn_inicio = img_btn_inicio
    win.img_btn_volver = img_btn_volver
    win.img_btn_registrar = img_btn_registrar

# menu de juego
def vtn_menu_juego(principal, jugador):
    win = tk.Toplevel(principal)
    win.title("Menú de juego")
    win.geometry("400x300")
    win.resizable(False, False)

    tk.Label(win, text=f"Bienvenido, {jugador.username}!", font=("Arial", 16, "bold")).pack(pady=30)

    tk.Button(win, text="Nueva partida", width=20, font=("Arial", 12),
              command=lambda: vtn_facciones(win, f"FACCIÓN — {jugador.username}",
                                            lambda f1: vtn_segunda_sesion(win, jugador, f1))).pack(pady=8)
    tk.Button(win, text="Ver ranking", width=20, font=("Arial", 12),
              command=lambda: vtn_ranking(win)).pack(pady=8)
    tk.Button(win, text="Cerrar sesión", width=20, font=("Arial", 12),
              command=win.destroy).pack(pady=8)


def vtn_facciones(padre, titulo, on_select):
    win = tk.Toplevel(padre)
    win.title("Seleccionar Facción")
    win.geometry("720x380")
    win.resizable(False, False)

    tk.Label(win, text=titulo, font=("Arial", 18, "bold")).pack(pady=20)

    frame_cards = tk.Frame(win)
    frame_cards.pack(pady=10)

    def seleccionar(faccion):
        win.destroy()
        on_select(faccion)

    for key, data in FACCIONES.items():
        card = tk.Frame(frame_cards, relief="solid", borderwidth=2, padx=10, pady=10)
        card.pack(side="left", padx=15)

        prev = tk.Canvas(card, width=160, height=90)
        prev.pack()
        for fi in range(3):
            for fj in range(3):
                color = data["color_a"] if (fi + fj) % 2 == 0 else data["color_b"]
                prev.create_rectangle(fj * 54, fi * 30, (fj + 1) * 54, (fi + 1) * 30,
                                      fill=color, outline="")

        tk.Label(card, text=data["nombre"], font=("Arial", 13, "bold")).pack(pady=5)
        tk.Button(card, text="Seleccionar", font=("Arial", 10),
                  bg=data["color_preview"], fg="black",
                  command=lambda k=key: seleccionar(k)).pack(pady=8)


# segunda sesion
def vtn_segunda_sesion(menu_win, jugador1, faccion1):
    win = tk.Toplevel(menu_win)
    win.title("Segundo jugador")
    win.geometry("350x250")
    win.resizable(False, False)

    tk.Label(win, text="SEGUNDO JUGADOR", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Label(win, text="Username:", font=("Arial", 11)).pack()
    entry_user = tk.Entry(win, font=("Arial", 11))
    entry_user.pack(pady=5)

    tk.Label(win, text="Password:", font=("Arial", 11)).pack()
    entry_pass = tk.Entry(win, font=("Arial", 11), show="*")
    entry_pass.pack(pady=5)

    def login_j2():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()
        jugador2, msg = iniciar_sesion(username, password)
        if jugador2:
            win.destroy()
            vtn_facciones(menu_win, f"FACCIÓN — {jugador2.username}",
                          lambda f2: vtn_partida(menu_win, jugador1, jugador2, faccion1, f2))
        else:
            messagebox.showerror("Error", msg, parent=win)

    tk.Button(win, text="Iniciar sesión", width=15, font=("Arial", 11), command=login_j2).pack(pady=15)


# ranking
def vtn_ranking(padre):
    win = tk.Toplevel(padre)
    win.title("Ranking")
    win.geometry("1000x800")
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(Image.open("Imagenes/fondo_rancking.png").resize((1000, 800)))
    img_btn_volver = ImageTk.PhotoImage(Image.open("Imagenes/volver.png").resize((400, 300)))
    canvas = tk.Canvas(win, width=1000, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")

    ranking_def, ranking_atk = obtener_ranking()

    y = 240
    for i, j in enumerate(ranking_def, 1):
        canvas.create_text(
            300, y,
            text=f"{i}. {j.username}  -  {j.victorias_defensor} victorias",
            fill="white",
            font=("Copperplate", 20, "bold")
        )
        y += 45

    y = 540
    for i, j in enumerate(ranking_atk, 1):
        canvas.create_text(
            300, y,
            text=f"{i}. {j.username}  -  {j.victorias_atacante} victorias",
            fill="white",
            font=("Copperplate", 20, "bold")
        )
        y += 45

    canvas.create_image(
        500, 780,
        image=img_btn_volver
    )
    def volver():
        win.destroy()
    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))
    Zclick(390, 710,610, 800,volver)
    win.img_fondo = img_fondo
    win.img_btn_volver = img_btn_volver

# informacion
def vtn_informacion(padre):
    win = tk.Toplevel(padre)
    win.title("Información")
    win.geometry("1000x800")
    win.resizable(False, False)

    img_fondo = ImageTk.PhotoImage(
        Image.open("Imagenes/informacion.png").resize((1000, 800)))
    img_btn_volver = ImageTk.PhotoImage(
        Image.open("Imagenes/volver.png").resize((400, 300)))
    canvas = tk.Canvas(win, width=1300, height=800, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")
    canvas.create_image(650,730,image=img_btn_volver)
    def volver():
        win.destroy()
    def Zclick(x1, y1, x2, y2, funcion):
        zona = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
        canvas.tag_bind(zona, "<Button-1>", lambda e: funcion())
        canvas.tag_bind(zona, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(zona, "<Leave>", lambda e: canvas.config(cursor=""))

    Zclick(540,700,760,760,volver)
    win.img_fondo = img_fondo
    win.img_btn_volver = img_btn_volver


# partida
CELL = 52  # cantidad de pixeles por celda
ESTILOS = {
    "olimpo": ("#1a5fb4", "OLI"),
    "oscura": ("#5e35b1", "OSC"),
    "volcan": ("#b5381d", "VOL"),
    "madera": ("#a0785a", "MUR"),
    "metal": ("#5e6264", "MET"),
    "flechas": ("#e07b00", "FLE"),
    "ninja": ("#2d3436", "NIN"),
    "reina_hielo": ("#4fc3f7", "REI"),
    "rey_barbaro": ("#7b3f00", "REY"),
    "fireball": ("#e01b24", "FIR"),
}


def cargar_imagen_faccion(faccion, tipo):
    try:
        ruta = f"Imagenes/facciones/{faccion}/{tipo}.png"
        img = Image.open(ruta).resize((CELL - 6, CELL - 6))
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


def vtn_partida(padre, jugador1, jugador2, faccion1, faccion2):
    partida = Partida(jugador1, jugador2)

    win = tk.Toplevel(padre)
    win.title("Partida")
    win.resizable(False, False)

    ronda_actual = [None]
    tipo_seleccionado = [None]
    turno = [1]
    imagenes_cache = {}

    frame_info = tk.Frame(win, bg="#1e1e2e", width=210, padx=10, pady=10)
    frame_info.grid(row=0, column=0, sticky="ns")
    frame_info.grid_propagate(False)

    canvas = tk.Canvas(win, width=10 * CELL, height=10 * CELL)
    canvas.grid(row=0, column=1)

    #  Fondo con facción de cada jugador
    def dibujar_fondo():
        canvas.delete("fondo")
        if partida.defensor_actual is jugador1:
            f_atk = FACCIONES[faccion2]
            f_def = FACCIONES[faccion1]
        else:
            f_atk = FACCIONES[faccion1]
            f_def = FACCIONES[faccion2]

        for i in range(10):
            for j in range(10):
                if j <= 4:
                    color = f_atk["color_a"] if (i + j) % 2 == 0 else f_atk["color_b"]
                else:
                    color = f_def["color_a"] if (i + j) % 2 == 0 else f_def["color_b"]
                canvas.create_rectangle(j * CELL, i * CELL,
                                        (j + 1) * CELL, (i + 1) * CELL,
                                        fill=color, outline="", tags="fondo")

        canvas.create_rectangle(9 * CELL + 3, 4 * CELL + 3,
                                10 * CELL - 3, 5 * CELL - 3,
                                fill="#f6d32d", outline="#e5a50a", width=2, tags="fondo")

    #  Capa 1: grilla durante colocación
    def mostrar_grilla():
        canvas.delete("grilla")
        for i in range(11):
            canvas.create_line(0, i * CELL, 10 * CELL, i * CELL,
                               fill="white", width=1, tags="grilla")
        for j in range(11):
            canvas.create_line(j * CELL, 0, j * CELL, 10 * CELL,
                               fill="white", width=1, tags="grilla")

    def ocultar_grilla():
        canvas.delete("grilla")

    #  Panel de info
    s = {"bg": "#1e1e2e", "fg": "white"}

    lbl_ronda = tk.Label(frame_info, text="", font=("Arial", 13, "bold"), **s)
    lbl_ronda.pack(pady=(5, 2))

    lbl_fase = tk.Label(frame_info, text="", font=("Arial", 10), **s)
    lbl_fase.pack()

    lbl_dinero = tk.Label(frame_info, text="", font=("Arial", 10), **s)
    lbl_dinero.pack(pady=(0, 10))

    tk.Label(frame_info, text="Selecciona tipo:", font=("Arial", 10, "bold"), **s).pack()

    frame_tipos = tk.Frame(frame_info, bg="#1e1e2e")
    frame_tipos.pack()

    lbl_log = tk.Label(frame_info, text="", font=("Arial", 9),
                       wraplength=190, justify="left", fg="#a6e3a1", bg="#1e1e2e")
    lbl_log.pack(pady=8)

    btn_accion = tk.Button(frame_info, font=("Arial", 10), width=18)
    btn_accion.pack(pady=5)

    #  Capa 2: dibujar entidades
    def dibujar_entidades():
        canvas.delete("entidad")
        ronda = ronda_actual[0]

        if partida.defensor_actual is jugador1:
            faccion_def = faccion1
            faccion_atk = faccion2
        else:
            faccion_def = faccion2
            faccion_atk = faccion1

        for i in range(10):
            for j in range(10):
                celda = ronda.mapa.obtener(i, j)
                if celda is None:
                    continue
                cx = j * CELL + CELL // 2
                cy = i * CELL + CELL // 2
                x1, y1 = j * CELL + 5, i * CELL + 5
                x2, y2 = (j + 1) * CELL - 5, (i + 1) * CELL - 5

                if isinstance(celda, BaseCentral):
                    pct = celda.vida / celda.vida_max
                    barra = int((CELL - 10) * pct)
                    canvas.create_rectangle(x1, y1, x1 + barra, y1 + 7,
                                            fill="#26a269", outline="", tags="entidad")
                    canvas.create_text(cx, cy + 4, text=f"BASE\n{celda.vida}",
                                       fill="#1a1a1a", font=("Arial", 7, "bold"), tags="entidad")
                    continue

                if isinstance(celda, (Torre, Muro)):
                    faccion_entidad = faccion_def
                else:
                    faccion_entidad = faccion_atk

                clave = f"{faccion_entidad}_{celda.tipo}"
                if clave not in imagenes_cache:
                    imagenes_cache[clave] = cargar_imagen_faccion(faccion_entidad, celda.tipo)

                img = imagenes_cache[clave]
                if img:
                    canvas.create_image(cx, cy, image=img, tags="entidad")
                else:
                    color, letra = ESTILOS[celda.tipo]
                    if isinstance(celda, Unidad):
                        canvas.create_oval(x1, y1, x2, y2, fill=color,
                                           outline="white", width=1, tags="entidad")
                    else:
                        canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                                outline="white", width=1, tags="entidad")
                    canvas.create_text(cx, cy, text=letra, fill="white",
                                       font=("Arial", 8, "bold"), tags="entidad")

    #  Iniciar ronda
    def iniciar_ronda():
        ronda_actual[0] = partida.iniciar_ronda()
        tipo_seleccionado[0] = None
        turno[0] = 1
        dibujar_fondo()
        dibujar_entidades()
        mostrar_fase_defensor()

    #  Fase defensor
    def mostrar_fase_defensor():
        ronda = ronda_actual[0]
        lbl_ronda.config(text=f"Ronda {partida.ronda_actual}")
        lbl_fase.config(text=f"DEFENSOR: {ronda.jugador_defensor.username}")
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_defensor}")
        lbl_log.config(text="")
        mostrar_grilla()
        for w in frame_tipos.winfo_children():
            w.destroy()

        tk.Label(frame_tipos, text="TORRES", bg="#1e1e2e", fg="#f6d32d",
                 font=("Arial", 9, "bold")).pack(pady=(4, 2))

        for tipo, datos in Torre.TIPOS.items():
            costo = datos["costo"]
            nombre = datos["nombre"]
            color = ESTILOS[tipo][0]
            tk.Button(
                frame_tipos,
                text=f"{nombre} (${costo})",
                width=22,
                font=("Arial", 8),
                bg=color,
                fg="black",
                command=lambda t=tipo: seleccionar(t)
            ).pack(pady=2)
        tk.Label(frame_tipos, text="MUROS", bg="#1e1e2e", fg="#f6d32d",
                 font=("Arial", 9, "bold")).pack(pady=(8, 2))

        for tipo, datos in Muro.TIPOS.items():
            costo = datos["costo"]
            nombre = datos["nombre"]
            color = ESTILOS[tipo][0]

            tk.Button(
                frame_tipos,
                text=f"{nombre} (${costo})",
                width=22,
                font=("Arial", 8),
                bg=color,
                fg="black",
                command=lambda t=tipo: seleccionar(t)
            ).pack(pady=2)

        btn_accion.config(
            text="Terminar colocación",
            bg="#e0c800",
            fg="black",
            state="normal",
            command=lambda: mostrar_fase_atacante()
        )
        canvas.bind("<Button-1>", clic_defensor)

    def clic_defensor(event):
        col = event.x // CELL
        fila = event.y // CELL
        tipo = tipo_seleccionado[0]
        if not tipo:
            lbl_log.config(text="Primero selecciona un tipo.")
            return
        ronda = ronda_actual[0]
        if tipo in Torre.TIPOS:
            ok, msg = ronda.defensor_colocar_torre(tipo, fila, col)
        else:
            ok, msg = ronda.defensor_colocar_muro(tipo, fila, col)
        lbl_log.config(text=msg)
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_defensor}")
        dibujar_entidades()

    #  Fase atacante 
    def mostrar_fase_atacante():
        ronda = ronda_actual[0]
        lbl_fase.config(text=f"ATACANTE: {ronda.jugador_atacante.username}")
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_atacante}")
        lbl_log.config(text="")
        tipo_seleccionado[0] = None
        mostrar_grilla()

        for w in frame_tipos.winfo_children():
            w.destroy()

        tk.Label(frame_tipos, text="UNIDADES", bg="#1e1e2e", fg="#f6d32d",
                 font=("Arial", 9, "bold")).pack(pady=(4, 2))

        for tipo, datos in Unidad.TIPOS.items():
            costo = datos["costo"]
            nombre = datos["nombre"]
            color = ESTILOS[tipo][0]

            tk.Button(
                frame_tipos,
                text=f"{nombre} (${costo})",
                width=22,
                font=("Arial", 8),
                bg=color,
                fg="black",
                command=lambda t=tipo: seleccionar(t)
            ).pack(pady=2)

        btn_accion.config(
            text="Iniciar combate",
            bg="#e01b24",
            fg="white",
            state="normal",
            command=lambda: iniciar_combate()
        )

        canvas.bind("<Button-1>", clic_atacante)

    def clic_atacante(event):
        col = event.x // CELL
        fila = event.y // CELL
        tipo = tipo_seleccionado[0]
        if not tipo:
            lbl_log.config(text="Primero selecciona un tipo.")
            return
        ronda = ronda_actual[0]
        ok, msg = ronda.atacante_colocar_unidad(tipo, fila, col)
        lbl_log.config(text=msg)
        lbl_dinero.config(text=f"Dinero: {ronda.dinero_atacante}")
        dibujar_entidades()

    #  Fase combate
    def iniciar_combate():
        canvas.unbind("<Button-1>")
        ocultar_grilla()
        for w in frame_tipos.winfo_children():
            w.destroy()
        lbl_fase.config(text="COMBATE")
        btn_accion.config(state="disabled")
        turno[0] = 1
        auto_turno()

    def auto_turno():
        ronda = ronda_actual[0]
        ronda.ejecutar_turno_combate()
        dibujar_entidades()
        base = ronda.mapa.base
        lbl_dinero.config(text=f"Base: {base.vida}/{base.vida_max}")
        lbl_log.config(text=f"Turno {turno[0]}")
        turno[0] += 1

        if ronda.terminada:
            partida.registrar_resultado_ronda(ronda.ganador_rol)
            ganador = "ATACANTE" if ronda.ganador_rol == "atacante" else "DEFENSOR"
            lbl_log.config(text=f"¡Ganó el {ganador}!")
            btn_accion.config(state="normal")

            if partida.terminada:
                partida.actualizar_victorias_jugadores()
                btn_accion.config(text=f"¡{partida.ganador.username} gana!",
                                  bg="#26a269", fg="white", command=lambda: None)
            else:
                btn_accion.config(text="Siguiente ronda", bg="#1a5fb4", fg="white",
                                  command=iniciar_ronda)
        else:
            win.after(700, auto_turno)

    def seleccionar(tipo):
        tipo_seleccionado[0] = tipo
        if tipo in Torre.TIPOS:
            nombre = Torre.TIPOS[tipo]["nombre"]
            lbl_log.config(text=f"Torre seleccionada: {nombre}")
        elif tipo in Muro.TIPOS:
            nombre = Muro.TIPOS[tipo]["nombre"]
            lbl_log.config(text=f"Muro seleccionado: {nombre}")
        elif tipo in Unidad.TIPOS:
            nombre = Unidad.TIPOS[tipo]["nombre"]
            lbl_log.config(text=f"Unidad seleccionada: {nombre}")
        else:
            lbl_log.config(text=f"Seleccionado: {tipo}")

    iniciar_ronda()
vtn_principal()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Model.ConexionUsuario import ConexionUsuario
from PIL import Image, ImageTk
from Controller.Juego import Juego
import tkinter as tk
from Tooltip import Tooltip 
import pygame
import threading

class Loggin():

    def Crear_Cuenta(self, event=None):
        # Configura los botones de la interfaz antes de crear la cuenta
        self.Botones()
        juego = Juego()
        try:
            # Crea una cuenta con el nombre de usuario y contraseña proporcionados
            juego.Crear_Cuenta(self.txtCreaUsuario.get(), self.txtCreaContraseña.get())
            pygame.mixer.music.stop()
        except Exception as e:
            # Muestra un mensaje de error si falla la creación de la cuenta
            messagebox.showerror("Error", f"Error al crear la cuenta: {e}")
                    
    def Record(self, event=None):
        try:
            # Configura los botones de la interfaz antes de mostrar el récord
            self.Botones()
            miConexion = ConexionUsuario()
            miConexion.crearConexion()
            con = miConexion.getConexion()
            cursor = con.cursor()
            # Selecciona y ordena los récords de los jugadores desde la base de datos
            cursor.execute("SELECT jugador.nombre, record.record, record.record FROM record JOIN jugador ON record.jugador = jugador.nombre ORDER BY record.record DESC")
            listaJugadores = cursor.fetchall()
            for index, jugador in enumerate(listaJugadores, start=1):
                nombre = jugador[0]
                record = jugador[1]
                self.datos.insert("", "end", values=(index, nombre, record))
        except Exception as e:
            # Muestra un mensaje de error si falla la generación del reporte
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")
   
    def Loggin(self, event=None):
        # Inicia sesión con el nombre de usuario y contraseña proporcionados
        juego = Juego()
        self.Botones()
        try:
            juego.Loggin(self.txtusuario.get(), self.txtpassword.get())
            pygame.mixer.music.stop()
        except Exception as e:
            # Muestra un mensaje de error si falla el inicio de sesión
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")
     
    def show_login_frame(self):
        # Muestra el marco de inicio de sesión
        self.Botones()
        self.clear_frame()
        self.loggin_ventana.place(relwidth=1, relheight=1)

    def show_register_frame(self):
        # Muestra el marco de registro
        self.Botones()
        self.clear_frame()
        self.registro_ventana.place(relwidth=1, relheight=1)

    def clear_frame(self):
        # Borra todos los widgets del marco principal
        for widget in self.main_frame.winfo_children():
            widget.place_forget()

    def show_main_frame(self, event=None):
        # Muestra el marco principal
        self.Botones()
        self.clear_frame()
        self.button_frame.place(relwidth=1, relheight=1)

    def record(self):
        # Muestra el marco de récord
        self.Botones()
        self.clear_frame()
        self.registro_record.place(relwidth=1, relheight=1)

    def Usuario(self, event):
        # Valida la entrada del nombre de usuario
        caracter = event.keysym
        if caracter.isalnum():
            self.txtusuario.configure(background='#90EE90')
        else:
            self.txtusuario.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtusuario.delete(len(self.txtusuario.get()) - 1, tk.END)

    def Contraseña(self, event):
        # Valida la entrada de la contraseña
        caracter = event.keysym
        if caracter.isdigit():
            self.txtpassword.configure(background='#90EE90')
        else:
            self.txtpassword.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtpassword.delete(len(self.txtpassword.get()) - 1, tk.END)
        if (len(self.txtusuario.get()) >= 5 and len(self.txtpassword.get()) >= 5):
            self.btnEntrar.config(state="normal") 
        else:
            self.btnEntrar.config(state="disabled") 

    def CrearUsuario(self, event):
        # Valida la entrada del nombre de usuario para crear una cuenta
        caracter = event.keysym
        if caracter.isalnum():
            self.txtCreaUsuario.configure(background='#90EE90')
        else:
            self.txtCreaUsuario.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtCreaUsuario.delete(len(self.txtCreaUsuario.get()) - 1, tk.END)

    def CrearContraseña(self, event):
        # Valida la entrada de la contraseña para crear una cuenta
        caracter = event.keysym
        if caracter.isdigit():
            self.txtCreaContraseña.configure(background='#90EE90')
        else:
            self.txtCreaContraseña.configure(background='#FFCCCC')
            if event.keysym != "BackSpace":
                self.txtCreaContraseña.delete(len(self.txtCreaContraseña.get()) - 1, tk.END)
        if (len(self.txtCreaUsuario.get()) >= 5 and len(self.txtCreaContraseña.get()) >= 5):
            self.btnRegistro.config(state="normal") 
        else:
            self.btnRegistro.config(state="disabled") 

    def verCaracteresLoggin(self, event=None):
        """
        Muestra los caracteres de la contraseña en texto plano.

        Args:
            event: Evento de disparo (por defecto None).
        """
        self.VerContraseñaSonido()
        self.txtpassword.configure(show='')
        self.btnVer.config(image=self.iconoOculto)

    def ocultarCaracteresLoggin(self, event):
        """
        Oculta los caracteres de la contraseña sustituyéndolos por asteriscos.

        Args:
            event: Evento de disparo.
        """
        self.VerContraseñaSonido()
        self.txtpassword.configure(show='*')
        self.btnVer.config(image=self.iconoVer)

    def verCaracteresCrear(self, event=None):
        """
        Muestra los caracteres de la contraseña en texto plano.

        Args:
            event: Evento de disparo (por defecto None).
        """
        self.VerContraseñaSonido()
        self.txtCreaContraseña.configure(show='')
        self.btnVer1.config(image=self.iconoOculto)

    def ocultarCaracteresCrear(self, event):
        """
        Oculta los caracteres de la contraseña sustituyéndolos por asteriscos.

        Args:
            event: Evento de disparo.
        """
        self.VerContraseñaSonido()
        self.txtCreaContraseña.configure(show='*')
        self.btnVer1.config(image=self.iconoVer)

    def mostrarAyuda(self, event):
        """
        Muestra un mensaje de ayuda al usuario.

        Args:
            event (tk.Event): Evento que desencadena la llamada a esta función.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Debe diligencia usuario y contraseña, luego presionar el botón crear o entrar.")

    def mostrarAyudaRecord(self, event):
        """
        Muestra un mensaje de ayuda al usuario.

        Args:
            event (tk.Event): Evento que desencadena la llamada a esta función.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Los datos que se muestran son los record de todos los jugadores.")
    
    def mostrarAyudaInicio(self, event):
        """
        Muestra un mensaje de ayuda al usuario.

        Args:
            event (tk.Event): Evento que desencadena la llamada a esta función.
        """
        self.Ayuda()
        messagebox.showinfo("Ayuda", "El botón iniciar sesión sirve para loguiarse e iniciar el juego,\n el botón crear cuenta sirve para registrarse e iniciar el juego \n y el botón puntaje sirve para ver los records")

    def Ayuda(self):
        """
        Reproduce un sonido de ayuda para proporcionar asistencia al usuario.
        """
        def music_thread_function():
            botones_sound = pygame.mixer.Sound(r'sound\ayuda.mp3')
            botones_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Botones(self):
        """
        Reproduce un sonido al darle click a los botones .
        """
        def music_thread_function():
            botones_sound = pygame.mixer.Sound(r'sound\cartoon130.mp3')
            botones_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()
    
    def VerContraseñaSonido(self):
        """
        Reproduce un sonido al darle click en el botón para ver la contraseña .
        """
        def music_thread_function():
            ver_sound = pygame.mixer.Sound(r'sound\scanner-beep-checkout.mp3')
            ver_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def inicio(self):
        """
        Reproduce un sonido al iniciar .
        """
        def music_thread_function():
            pygame.mixer.music.load(r'sound\gravity-falls-theme.mp3')
            pygame.mixer.music.play(-1)

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()


    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de Sesión")
        self.ventana.resizable(0, 0)
        self.ventana.geometry("600x500")

        # Inicializa pygame y el mezclador de audio
        pygame.init()
        pygame.mixer.init()
        self.music_thread = None

        # Cargar y ajustar la imagen de fondo
        self.imagen_fondo = Image.open(r"iconos\Designer.jpeg")
        self.imagen_fondo = self.imagen_fondo.resize((600, 500), Image.Resampling.LANCZOS)
        self.imagen = ImageTk.PhotoImage(self.imagen_fondo)
        
        # Crear el frame principal con la imagen de fondo
        self.main_frame = tk.Label(self.ventana, image=self.imagen)
        self.main_frame.place(relwidth=1, relheight=1)

        # Configurar estilos para los widgets
        self.style = ttk.Style()    
        self.style.configure('TLabel', font=('Lucida Console', 12), background='black', foreground='white')
        self.style.configure('TEntry', font=('Lucida Console', 12))

        #  # Definir un nuevo estilo para los botones
        self.style.configure('Purple.TButton', font=('Arial', 12), background='black', foreground='white')
        self.style.map('Purple.TButton', background=[('active', 'black')], foreground=[('active', 'white')])

        # Botones iniciales
        self.button_frame = tk.Frame(self.main_frame, bg="", highlightthickness=0)
        self.button_frame.place(relwidth=1, relheight=1)

         # Etiqueta del título principal
        self.lblTitulo = tk.Label(self.button_frame, text="JUEGA AHORCADO", font=("Lucida Console", 25), fg="white", bg="black")
        self.lblTitulo.place(relx=0.5, rely=0.2, anchor="center")

        iconologgin = Image.open(r"iconos\casa_preview_rev_1.png")
        iconologgin = iconologgin.resize((30, 30))
        self.iconologgin = ImageTk.PhotoImage(iconologgin)
        self.btnLoggin = ttk.Button(self.button_frame, image=self.iconologgin, text="Iniciar Sesión", compound="left", command=self.show_login_frame, style='Purple.TButton')
        self.btnLoggin.place(relx=0.5, rely=0.4, anchor="center", width=150, height=50)

        iconoCrear = Image.open(r"iconos\usuario_preview_rev_1.png")
        iconoCrear = iconoCrear.resize((30, 30))
        self.iconoCrear = ImageTk.PhotoImage(iconoCrear)
        self.btnCrear = ttk.Button(self.button_frame, image=self.iconoCrear, text="Crear Usuario", compound="left", command=self.show_register_frame, style='Purple.TButton')
        self.btnCrear.place(relx=0.5, rely=0.6, anchor="center", width=150, height=50)

        iconoRecord = Image.open(r"iconos\ganador_preview_rev_1.png")
        iconoRecord = iconoRecord.resize((30, 30))
        self.iconoRecord = ImageTk.PhotoImage(iconoRecord)
        self.btnRecord = ttk.Button(self.button_frame, image=self.iconoRecord, text=" Puntaje", command=self.record, compound="left", style='Purple.TButton')
        self.btnRecord.place(relx=0.5, rely=0.8, anchor="center", width=150, height=50)

        iconoAyuda = Image.open(r"iconos\pregunta_preview_rev_1.png")
        iconoAyuda = iconoAyuda.resize((27, 27))
        self.iconoAyuda = ImageTk.PhotoImage(iconoAyuda)
        self.btnAyuda =ttk.Button(self.button_frame, image=self.iconoAyuda, style='Purple.TButton')
        self.btnAyuda.place(relx=1, x=-37, y=15, width=35, height=35)
        Tooltip(self.btnAyuda, "Presione para obtener ayuda!\nAlt+d")
        self.btnAyuda.bind('<Button-1>', self.mostrarAyudaInicio)
        self.ventana.bind('<Alt-d>', self.mostrarAyudaInicio)

        # Frame de Iniciar Sesión
        self.loggin_ventana = tk.Frame(self.main_frame, bg="", highlightthickness=0)

        iconoVer = Image.open(r"iconos\show_preview_rev_1.png")
        iconoVer = iconoVer.resize((30, 30))
        self.iconoVer = ImageTk.PhotoImage(iconoVer)

        iconoOculto = Image.open(r"iconos\ojo_preview_rev_1.png")  
        iconoOculto = iconoOculto.resize((30, 30))
        self.iconoOculto = ImageTk.PhotoImage(iconoOculto)

        self.btnVer = ttk.Button(self.loggin_ventana, image=self.iconoVer, style='Purple.TButton', compound="left")
        self.btnVer.place(relx=0.7, rely=0.57, width=40, height=40)
        Tooltip(self.btnVer, "Presione para ver la contraseña!\nAlt+v")
        self.btnVer.bind("<Button-1>", self.verCaracteresLoggin)
        self.btnVer.bind("<ButtonRelease-1>", self.ocultarCaracteresLoggin)
        self.ventana.bind("<Alt-v>", self.verCaracteresLoggin)

        self.login_label = ttk.Label(self.loggin_ventana, text="Iniciar Sesión", style='TLabel')
        self.login_label.place(relx=0.5, rely=0.1, anchor="center")

        self.lblusuario = ttk.Label(self.loggin_ventana, text="Usuario:", style='TLabel')
        self.lblusuario.place(relx=0.5, rely=0.3, anchor="center")
        self.txtusuario = ttk.Entry(self.loggin_ventana, style='TEntry')
        self.txtusuario.place(relx=0.5, rely=0.4, anchor="center", width=200, height=30)
        self.txtusuario.bind("<KeyRelease>", self.Usuario)
        self.txtusuario.insert(0, "Ej:Laratatiana123")
        self.txtusuario.bind("<Button-1>", lambda event:self.txtusuario.delete(0, tk.END))

        self.lblpassword = ttk.Label(self.loggin_ventana, text="Contraseña:", style='TLabel')
        self.lblpassword.place(relx=0.5, rely=0.5, anchor="center")
        self.txtpassword = ttk.Entry(self.loggin_ventana, show="*", style='TEntry')
        self.txtpassword.place(relx=0.5, rely=0.6, anchor="center", width=200, height=30)
        self.txtpassword.bind("<KeyRelease>", self.Contraseña)
        Tooltip(self.txtpassword, "Ingrese una contraseña")

        iconoRegistro = Image.open(r"iconos\tocar (1)_preview_rev_1.png")
        iconoRegistro = iconoRegistro.resize((20, 20))
        self.iconoRegistro = ImageTk.PhotoImage(iconoRegistro)
        self.btnEntrar = ttk.Button(self.loggin_ventana, image=self.iconoRegistro, text=" Entrar", compound="left",command=lambda: self.Loggin(), style='Purple.TButton', state="disabled")
        self.btnEntrar.place(relx=0.4, rely=0.7, anchor="center", width=100, height=30)
        Tooltip(self.btnEntrar, "Precione para ingresar al juego!\nAlt+e")
        self.ventana.bind("<Alt-e>", self.Loggin) 

        iconoVolverL = Image.open(r"C:\Users\ASUS\Downloads\Mini proyecto\iconos\flecha - copia.png")
        iconoVolverL = iconoVolverL.resize((20, 20))
        self.iconoVolverL = ImageTk.PhotoImage(iconoVolverL)
        self.btnVolverLogin = ttk.Button(self.loggin_ventana, image=self.iconoVolverL, text=" Volver", compound="left", command=self.show_main_frame, style='Purple.TButton')
        self.btnVolverLogin.place(relx=0.6, rely=0.7, anchor="center", width=100, height=30)
        Tooltip(self.btnVolverLogin, "Presione para volver al menú principal!\nAlt+r")
        self.ventana.bind("<Alt-r>", self.show_main_frame) 

        iconoAyuda2 = Image.open(r"iconos\pregunta_preview_rev_1.png")
        iconoAyuda2 = iconoAyuda2.resize((27, 27))
        self.iconoAyuda2 = ImageTk.PhotoImage(iconoAyuda2)
        self.btnAyuda2 =ttk.Button(self.loggin_ventana, image=self.iconoAyuda2, style='Purple.TButton')
        self.btnAyuda2.place(relx=1, x=-37, y=15, width=35, height=35)
        Tooltip(self.btnAyuda2, "Presione para obtener ayuda!\nAlt+c")
        self.btnAyuda2.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-c>', self.mostrarAyuda)

        # Frame de Crear Usuario
        self.registro_ventana = tk.Frame(self.main_frame, bg="", highlightthickness=0)

        self.lblRegistro = ttk.Label(self.registro_ventana, text="Crear Usuario", style='TLabel')
        self.lblRegistro.place(relx=0.5, rely=0.1, anchor="center")
        
        self.btnVer1 = ttk.Button(self.registro_ventana, image=self.iconoVer, style='Purple.TButton', compound="center")
        self.btnVer1.place(relx=0.7, rely=0.57, width=40, height=40)
        Tooltip(self.btnVer1, "Presione para ver la contraseña!\nAlt+v")
        self.btnVer1.bind("<Button-1>", self.verCaracteresCrear)
        self.btnVer1.bind("<ButtonRelease-1>", self.ocultarCaracteresCrear)
        self.ventana.bind("<Alt-v>", self.verCaracteresCrear)

        self.lblCreaUsuario = ttk.Label(self.registro_ventana, text="Nuevo Usuario:", style='TLabel')
        self.lblCreaUsuario.place(relx=0.5, rely=0.3, anchor="center")
        self.txtCreaUsuario = ttk.Entry(self.registro_ventana, style='TEntry')
        self.txtCreaUsuario.place(relx=0.5, rely=0.4, anchor="center", width=200, height=30)
        self.txtCreaUsuario.bind("<KeyRelease>", self.CrearUsuario)
        self.txtCreaUsuario.insert(0, "Ej:Laratatiana123")
        self.txtCreaUsuario.bind("<Button-1>", lambda event:self.txtCreaUsuario.delete(0, tk.END))
        
        self.lblCreaContraseña = ttk.Label(self.registro_ventana, text="Contraseña:", style='TLabel')
        self.lblCreaContraseña.place(relx=0.5, rely=0.5, anchor="center")
        self.txtCreaContraseña = ttk.Entry(self.registro_ventana, show="*", style='TEntry')
        self.txtCreaContraseña.place(relx=0.5, rely=0.6, anchor="center", width=200, height=30)
        self.txtCreaContraseña.bind("<KeyRelease>", self.CrearContraseña)
        Tooltip(self.txtCreaContraseña, "Ingrese una contraseña")

        self.btnRegistro = ttk.Button(self.registro_ventana, image=self.iconoRegistro, text=" Registrar", compound="left", command=lambda: self.Crear_Cuenta(), state="disabled", style='Purple.TButton')
        self.btnRegistro.place(relx=0.4, rely=0.7, anchor="center", width=100, height=30)
        Tooltip(self.btnRegistro, "Precione para ingresar al juego!\nAlt+e")
        self.ventana.bind("<Alt-e>", self.Crear_Cuenta) 

        self.btnVolverRegistro = ttk.Button(self.registro_ventana, image=self.iconoVolverL, text=" Volver", compound="left", command=self.show_main_frame, style='Purple.TButton')
        self.btnVolverRegistro.place(relx=0.6, rely=0.7, anchor="center", width=100, height=30)
        Tooltip(self.btnVolverRegistro, "Presione para volver al menú principal!\nAlt+r")
        self.ventana.bind("<Alt-r>", self.show_main_frame) 

        iconoAyuda3 = Image.open(r"iconos\pregunta_preview_rev_1.png")
        iconoAyuda3 = iconoAyuda3.resize((27, 27))
        self.iconoAyuda3 = ImageTk.PhotoImage(iconoAyuda3)
        self.btnAyuda3 =ttk.Button(self.registro_ventana, image=self.iconoAyuda3, style='Purple.TButton')
        self.btnAyuda3.place(relx=1, x=-37, y=15, width=35, height=35)
        Tooltip(self.btnAyuda3, "Presione para obtener ayuda!\nAlt+a")
        self.btnAyuda3.bind('<Button-1>', self.mostrarAyuda)
        self.ventana.bind('<Alt-a>', self.mostrarAyuda)

        # Frame de record 
        self.registro_record = tk.Frame(self.main_frame, bg="", highlightthickness=0)

        self.datos = ttk.Treeview(self.registro_record, columns=("N", "Nombre de usuario", "Record"), show="headings")
        self.datos.column("N", width=25, anchor=tk.CENTER)
        self.datos.heading("Nombre de usuario", text="Nombre de usuario")
        self.datos.heading("Record", text="Record")
        self.datos.place(relx=0.5, rely=0.5, anchor="center")
        self.Record()

        self.datos.column("#0", width=0, stretch=tk.NO) 
        self.datos.column("N", width=25, anchor=tk.CENTER)
        self.datos.column("Nombre de usuario", width=250, anchor=tk.CENTER)
        self.datos.column("Record", width=250, anchor=tk.CENTER)

        self.btnVolverRegistro = ttk.Button(self.registro_record, image=self.iconoVolverL, text=" Volver", compound="left", command=self.show_main_frame, style='Purple.TButton')
        self.btnVolverRegistro.place(relx=0.5, rely=0.8, anchor="center", width=100, height=30)
        Tooltip(self.btnVolverRegistro, "Presione para volver al menú principal!\nAlt+r")
        self.ventana.bind("<Alt-r>", self.show_main_frame) 
        
        iconoAyuda4 = Image.open(r"iconos\pregunta_preview_rev_1.png")
        iconoAyuda4 = iconoAyuda.resize((27, 27))
        self.iconoAyuda4 = ImageTk.PhotoImage(iconoAyuda4)
        self.btnAyuda4 =ttk.Button(self.registro_record, image=self.iconoAyuda4, style='Purple.TButton')
        self.btnAyuda4.place(relx=1, x=-37, y=15, width=35, height=35)
        Tooltip(self.btnAyuda4, "Presione para obtener ayuda!\nAlt+o")
        self.btnAyuda4.bind('<Button-1>', self.mostrarAyudaRecord)
        self.ventana.bind('<Alt-o>', self.mostrarAyudaRecord)
        
        
        
        self.inicio()
        self.ventana.mainloop()

      











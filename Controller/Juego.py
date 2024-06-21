from tkinter import messagebox
from Model.ConexionUsuario import ConexionUsuario
import threading
import pygame
from View.Ahorcado import Ahorcado

class Juego():
    def __init__(self, nombre="", password=""):
        # Inicializa los atributos de la clase Juego
        self.nombre = nombre
        self.password = password
        self.record = 0

    def getNombre(self):
        # Retorna el nombre del jugador
        return self.nombre
    
    def getPassword(self):
        # Retorna la contraseña del jugador
        return self.password
    
    def setNombre(self, nombre):
        # Establece el nombre del jugador
        self.nombre = nombre
    
    def setPassword(self, password):
        # Establece la contraseña del jugador
        self.password = password
    
    def getRecord(self):
        # Retorna el récord del jugador
        return self.record
    
    def setRecord(self, record):
        # Establece el récord del jugador
        self.record = record

    def Crear_Cuenta(self, nombre, contraseña):
        # Método para crear una nueva cuenta de jugador
        miConexion = ConexionUsuario()
        miConexion.crearConexion()
        con = miConexion.getConexion()
        cursor = con.cursor()
        try:
            record = 0  # Inicializa el récord a 0
            self.Pregunta()
            respuesta = messagebox.askquestion("Confirmación", f"¿Está seguro que desea crear la cuenta {nombre}?")
            if respuesta == "yes":
                cursor.execute("SELECT nombre FROM jugador WHERE nombre = ?", (nombre,))
                listaJugadores = cursor.fetchall()
                if listaJugadores:
                    # Informa si el nombre de usuario ya está registrado
                    messagebox.showinfo("Éxito", f"El nombre de usuario {nombre} ya se encuentra registrado")
                else:
                    # Inserta el nuevo jugador en la base de datos
                    cursor.execute("INSERT INTO jugador(nombre, contraseña) VALUES (?, ?)", (nombre, contraseña))
                    con.commit()
                    # Inserta el récord inicial del nuevo jugador en la base de datos
                    cursor.execute("INSERT INTO record(jugador, record) VALUES (?, ?)", (nombre, record))
                    con.commit()
                    self.setRecord(0)  # Inicializa el récord a 0
                    messagebox.showinfo("Éxito", f"El nuevo jugador {nombre} se registró correctamente")
                    # Inicia el juego en un nuevo hilo
                    pygame_thread = threading.Thread(target=self.iniciar_pygame)
                    pygame_thread.daemon = True
                    pygame_thread.start()
            else:
                # Informa de la cancelación del registro
                messagebox.showinfo("Cancelación", "Registro cancelado")
        except Exception as e:
            # Manejo de errores y rollback en caso de excepción
            con.rollback()
            messagebox.showerror("Error", f"Error al crear el cliente: {str(e)}")
        miConexion.cerrarConexion()

    def Loggin(self, nombre, contraseña):
        # Método para iniciar sesión de un jugador existente
        miConexion = ConexionUsuario()
        miConexion.crearConexion()
        con = miConexion.getConexion()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT nombre, contraseña FROM jugador WHERE nombre = ? AND contraseña = ?", (nombre, contraseña))
            listaJugadores = cursor.fetchall()
            if listaJugadores:
                # Si el jugador existe, establece el nombre y el récord del jugador
                jugador1 = listaJugadores[0]
                self.setNombre(jugador1[0])
                cursor.execute("SELECT record FROM record WHERE jugador = ?", (nombre,))
                record = cursor.fetchone()
                if record:
                    self.setRecord(record[0])  # Inicializa el récord con el récord actual de la base de datos
                messagebox.showinfo("Mensaje", f"Bienvenido Jugador {nombre}")
                # Inicia el juego en un nuevo hilo
                pygame_thread = threading.Thread(target=self.iniciar_pygame)
                pygame_thread.daemon = True
                pygame_thread.start()
            else:
                # Informa si el jugador no está registrado
                messagebox.showinfo("Mensaje", f"El jugador {nombre} no se encuentra registrado")
        except Exception as e:
            # Manejo de errores y rollback en caso de excepción
            con.rollback()
            messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")
        miConexion.cerrarConexion()


    def ActualizarRecord(self, nombre, nuevo_record):
        # Método para actualizar el récord de un jugador en la base de datos
        miConexion = ConexionUsuario()
        miConexion.crearConexion()
        con = miConexion.getConexion()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT record FROM record WHERE jugador = ?", (nombre,))
            record_actual = cursor.fetchone()
            if record_actual:
                record_actual = record_actual[0]
                if nuevo_record > record_actual:  # Solo actualizar si el nuevo récord acumulado es mayor
                    cursor.execute("UPDATE record SET record = ? WHERE jugador = ?", (nuevo_record, nombre))
                    con.commit()
                    self.setRecord(nuevo_record)  # Actualizar el récord en el objeto Juego
        except Exception as e:
            # Manejo de errores y rollback en caso de excepción
            con.rollback()
            messagebox.showerror("Error", f"Error al actualizar el récord: {str(e)}")
        miConexion.cerrarConexion()

    def iniciar_pygame(self):
        # Método para iniciar el juego de Ahorcado utilizando Pygame
        pygame.init()
        ahorcado = Ahorcado(self)
        ahorcado.start_game()

    def Pregunta(self):
        
        # Reproduce un sonido de pregunta para confirmar una acción con el usuario.
        
        def music_thread_function():
            pygame.mixer.init()
            pygame.mixer.music.load(r'sound\pregunta.mp3')
            pygame.mixer.music.play()

        # Inicia el hilo para reproducir el sonido de pregunta
        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

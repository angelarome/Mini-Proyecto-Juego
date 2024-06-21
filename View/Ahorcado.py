import pygame
import random
import sys
from tkinter import messagebox
import threading

class Ahorcado():
    def reset_game(self):
        # Reinicia el juego, reseteando errores, letras adivinadas y eligiendo una nueva palabra
        self.mistakes = 0
        self.guessed_letters = set()
        self.word = random.choice(self.words)
        self.game_over = False
        self.victory = False

    def draw_hangman(self):
        # Dibuja el ahorcado basado en el número de errores
        if self.mistakes >= 1:  # Cabeza
            pygame.draw.circle(self.screen, self.BLACK, (400, 200), 40)
        if self.mistakes >= 2:  # Cuerpo
            pygame.draw.line(self.screen, self.BLACK, (400, 240), (400, 400), 5)
        if self.mistakes >= 3:  # Brazo izquierdo
            pygame.draw.line(self.screen, self.BLACK, (400, 280), (300, 200), 5)
        if self.mistakes >= 4:  # Brazo derecho
            pygame.draw.line(self.screen, self.BLACK, (400, 280), (500, 200), 5)
        if self.mistakes >= 5:  # Pierna izquierda
            pygame.draw.line(self.screen, self.BLACK, (400, 400), (300, 500), 5)
        if self.mistakes >= 6:  # Pierna derecha
            pygame.draw.line(self.screen, self.BLACK, (400, 400), (500, 500), 5)

    def draw_word(self):
        # Dibuja la palabra con las letras adivinadas y guiones bajos para las letras no adivinadas
        font = pygame.font.Font(None, self.FONT_SIZE)
        display_word = ''
        for letter in self.word:
            if letter in self.guessed_letters:
                display_word += letter
            else:
                display_word += '_ '
        text = font.render(display_word, True, self.BLACK)
        self.screen.blit(text, (300, 500))

    def draw_alphabet(self):
        # Dibuja el alfabeto con las letras no adivinadas
        font = pygame.font.Font(None, self.FONT_SIZE)
        x, y = 50, 50
        for letter in self.ALPHABET:
            if letter not in self.guessed_letters:
                text = font.render(letter, True, self.BLACK)
                self.screen.blit(text, (x, y))
            x += 40
            if x >= 750:
                x = 50
                y += 50  # Mueve a la siguiente línea después de cada fila completa

    def draw_score(self):
        # Dibuja el puntaje actual en la pantalla
        font = pygame.font.Font(None, self.FONT_SIZE)
        score_text = font.render(f"Record: {self.record}", True, self.BLACK)
        self.screen.blit(score_text, (650, 20))

    def draw_restart_button(self):
        # Dibuja el botón para reiniciar el juego
        font = pygame.font.Font(None, 36)
        button_text = font.render("Volver a Jugar", True, self.BLACK)
        button_rect = button_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 100))
        pygame.draw.rect(self.screen, self.RED, button_rect)
        self.screen.blit(button_text, button_rect)

    def display_message(self, message, color):
        # Muestra un mensaje en la pantalla
        font = pygame.font.Font(None, 50)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def handle_mouse_click(self, pos):
        # Maneja el clic del ratón para adivinar una letra
        mouseX, mouseY = pos
        x, y = 50, 50
        for letter in self.ALPHABET:
            if x <= mouseX <= x + 40 and y <= mouseY <= y + 40:
                if letter not in self.guessed_letters:
                    self.guessed_letters.add(letter)
                    if letter in self.word:
                        self.record += 10
                        self.Correcto()
                    else:
                        self.mistakes += 1
                        self.Error()
                break
            x += 40
            if x >= 750:
                x = 50
                y += 50

    def handle_restart_click(self, pos):
        # Maneja el clic del ratón para reiniciar el juego
        mouseX, mouseY = pos
        font = pygame.font.Font(None, 36)
        button_text = font.render("Volver a Jugar", True, self.RED)
        button_rect = button_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 100))
        if button_rect.collidepoint(mouseX, mouseY):
            self.reset_game()

    def run_game(self):
        # Ejecuta el bucle principal del juego
        self.Inicio()
        clock = pygame.time.Clock()
        running = True
        background_image = pygame.image.load(r'iconos\WhatsApp Image 2024-06-20 at 23.11.57.jpeg').convert()

        while running:
            # Ajusta el tamaño de la imagen de fondo según el tamaño de la ventana
            screen_width, screen_height = pygame.display.get_surface().get_size()
            background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
            self.screen.blit(background_image, (0, 0))

            # Dibuja los diferentes elementos del juego en la pantalla
            self.draw_hangman()
            self.draw_word()
            self.draw_alphabet()
            self.draw_score()
            self.Boton_Ayuda()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Maneja el clic del ratón para reiniciar el juego o adivinar una letra
                    if self.mistakes >= 6 or all(letter in self.guessed_letters for letter in self.word):
                        self.handle_restart_click(pygame.mouse.get_pos())
                        if self.record > self.Juego.getRecord():
                            self.Juego.setRecord(self.record)
                            self.Juego.ActualizarRecord(self.Juego.getNombre(), self.record)
                    else:
                        self.handle_mouse_click(pygame.mouse.get_pos())
                        if self.record > self.Juego.getRecord():
                            self.Juego.setRecord(self.record)
                            self.Juego.ActualizarRecord(self.Juego.getNombre(), self.record)


            if self.mistakes >= 6:
                # Si el número de errores es mayor o igual a 6, el juego se considera perdido
                if not self.game_over:
                    self.Perder()  # Llama a la función de pérdida
                    self.game_over = True
                # Muestra un mensaje indicando la palabra correcta
                self.display_message(f"La palabra es {self.word}", self.RED)
                self.draw_restart_button()  # Dibuja el botón para reiniciar el juego

            elif all(letter in self.guessed_letters for letter in self.word):
                # Si todas las letras de la palabra han sido adivinadas, el juego se considera ganado
                if not self.victory:
                    self.Ganar()  # Llama a la función de victoria
                    self.victory = True
                # Muestra un mensaje de victoria
                self.display_message("¡Ganaste!", self.BLUE)
                self.draw_restart_button()  # Dibuja el botón para reiniciar el juego

            pygame.display.flip()  # Actualiza la pantalla
            clock.tick(60)  # Controla la velocidad del bucle del juego

        pygame.quit()  # Cierra Pygame
        sys.exit()  # Sale del programa

    def mostrarAyudaRecord(self, event=None):
        # Muestra un cuadro de diálogo de ayuda
        self.Ayuda()
        messagebox.showinfo("Ayuda", "Da click a una letra hasta adivinar la palabra, tienes 6 oportunidades")

    def Ayuda(self):
        # Reproduce un sonido de ayuda en un hilo separado
        def music_thread_function():
            ayuda_sound = pygame.mixer.Sound(r'sound\ayuda.mp3')
            ayuda_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Boton_Ayuda(self):
        # Dibuja el botón de ayuda en la pantalla y maneja su clic
        button_image = pygame.image.load(r'iconos\pregunta_preview_rev_1.png')
        button_image = pygame.transform.scale(button_image, (50, 50))
        button_rect = button_image.get_rect(topleft=(8, 8))
        self.screen.blit(button_image, button_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                self.mostrarAyudaRecord()

    def Perder(self):
        # Reproduce un sonido de pérdida en un hilo separado
        def music_thread_function():
            perder_sound = pygame.mixer.Sound(r'sound\mario-kart-lose-1.mp3')
            perder_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Ganar(self):
        # Reproduce un sonido de victoria en un hilo separado
        def music_thread_function():
            ganar_sound = pygame.mixer.Sound(r'sound\bites-ta-da-winner.mp3')
            ganar_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Error(self):
        # Reproduce un sonido de error en un hilo separado
        def music_thread_function():
            error_sound = pygame.mixer.Sound(r'sound\perder-incorrecto-no-valido.mp3')
            error_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Correcto(self):
        # Reproduce un sonido de acierto en un hilo separado
        def music_thread_function():
            correct_sound = pygame.mixer.Sound(r'sound\correct-ding.mp3')
            correct_sound.play()

        music_thread = threading.Thread(target=music_thread_function)
        music_thread.start()

    def Inicio(self):
        # Reproduce la música de fondo en un hilo separado
        def music_thread_function():
            pygame.mixer.music.load(r'sound\gravity-falls-theme.mp3')
            pygame.mixer.music.play(-1)

        self.music_thread = threading.Thread(target=music_thread_function)
        self.music_thread.start()

    def start_game(self):
        # Inicia el bucle principal del juego
        self.run_game()

    def __init__(self, Juego):
        # Inicializa el juego y sus configuraciones
        pygame.init()
        pygame.mixer.init()

        self.Juego = Juego
        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.FONT_SIZE = 40
        self.ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.game_over = False
        self.victory = False

        # Lee las palabras desde un archivo de texto
        with open(r'View\words.txt', 'r') as file:
            self.words = [line.strip().upper() for line in file]

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Ahorcado")
        self.record = 0
        self.reset_game()  # Resetea el juego al inicio
        self.music_thread = None

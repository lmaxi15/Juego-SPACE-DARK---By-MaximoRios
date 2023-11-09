import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageFont, ImageDraw, ImageTk
from moviepy.editor import VideoFileClip
import numpy
import pygame
import sys
import random
import datetime


class menu_main:
    def __init__(self, root):
        self.root = root
        self.root.title('SpaceDark - By Lmaxi')
        self.root.geometry('500x300')
        self.create_menu()
        self.game_state = 'menu'  

    #====================MENU PRINCIPAL====================#
    def create_menu(self):
        menu_frame = tk.Frame(self.root, bg='black')
        menu_frame.pack(pady=0, fill='both', expand=True)
        
        text_font_path = "fonts\HFHourglass.ttf"
        text_custom_font = ImageFont.truetype(text_font_path, 43)
        self.image = Image.new("RGBA", (500, 45), (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.image)
        def update_text_color(menu_text):
            nonlocal text_color
            text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
            draw.rectangle((0, 0, 500, 45), fill=(0, 0, 0, 0))
            draw.text((10, 10), 'SpaceDark - By Lmaxi', font=text_custom_font, fill=text_color)
            image_tk = ImageTk.PhotoImage(self.image)
            menu_text.configure(image=image_tk)
            menu_text.image = image_tk
            root.after(1000, update_text_color, menu_text)
        text_color = (255, 255, 255, 255)
        menu_text = tk.Label(menu_frame, image=None, bg='black')
        menu_text.pack(side='top', anchor='center', fill='both')
        update_text_color(menu_text)
        
        login_button = self.create_custom_button(menu_frame, text='Login', command=self.login_window, button_width=150, button_height=40)
        login_button.pack(pady=30)
        login_button.bind("<Enter>", lambda event, button=login_button: self.change_color(event, button, 'green'))
        login_button.bind("<Leave>", lambda event, button=login_button: self.reset_color(event, button, 'white'))
        register_button = self.create_custom_button(menu_frame, text='Register', command=self.register_window, button_width=150, button_height=40)
        register_button.pack(pady=15)
        register_button.bind("<Enter>", lambda event, button=register_button: self.change_color(event, button, 'green'))
        register_button.bind("<Leave>", lambda event, button=register_button: self.reset_color(event, button, 'white'))
    #====================MENU PRINCIPAL====================#

    #====================TEXTO BOTON====================#
    def change_color(self, event, button, new_color):
        button.config(bg=new_color)
    def reset_color(self, event, button, original_color):
        button.config(bg=original_color)
    def create_custom_button(self, parent, text, command, button_width, button_height):
        custom_button_image = self.create_custom_button_text(text, button_width, button_height)
        custom_button = tk.Button(parent, image=custom_button_image, command=command, width=button_width, height=button_height, bg='white')
        custom_button.image = custom_button_image
        return custom_button
    def create_custom_button_text(self, text, width, height):
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font_path = "fonts\KarmaticArcade.ttf"
        font = ImageFont.truetype(font_path, 20)
        text_width, text_height = draw.textsize(text, font)
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)
        return ImageTk.PhotoImage(img)
    #====================TEXTO BOTON====================#

    def update_partidas(self, cod_jugador):
        try:
            with open('acumulador_partidas.txt', 'r') as file:
                lines = file.readlines()
                updated_lines = []
                existe = False
                for line in lines:
                    parts = line.strip().split(',')
                    if parts[0] == cod_jugador:
                        existe = True
                        parts[1] = str(int(parts[1]) + 1)
                    updated_lines.append(','.join(parts))
                if not existe:
                    updated_lines.append(f"{cod_jugador},1")
            with open('acumulador_partidas.txt', 'w') as file:
                file.write('\n'.join(updated_lines))
        except FileNotFoundError:
            # Si el archivo no existe, lo creamos y agregamos el jugador con 1 partida
            with open('acumulador_partidas.txt', 'w') as file:
                file.write(f"{cod_jugador},1")
        
    #====================MENU LOGIN====================#
    def login_window(self):
        login_window = tk.Toplevel(self.root)
        login_window.title('Login')
        login_window.geometry('500x200')
        login_window.configure(bg='black')
        
        font_path = "fonts\Computerfont.ttf"
        custom_font = ImageFont.truetype(font_path, 20)
        width, height = 100, 30
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        text_content1 = 'Usuario:'
        draw.text((18, 10), text_content1, font=custom_font, fill=(255, 255, 255, 255))
        image_tk = ImageTk.PhotoImage(image)
        text_label = tk.Label(login_window, image=image_tk, bg='black')
        text_label.image = image_tk
        text_label.pack()
        usuario_entry = tk.Entry(login_window)
        usuario_entry.pack(pady=5)

        text_content2 = 'Clave:'
        image2 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw2 = ImageDraw.Draw(image2)
        draw2.text((25, 10), text_content2, font=custom_font, fill=(255, 255, 255, 255))
        image2_tk = ImageTk.PhotoImage(image2)
        text_label2 = tk.Label(login_window, image=image2_tk, bg='black')
        text_label2.image = image2_tk
        text_label2.pack()
        clave_entry = tk.Entry(login_window, show='*')
        clave_entry.pack(pady=5)

        login_button = self.create_custom_button(login_window, text='Login', command=lambda: self.check_credentials(usuario_entry.get(), clave_entry.get(), login_window), button_width=120, button_height=30)
        login_button.pack(pady=10)
        login_button.bind("<Enter>", lambda event, button=login_button: self.change_color(event, button, 'green'))
        login_button.bind("<Leave>", lambda event, button=login_button: self.reset_color(event, button, 'white'))
    #====================MENU LOGIN====================#

    def check_credentials(self, usuario, clave, login_window):
        if not usuario or not clave:
            messagebox.showerror('Error', 'Por favor, ingrese el usuario y la clave.')
            return
        with open('maestro_usuarios.txt', 'r') as file:
            for line in file:
                stored_cod, stored_NyA, stored_usuario, stored_clave, _ = line.strip().split(',')
                if usuario == stored_usuario and clave == stored_clave:
                    messagebox.showinfo('Inicio de Sesión', 'Inicio de Sesión Exitoso')
                    self.update_partidas(stored_cod)
                    login_window.destroy()

                    with open('acumulador_partidas.txt', 'r') as archivo_acumulador:
                        for linea in archivo_acumulador:
                            datos = linea.strip().split(',')
                            cod_jugador = datos[0]
                            num_partida = datos[1]
                            if cod_jugador == stored_cod:
                                self.cod_jugador = cod_jugador  
                                self.num_partida = num_partida
                                break
                    self.start_game()
                    return
        messagebox.showerror('Error', 'Usuario o Clave incorrectos')

    #====================MENU REGISTER====================#
    def register_window(self):
        register_window = tk.Toplevel(self.root)
        register_window.title('Register')
        register_window.geometry('500x300')
        register_window.configure(bg='black')

        font_path = "fonts\Computerfont.ttf"
        custom_font = ImageFont.truetype(font_path, 20)
        width, height = 180, 30
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        text_content1 = 'Nombre Y Apellido:'
        draw.text((12, 10), text_content1, font=custom_font, fill=(255, 255, 255, 255))
        image_tk = ImageTk.PhotoImage(image)
        text_label = tk.Label(register_window, image=image_tk, bg='black')
        text_label.image = image_tk
        text_label.pack()
        NyA_entry = tk.Entry(register_window)
        NyA_entry.pack(pady=3)

        text_content2 = 'Usuario:'
        image2 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw2 = ImageDraw.Draw(image2)
        draw2.text((60, 10), text_content2, font=custom_font, fill=(255, 255, 255, 255))
        image2_tk = ImageTk.PhotoImage(image2)
        text_label2 = tk.Label(register_window, image=image2_tk, bg='black')
        text_label2.image = image2_tk
        text_label2.pack()
        usuario_entry = tk.Entry(register_window)
        usuario_entry.pack(pady=3)

        text_content3 = 'Clave:'
        image3 = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw3 = ImageDraw.Draw(image3)
        draw3.text((68, 10), text_content3, font=custom_font, fill=(255, 255, 255, 255))
        image3_tk = ImageTk.PhotoImage(image3)
        text_label3 = tk.Label(register_window, image=image3_tk, bg='black')
        text_label3.image = image3_tk
        text_label3.pack()
        clave_entry = tk.Entry(register_window, show='*')
        clave_entry.pack(pady=3)

        guardar_button = self.create_custom_button(register_window, text='Guardar', command=lambda: self.save_user(NyA_entry.get(), usuario_entry.get(), clave_entry.get(), register_window), button_width=160, button_height=30)
        guardar_button.pack(pady=15)
        guardar_button.bind("<Enter>", lambda event, button=guardar_button: self.change_color(event, button, 'green'))
        guardar_button.bind("<Leave>", lambda event, button=guardar_button: self.reset_color(event, button, 'white'))
        
        cancelar_button = self.create_custom_button(register_window, text='Cancelar', command=register_window.withdraw, button_width=160, button_height=30)
        cancelar_button.pack(pady=5)
        cancelar_button.bind("<Enter>", lambda event, button=cancelar_button: self.change_color(event, button, 'green'))
        cancelar_button.bind("<Leave>", lambda event, button=cancelar_button: self.reset_color(event, button, 'white'))
    #====================MENU REGISTER====================#

    def save_user(self, NyA, usuario, clave, register_window):
        if not NyA or not usuario or not clave:
            messagebox.showerror('Error', 'Por favor, complete todos los campos.')
            return
        try:
            with open('maestro_usuarios.txt', 'r') as f:
                lines = f.readlines()
                if lines:
                    last_line = lines[-1]
                    last_cod_user = int(last_line.split(',')[0])
                    cod_user = last_cod_user + 1
                else:
                    cod_user = 1
        except FileNotFoundError:
            cod_user = 1
        with open('maestro_usuarios.txt', 'a+') as file:
            file.write(f'{cod_user},{NyA},{usuario},{clave},\n')
        messagebox.showinfo('Registro Exitoso', 'Registro Exitoso')
        register_window.withdraw()


    def start_game(self):
        cod_jugador = self.cod_jugador
        num_partida = self.num_partida
        self.root.destroy()
        game = SpaceDarkGame(cod_jugador, num_partida)
        game.run()
        pygame.quit()



class SpaceDarkGame:
    def __init__(self, cod_jugador, num_partida):
        #==============================PANTALLA Y MENU==============================#
        pygame.init()
        self.paused = False
        self.cod_jugador = cod_jugador
        self.num_partida = num_partida
        # Pantalla
        self.width = 500
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SPACEDARK - BY MAX")
        # Cargar el GIF usando MoviePy
        self.gif = VideoFileClip("img/fondocongif3.gif")
        # Redimensionar el GIF (ajusta el tamaño según tus necesidades)
        self.gif = self.gif.resize((600, 830))
        # Obtener la duración del GIF en segundos
        self.duracion_gif = self.gif.duration
        # Crear un reloj para controlar la velocidad de reproducción
        self.clock = pygame.time.Clock()
        # Inicializar la posición de reproducción del GIF
        self.tiempo_actual = 0
        # Fuente
        self.font = pygame.font.Font('fonts\OriginTech.ttf', 50) 
        # Opciones de menú
        self.menu_options = ['Jugar', 'Opciones', 'Salir']
        # Estado del juego
        self.game_state = 'menu'
        #==============================PANTALLA Y MENU==============================#


    #==============================IMAGENES GENERALES==============================#
    # Escenarios
    stage1_bg = pygame.image.load('img\stage1.png')
    stage2_bg = pygame.image.load('img\stage2.png')
    stage3_bg = pygame.image.load('img\stage3.png')
    stage4_bg = pygame.image.load('img\stage4.png')
    stage5_bg = pygame.image.load('img\stage5.png')
    # Vida judador
    vida_100 = pygame.image.load('img/vida/vida_100.png')
    vida_80 = pygame.image.load('img/vida/vida_80.png')
    vida_60 = pygame.image.load('img/vida/vida_60.png')
    vida_40 = pygame.image.load('img/vida/vida_40.png')
    vida_20 = pygame.image.load('img/vida/vida_20.png')
    vida_5 = pygame.image.load('img/vida/vida_5.png')
    vida_0 = pygame.image.load('img/vida/vida_0.png')
    # Nave judador 1
    player_img_down = pygame.image.load("img/nave_1/gas_down.png")
    player_img_up = pygame.image.load("img/nave_1/gas_up.png")
    player_img_left = pygame.image.load("img/nave_1/gas_left.png") 
    player_img_right = pygame.image.load("img/nave_1/gas_right.png")
    bullet_img = pygame.image.load("img/nave_1/ettack.png")
    # Enemigo 1
    enemy1_img = pygame.image.load("img/enemy_1/nave.png")
    bullet1_enemy1 = pygame.image.load("img/enemy_1/ettack.png")
    # Enemigo 2
    enemy2_img = pygame.image.load("img/enemy_2/nave.png")
    bullet1_enemy2 = pygame.image.load("img/enemy_2/ettack_1.png")
    bullet2_enemy2 = pygame.image.load("img/enemy_2/ettack_2.png")
    #==============================IMAGENES GENERALES==============================#


    #===================================VARIABLES GENERALES===================================#
    # Jugador
    player_pos = [200, 520]
    # Inicializar imagen actual del jugador
    player_img_actual = player_img_down
    # Balas 
    bullets = [] # Lista para almacenar las balas del jugador
    # Tiempo mínimo entre disparos en ms
    last_shot = 0 # Tiempo del último disparo
    shot_cooldown = 500 # Tiempo de espera entre disparos

    # Vida
    player_life = 100 # Vida inicial 100%
    player_life_img = vida_100 # Imagen inicial con vida 100%

    # Lista de enemigos
    enemies = []
    enemy_bullets = {} # Diccionario para las balas
    # Temporizador y delay para disparos enemigos
    enemy_bullet_timer = 0 # Contador de tiempo 
    enemy_bullet_delay = 2 # Tiempo entre disparos enemigos / Ajusta este valor según la velocidad deseada
    points = 0
    stage = 1
    score_next_stage = 25
    show_stage_message = False
    #===================================VARIABLES GENERALES===================================#


    #===================================FUNCIONES JUGADOR===================================#
    #======BALAS JUGADOR======#
    def handle_bullets(self, bullets):
        for bullet in bullets:
            bullet[1] -= 8  # Mover bala hacia arriba
        bullets = [b for b in bullets if b[1] > -50] # Eliminar balas salidas
        for bullet in bullets:
            self.screen.blit(self.bullet_img, (bullet[0], bullet[1]))

    def handle_player(self, player_pos):
        self.screen.blit(self.player_img_actual, (player_pos[0], player_pos[1]))
    #======BALAS JUGADOR======#

    #======VIDA JUGADOR======#
    def update_player_life(self, new_life):
        self.player_life = new_life
        if self.player_life >= 100:
            self.player_life_img = self.vida_100
        elif self.player_life >= 80:
            self.player_life_img = self.vida_80
        elif self.player_life >= 60:
            self.player_life_img = self.vida_60
        elif self.player_life >= 40:
            self.player_life_img = self.vida_40
        elif self.player_life >= 20: 
            self.player_life_img = self.vida_20
        elif self.player_life >= 0:
            self.player_life_img = self.vida_5
        else:
            self.player_life_img = self.vida_0
    #===================================FUNCIONES JUGADOR===================================#


    #===================================FUNCIONES ENEMIGO===================================#
    #======ENEMIGO MOVIMIENTO======#
    def create_enemy(self):
        return {
            'id': random.randint(0, 9999), # genera un id aleatorio
            'pos': [random.randint(0, self.width - self.enemy1_img.get_width()), 100],
            'vel': random.choice([3, 5]),  # Velocidad aleatoria
            'dir': "right" if random.randint(0, 1) == 0 else "left",  # Dirección aleatoria
            'active': True,
            'last_shot': 0,
            'shot_cooldown': random.randint(2000, 3000)  # Cooldown de disparo aleatorio
        }

    def move_enemy(self, enemy):
        if enemy['dir'] == "right":
            enemy['pos'][0] += enemy['vel']
            if enemy['pos'][0] >= (self.width - self.enemy1_img.get_width()):
                enemy['dir'] = "left"
        elif enemy['dir'] == "left":
            enemy['pos'][0] -= enemy['vel']
            if enemy['pos'][0] <= 0:
                enemy['dir'] = "right"

    def enemy_shoot(self, enemy):
        # Inicializar lista de balas si no existe
        if enemy['id'] not in self.enemy_bullets:
            self.enemy_bullets[enemy['id']] = []
        now = pygame.time.get_ticks()
        if now - enemy['last_shot'] > enemy['shot_cooldown']:
            x = enemy['pos'][0] 
            y = enemy['pos'][1]
            # Agregar bala a lista de ese enemigo
            self.enemy_bullets[enemy['id']].append([x, y])  
            enemy['last_shot'] = now
    #======ENEMIGO MOVIMIENTO======#

    #======BALAS ENEMIGO======#
    def handle_enemy_bullets(self, enemy_bullets):
        # Recorrer cada bala en la lista de balas enemigo
        for b in enemy_bullets:  
            # Mover la bala hacia abajo sumando 3 a su posición y
            b[1] += 3
            # Filtrar la lista para remover las balas que salieron de la pantalla
            enemy_bullets = [b for b in enemy_bullets if b[1] < self.height] 
        # Recorrer nuevamente la lista filtrada
        for b in enemy_bullets:
            # Dibujar la bala enemiga en su posición actual 
            self.screen.blit(self.bullet1_enemy1, b)
        return enemy_bullets
    #======BALAS ENEMIGO======#
    #===================================FUNCIONES ENEMIGO===================================#


    #===================================DETALLE PARTIDA Y JUGADOR===================================#
    def guardar_detalle_partida(self, points, stage):
        cod_jugador = self.cod_jugador
        num_partida = self.num_partida
        fecha_actual = datetime.datetime.now().strftime("%Y/%m/%d")
        with open("detalle_partidaYjugador.txt", "a") as archivo_detalle:
            archivo_detalle.write(f"{cod_jugador},{num_partida},{points},{stage},{fecha_actual}\n")
    #===================================DETALLE PARTIDA Y JUGADOR===================================#

    #========================================DETALLE COLISIONES========================================#
    def guardar_detalle_colisiones(self, collision_x, collision_y):
        cod_jugador = self.cod_jugador
        num_partida = self.num_partida
        fecha_actual = datetime.datetime.now().strftime("%Y/%m/%d")
        with open("detalle_colisiones.txt", "a") as archivo_colisiones:
            archivo_colisiones.write(f"{cod_jugador},{num_partida},{fecha_actual},{collision_x},{collision_y}\n")
    #========================================DETALLE COLISIONES========================================#


    #==============================PROGRAMA PRINCIPAL==============================#
    def run(self):
        animacion_activada = True
        superficie = None
        playing_fps = 60
        menu_fps = 30
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = 'menu'
                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_p]:
                        self.paused = not self.paused

            if not self.paused:
                if self.game_state == 'menu':
                    pygame.time.Clock().tick(menu_fps)
                    
                    # Resetear variables 
                    self.player_life = 100
                    self.player_life_img = self.vida_100
                    self.bullets = []
                    self.enemies = []
                    self.enemy_bullets = {}
                    self.points = 0
                    self.stage = 1
                    self.score_next_stage = 25
                    self.show_stage_message = False
                    self.bullets_to_remove = []
                    # Rectángulos 
                    rect_1 = None
                    rect_2 = None
                    rect_3 = None
                    
                    if superficie is not None:
                        x = (self.width - superficie.get_width()) // 2
                        y = (self.height - superficie.get_height()) // 2
                        self.screen.blit(superficie, (x, y))

                    # Obtener mouse
                    mouse_pos = pygame.mouse.get_pos()

                    # Dibujar opciones
                    for i, option in enumerate(self.menu_options):
                        text = self.font.render(option, True, (255,255,255))
                        rect = text.get_rect(center=(self.width/2, (i+1)*175))
                        if i == 0:
                            rect_1 = rect
                        elif i == 1:
                            rect_2 = rect  
                        elif i == 2:
                            rect_3 = rect
                        # Dibujar opción
                        self.screen.blit(text, rect)

                    # Manejar eventos  
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            if rect_1.collidepoint(mouse_pos):
                                self.game_state = 'playing'
                            elif rect_2.collidepoint(mouse_pos):
                                self.game_state = 'options'
                            elif rect_3.collidepoint(mouse_pos):
                                pygame.quit()
                                sys.exit()

                elif self.game_state == 'playing':
                    pygame.time.Clock().tick(playing_fps)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.game_state = 'menu'
                    keys = pygame.key.get_pressed()
                    animacion_activada = False

                    if keys[pygame.K_SPACE]:
                        now = pygame.time.get_ticks()
                        if now - self.last_shot > self.shot_cooldown:
                            self.last_shot = now
                            x = self.player_pos[0] + 1
                            y = self.player_pos[1] - 1
                            self.bullets.append([x, y])

                    if keys[pygame.K_LEFT]:
                        self.player_img_actual = self.player_img_left
                        if self.player_pos[0] > (65 - self.player_img_actual.get_width()):
                            self.player_pos[0] -= 5

                    if keys[pygame.K_RIGHT]:
                        self.player_img_actual = self.player_img_right
                        if self.player_pos[0] < (495 - self.player_img_actual.get_width()):
                            self.player_pos[0] += 5

                    if keys[pygame.K_UP]:
                        self.player_img_actual = self.player_img_up 
                        if self.player_pos[1] > (280 - self.player_img_actual.get_height()):
                            self.player_pos[1] -= 5

                    if keys[pygame.K_DOWN]:
                        self.player_img_actual = self.player_img_down
                        if self.player_pos[1] < (695 - self.player_img_actual.get_height()):
                            self.player_pos[1] += 5

                    # Crear nuevos enemigos si no hay enemigos activos
                    if not any(enemy['active'] for enemy in self.enemies):
                        num_enemies_to_create = random.randint(3, 4)
                        for cant in range(num_enemies_to_create):
                            self.enemies.append(self.create_enemy())

                    # Lógica de colisiones jugador-bala enemiga
                    for bullet in self.bullets[:]:
                        bullet_rect = self.bullet_img.get_rect(topleft=(bullet[0], bullet[1]))
                        for enemy in self.enemies[:]:
                            enemy_rect = self.enemy1_img.get_rect(topleft=enemy['pos'])
                            if enemy['active'] and bullet_rect.colliderect(enemy_rect):
                                enemy['active'] = False
                                self.points += 1
                                self.guardar_detalle_colisiones(bullet[0], bullet[1])
                                if enemy['id'] in self.enemy_bullets:
                                    del self.enemy_bullets[enemy['id']]
                                # Agregar ambas balas a la lista de balas para eliminar
                                self.bullets_to_remove.append(bullet)
                    # Eliminar las balas del jugador y enemigas de la lista de balas
                    for bullet in self.bullets_to_remove:
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

                    # Lógica de colisiones balas enemigas-jugador
                    for id in self.enemy_bullets:
                        for bullet in self.enemy_bullets[id]:
                            bullet_rect = self.bullet1_enemy1.get_rect(topleft=bullet)
                            player_rect = self.player_img_actual.get_rect(topleft=self.player_pos)
                            if bullet_rect.colliderect(player_rect):
                                self.player_life -= 20
                                self.update_player_life(self.player_life)
                                self.enemy_bullets[id].remove(bullet)
                                break

                    # Pantalla de Game Over
                    if self.player_life == -20:
                        self.guardar_detalle_partida(self.points, self.stage)
                        font_go = pygame.font.SysFont('fonts\FakeHope.ttf', 60)
                        text_go = font_go.render("YOU LOST THE GAME", True, (255,0,0))
                        text_rect = text_go.get_rect(center=(self.width/2, self.height/2))
                        self.screen.blit(text_go, text_rect)
                        pygame.display.update()
                        pygame.time.wait(3000)
                        animacion_activada = True
                        if superficie is not None:
                            self.screen.blit(superficie, (x, y))
                        self.game_state = 'menu'

                    # Actualizar pantalla  
                    self.screen.fill((0,0,0)) # Fondo negro

                    if self.stage == 1:
                        self.screen.blit(self.stage1_bg, (0, 0))
                    elif self.stage == 2:
                        self.screen.blit(self.stage2_bg, (0, 0))
                    elif self.stage == 3:
                        self.screen.blit(self.stage3_bg, (0, 0))
                    elif self.stage == 4:
                        self.screen.blit(self.stage4_bg, (0, 0))
                    elif self.stage == 5:
                        self.screen.blit(self.stage5_bg, (0, 0))

                    # Jugador - Balas
                    self.handle_player(self.player_pos)
                    self.handle_bullets(self.bullets)
                    self.screen.blit(self.player_life_img, (10,650))

                    # Enemigo - Balas
                    for enemy in self.enemies[:]:
                        self.move_enemy(enemy)
                        if enemy['active']:
                            self.screen.blit(self.enemy1_img, enemy['pos'])
                            self.enemy_shoot(enemy)
                            # Controla el temporizador de balas enemigas
                            self.enemy_bullet_timer += 1
                            if self.enemy_bullet_timer >= self.enemy_bullet_delay:
                                for id in self.enemy_bullets: 
                                    self.enemy_bullets[id] = self.handle_enemy_bullets(self.enemy_bullets[id])
                                self.enemy_bullet_timer = 0

                    # Después de la línea que actualiza los puntos
                    if self.points >= self.score_next_stage:
                        self.stage += 1
                        self.score_next_stage += 25
                        self.show_stage_message = True
                        self.stage_message_timer = pygame.time.get_ticks()

                    if self.show_stage_message:
                        current_time = pygame.time.get_ticks()
                        if current_time - self.stage_message_timer < 3500:  # 2 segundos en milisegundos
                            font_stage_message = pygame.font.Font('fonts\FakeHope.ttf', 30)
                            stage_message = f"¡¡FELICIDADES HAS PASADO AL STAGE {self.stage} !!"
                            text_stage_message = font_stage_message.render(stage_message, True, (0, 255, 0))
                            text_rect = text_stage_message.get_rect(center=(self.width/2, self.height/2))
                            self.screen.blit(text_stage_message, text_rect)
                        else:
                            self.show_stage_message = False

                    # Dibujar el texto "Stage X/Y"
                    font_stage = pygame.font.Font('fonts\FakeHope.ttf', 20)
                    text_stage = font_stage.render(f"Stage: {self.stage} / 5", True, (255, 255, 255))
                    self.screen.blit(text_stage, (self.width - text_stage.get_width() - 10, 10))

                    # Dibujar puntos
                    font_points = pygame.font.Font('fonts\FakeHope.ttf', 20)
                    text_points = font_points.render("Puntos: " + str(self.points), True, (255, 0, 0))
                    self.screen.blit(text_points, (10, 10))
                    pygame.display.update()
                elif self.game_state == 'options':
                    print('OPCIONES DE LOS INFORMES:')
                    print('1) PADRON USUARIOS DEL JUEGO.')
                    print('2) PLANILLA PUNTAJES DE JUGADORES.')
                    print('3) COSULTA POR USUARIO Y POR NUMERO DE PARTIDA.')
                    print('4) CONSULTA DE RANKING POR USUARIO.')
                    print('5) RESOLUCION DE MATRICES - DOS DIMENCIONES')
                    print('6) INFORME DE INTERVENCION DE LOS OBJETOS')
                    print('7) RESOLUCION DE MATRICES - TRES DIMENCIONES')
                    opcion = int(input("Elija una opcion: "))

                    if opcion == 1:
                        print("\nPADRON USUARIOS DEL JUEGO:")
                        total_usuarios = 0
                        usuarios = []
                        with open('maestro_usuarios.txt', 'r') as archivo_usuarios:
                            print(f"Codigo Usuario |-| Nombre Y Apellido |-| Username |-| Clave |")
                            for linea in archivo_usuarios:
                                items = linea.strip().split(',')
                                usuario = {'cod_usuario': items[0], 'nya': items[1], 'username': items[2], 'clave': items[3]}  
                                usuarios.append(usuario)
                                print(f"{usuario['cod_usuario'].ljust(14)} |-| {usuario['nya'].ljust(17)} |-| {usuario['username'].ljust(8)} |-| {usuario['clave'].ljust(5)} |")
                                total_usuarios += 1
                        print(f"\nTotal de usuarios: {total_usuarios}")
                        input("")
                    elif opcion == 2:
                        print("\nPLANILLA PUNTAJES DE JUGADORES:")
                        usuarios = []
                        with open('maestro_usuarios.txt', 'r') as archivo_usuarios:
                            for linea in archivo_usuarios:
                                items = linea.strip().split(',')
                                usuario = {'cod_usuario': items[0], 'nya': items[1]}  
                                usuarios.append(usuario)
                        partidas = []  
                        with open('detalle_partidaYjugador.txt', 'r') as archivo_partidas:
                            for linea in archivo_partidas:
                                items = linea.strip().split(',')
                                partida = {'cod_usuario': items[0], 'numpartida': items[1], 'puntaje': items[2]}
                                partidas.append(partida)
                        max_puntaje = 0
                        nya_max_punt = ''
                        print(f"Codigo Usuario |-| Nombre Y Apellido |-| Tol Punt A(num part) |-| Tol Punt B(punt) |")
                        for p in partidas:
                            for u in usuarios:
                                if p['cod_usuario'] == u['cod_usuario']:
                                    print(f"{u['cod_usuario'].ljust(14)} |-| {u['nya'].ljust(17)} |-| {p['numpartida'].ljust(20)} |-| {p['puntaje'].ljust(16)} |")
                                    if int(p['puntaje']) > max_puntaje:
                                        max_puntaje = int(p['puntaje'])
                                        nya_max_punt = u['nya']
                        Tol_Punt_B = 0
                        for p in partidas:
                            puntos = int(p['puntaje'])
                            Tol_Punt_B += puntos
                        Tol_Punt_A = len(partidas)
                        print(f"\nTotal Puntos A: {Tol_Punt_A:<9} |-| Total Puntos B: {Tol_Punt_B} |")
                        print(f"El Mejor Usuario: {nya_max_punt} |-| Puntaje Más Alto: {max_puntaje} |")
                        input("")
                    elif opcion == 3:
                        print("\nCOSULTA POR USUARIO Y POR NUMERO DE PARTIDA:")
                        usuarios = []
                        with open('maestro_usuarios.txt', 'r') as archivo_usuarios:
                            for linea in archivo_usuarios:
                                items = linea.strip().split(',')
                                usuario = {'cod_usuario': items[0], 'nya': items[1]}  
                                usuarios.append(usuario)
                                print(f"Código: {usuario['cod_usuario']} |-| Nombre y apellido: {usuario['nya']}")
                        colisiones = []
                        with open('detalle_colisiones.txt', 'r') as archivo_colisiones:
                            for linea in archivo_colisiones:
                                items = linea.strip().split(',')
                                colision = {'cod_usuario': items[0], 'numpartida': items[1], 'fecha': items[2], 'X': items[3], 'Y': items[4]}  
                                colisiones.append(colision)
                        
                        codigo = input("Ingrese un codigo usuario: ")
                        partida = input("Ingrese el numero de partida: ")
                        for c in colisiones:
                            for u in usuarios:
                                if codigo == c['cod_usuario'] and partida == c['numpartida']:
                                    print(f"Nom Y Ape: {u['nya']}")
                                    print(f"Fecha: {c['fecha']}, Cordenadas: X, Y")

            else:
                # Si el juego está pausado, puedes mostrar un mensaje o una pantalla de pausa
                font_pause = pygame.font.Font('fonts\OriginTech.ttf', 65)
                text_pause = font_pause.render("PAUSE", True, (255, 255, 255))
                text_rect = text_pause.get_rect(center=(250, 100))
                self.screen.blit(text_pause, text_rect)
            pygame.display.flip()

            if animacion_activada:
                # Avanzar en el tiempo y actualizar la animación del GIF
                self.tiempo_actual += 1 / 30  # Asumiendo una velocidad de fotogramas de 30 por segundo
                if self.tiempo_actual > self.duracion_gif:
                    self.tiempo_actual = 0
                fotograma = self.gif.get_frame(self.tiempo_actual)
                superficie = pygame.surfarray.make_surface(numpy.transpose(fotograma, (1, 0, 2)))
    #==============================PROGRAMA PRINCIPAL==============================#

#===PRUEBAS RAPIDAS===#
if __name__ == "__main__":
    pygame.init()
    game = SpaceDarkGame("cod_jugador", "num_partida")
    game.run()
#===PRUEBAS RAPIDAS===#

#if __name__ == "__main__":
#    root = tk.Tk()
#    app = menu_main(root)
#    root.mainloop()
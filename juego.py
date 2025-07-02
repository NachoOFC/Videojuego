import pygame
from pygame.locals import *

pygame.init()
 # ----------- Declarar constantes -------------------------
ventana_x = 850
ventana_y = 480
ventana = pygame.display.set_mode((ventana_x,ventana_y))
pygame.display.set_caption("El Jarl")
reloj = pygame.time.Clock()
negro=(0,0,0)
fuente=pygame.font.SysFont("segoe print", 22)
lvl = 1
puntaje = 0


# -----------------------Vikingo------------------------------
class personaje(object):
	def __init__(self, x, y, fuente, limite):
		self.x = x
		self.y = y
		self.velocidad = 15
		
		#Atributos para salto
		self.ha_saltado = False
		self.impulso_salto = 10

		# Caracteristicas del vikingo
		self.va_izquierda = False
		self.va_derecha = False
		self.contador_pasos = 0
		self.camina_derecha = [pygame.image.load("img/vikingoderecha1.png")]	
		self.camina_izquierda = [pygame.image.load("img/vikingoizquierda1.png")]
		self.quieto = pygame.image.load("img/vikingo.png")
		self.ancho = self.quieto.get_width()
		self.alto = self.quieto.get_height()
		self.camino = [100, limite]

		# Salud
		self.salud = 100
		
		# Zona de impacto
		self.zona_impacto = (self.x + 15, self.y + 10, 30, 50)

	# Dibujar en pantalla 
	def dibujar(self, cuadro):
		# Vida del vikingo en pantalla (actualizada)
		texto=fuente.render(str(self.salud), True, negro)
		if self.contador_pasos + 1 > 0:
			self.contador_pasos = 0

		if self.va_izquierda:
			cuadro.blit(self.camina_izquierda[self.contador_pasos], (self.x,self.y))
			self.contador_pasos += 1
		elif self.va_derecha:
			cuadro.blit(self.camina_derecha[self.contador_pasos], (self.x,self.y))
			self.contador_pasos += 1
		else:
			cuadro.blit(self.quieto, (self.x,self.y))

		#Dibujar en pantalla la zona de impacto
		self.zona_impacto = (self.x + 8, self.y , 80, 100)		
		#pygame.draw.rect(cuadro, (255,0,0), self.zona_impacto, 2) 
		
		# Barra de vida del vikingo
		pygame.draw.rect(cuadro, (255,0,0), (30, 30, 100, 20))
		pygame.draw.rect(cuadro, (0,128,0), (30, 30 , self.salud, 20))

		# Mostrar la vida restante del vikingo
		ventana.blit(texto, (55, 19))
	
	# Movimiento del vikingo segun teclas
	def se_mueve_segun(self, k, iz, de, salta):
		# Movimiento a izquierda 
		if k[iz] and self.x > self.velocidad:
			self.x -= self.velocidad
			self.va_izquierda = True
			self.va_derecha = False
		# Moviminento a derecha
		elif k[de] and self.x < ventana_x - self.ancho - self.velocidad:
			self.x += self.velocidad
			self.va_derecha = True
			self.va_izquierda = False
		# Controles de animación en caso de dejar de moverse en horizonal
		else:			
			self.va_izquierda = False
			self.va_derecha = False
			self.contador_pasos = 0
		
		# Si se reconoce que se ha saltado con la tecla espacio
		if self.ha_saltado:
			if self.impulso_salto >= -10:
				if self.impulso_salto < 0:
					self.y -= (self.impulso_salto**2) * 0.5 * -1
				else:
					self.y -= (self.impulso_salto**2) * 0.5
				self.impulso_salto -= 1
			else:
				self.ha_saltado = False
				self.impulso_salto = 10
		else:
			if k[salta]:
				self.ha_saltado = True
				self.va_izquierda = False
				self.va_derecha = False
				self.contador_pasos = 0
			else:
				self.y +=10
				if self.y>325:
					self.y=325

	def se_mueve_solo(self, nivel):
		if self.velocidad > 0:
			if self.x + self.velocidad < self.camino[1]:
				self.x += self.velocidad * nivel
				self.va_derecha = True
				self.va_izquierda = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		else:
			if self.x - self.velocidad > self.camino[0]:
				self.x += self.velocidad * nivel 
				self.va_izquierda = True
				self.va_derecha = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0

	# Detección de colisiones 
	def se_encuentra_con(self, alguien):
		R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
		R1_ar = self.zona_impacto[1]
		R1_iz = self.zona_impacto[0]
		R1_de = self.zona_impacto[0] + self.zona_impacto[2]
		R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3]
		R2_ar = alguien.zona_impacto[1]
		R2_iz = alguien.zona_impacto[0]
		R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2]

		return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

	# Personaje recibe golpe de daño de parte de otro personaje
	def es_golpeado(self):
		self.ha_saltado = False
		self.impulso_salto = 10
		self.x = 5
		self.y = 355
		self.contador_pasos = 0
		# Velocidad resurreccion al ser impactado/dañado
		pygame.time.delay(10)


# ---------------------------- Robot -----------------------
class robot(object):
	def __init__(self, x, y, fuente, limite):
		# Caracteristicas del robot
		self.x = x
		self.y = y
		self.velocidad = 5
		self.daño = 15
		self.puntos = 10
		self.va_izquierda = False
		self.va_derecha = False
		self.contador_pasos = 0
		self.camina_derecha = [pygame.image.load("img/superrobotderecha.png")]
		self.camina_izquierda = [pygame.image.load("img/superrobot.png")]
		self.quieto = pygame.image.load("img/superrobot.png")
		self.ancho = self.quieto.get_width()
		self.alto = self.quieto.get_height()
		# Limites de movimiento
		self.camino = [100, limite]
		# Salud robot
		self.salud = 100
		# Zona de impacto
		self.zona_impacto = (self.x + 15, self.y + 10, 30, 50)
	
	# Dibujar en pantalla
	def dibujar(self, cuadro):
		if self.contador_pasos + 1 > 1:
			self.contador_pasos = 0

		if self.va_izquierda:
			cuadro.blit(self.camina_izquierda[self.contador_pasos], (self.x,self.y))
			self.contador_pasos += 1
		elif self.va_derecha:
			cuadro.blit(self.camina_derecha[self.contador_pasos], (self.x,self.y))
			self.contador_pasos += 1
		else:
			cuadro.blit(self.quieto, (self.x,self.y))		
		# Dibujar Zona de impacto
		self.zona_impacto = (self.x , self.y , 130, 80)
		#pygame.draw.rect(cuadro, (255,0,0), self.zona_impacto, 2)

		# Dibujar vida del robot
		pygame.draw.rect(cuadro, (255,0,0), (self.x + 15, self.y - 5, 100, 10))
		pygame.draw.rect(cuadro, (0,128,0), (self.x + 15, self.y - 5, self.salud, 10))
	
	# Movimiento automatico del robot
	def se_mueve_solo(self):
		if self.velocidad > 0:
			if self.x + self.velocidad < self.camino[1]:
				self.x += self.velocidad 
				self.va_derecha = True
				self.va_izquierda = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		else:
			if self.x - self.velocidad > self.camino[0]:
				self.x += self.velocidad 
				self.va_izquierda = True
				self.va_derecha = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		

	# Detección de colisiones
	def se_encuentra_con(self, alguien):
		R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
		R1_ar = self.zona_impacto[1]
		R1_iz = self.zona_impacto[0]
		R1_de = self.zona_impacto[0] + self.zona_impacto[2]
		R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3]
		R2_ar = alguien.zona_impacto[1]
		R2_iz = alguien.zona_impacto[0]
		R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2]

		return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

class robodog(object):
	def __init__(self, x, y, fuente, limite):
		# Caracteristicas del robot
		self.x = x
		self.y = y
		self.velocidad = 10 
		self.puntos = 10
		self.daño = 10
		self.va_izquierda = False
		self.va_derecha = False
		self.contador_pasos = 0
		self.camina_derecha = [pygame.image.load("img/robodog.png")]
		self.camina_izquierda = [pygame.image.load("img/robodogizquierda.png")]
		self.quieto = pygame.image.load("img/robodog.png")
		self.ancho = self.quieto.get_width()
		self.alto = self.quieto.get_height()
		# Limites de movimiento
		self.camino = [120, limite]
		# Salud robot
		self.salud = 100
		# Zona de impacto
		self.zona_impacto = (self.x + 15, self.y + 10, 30, 50)
	
	# Dibujar en pantalla
	def dibujar(self, cuadro):
		if self.contador_pasos + 1 > 0:
			self.contador_pasos = 0

		if self.va_izquierda:
			cuadro.blit(self.camina_izquierda[self.contador_pasos], (self.x,self.y))
			self.contador_pasos += 1
		elif self.va_derecha:
			cuadro.blit(self.camina_derecha[self.contador_pasos], (self.x,self.y))
			self.contador_pasos += 1
		else:
			cuadro.blit(self.quieto, (self.x,self.y))		
		# Dibujar Zona de impacto
		self.zona_impacto = (self.x , self.y , 130, 80)
		#pygame.draw.rect(cuadro, (255,0,0), self.zona_impacto, 2)

		# Dibujar vida del robot
		pygame.draw.rect(cuadro, (255,0,0), (self.x + 15, self.y - 5, 100, 10))
		pygame.draw.rect(cuadro, (0,128,0), (self.x + 15, self.y - 5, self.salud, 10))
	
	# Movimiento automatico del robot
	def se_mueve_solo(self):
		if self.velocidad > 0:
			if self.x + self.velocidad < self.camino[1]:
				self.x += self.velocidad 
				self.va_derecha = True
				self.va_izquierda = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		else:
			if self.x - self.velocidad > self.camino[0]:
				self.x += self.velocidad 
				self.va_izquierda = True
				self.va_derecha = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		

	# Detección de colisiones
	def se_encuentra_con(self, alguien):
		R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
		R1_ar = self.zona_impacto[1]
		R1_iz = self.zona_impacto[0]
		R1_de = self.zona_impacto[0] + self.zona_impacto[2]
		R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3]
		R2_ar = alguien.zona_impacto[1]
		R2_iz = alguien.zona_impacto[0]
		R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2]

		return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

# ---------------------------- Jefe final -----------------------
class jefe(object):
	def __init__(self, x, y, fuente, limite):   
		# Caracteristicas del robot
		self.x = x
		self.y = y
		self.velocidad = 5
		self.puntos = 100
		self.daño = 25
		self.va_izquierda = False
		self.va_derecha = False
		self.contador_pasos = 0
		self.camina_derecha = [pygame.image.load("img/jefe.png"), pygame.image.load("img/jefederecha.png"),pygame.image.load("img/jefe2.png"),pygame.image.load("img/jefe3.png")]
		self.camina_izquierda = [pygame.image.load("img/jefe.png"), pygame.image.load("img/jefederecha.png"),pygame.image.load("img/jefe2.png"),pygame.image.load("img/jefe2.png")]
		self.quieto = pygame.image.load("img/jefe.png")
		self.ancho = self.quieto.get_width()
		self.alto = self.quieto.get_height()
		# Limites de movimiento
		self.camino = [120, limite]
		# Salud robot
		self.salud = 350
		# Zona de impacto
		self.zona_impacto = (self.x + 15, self.y + 10, 30, 50)
	
	# Dibujar en pantalla
	def dibujar(self, cuadro):
		if self.contador_pasos + 1 > 16:
			self.contador_pasos = 0

		if self.va_izquierda:
			cuadro.blit(self.camina_izquierda[self.contador_pasos//4], (self.x,self.y))
			self.contador_pasos += 1
		elif self.va_derecha:
			cuadro.blit(self.camina_derecha[self.contador_pasos//4], (self.x,self.y))
			self.contador_pasos += 1
		else:
			cuadro.blit(self.quieto, (self.x,self.y))		
		# Dibujar Zona de impacto
		self.zona_impacto = (self.x , self.y , 130, 80)
		#pygame.draw.rect(cuadro, (255,0,0), self.zona_impacto, 2)

		# Dibujar vida del robot
		pygame.draw.rect(cuadro, (255,0,0), (self.x, self.y - 15, 175, 10))
		pygame.draw.rect(cuadro, (0,128,0), (self.x, self.y - 15, self.salud//2, 10))
	
	# Movimiento automatico del robot
	def se_mueve_solo(self):
		if self.velocidad > 0:
			if self.x + self.velocidad < self.camino[1]:
				self.x += self.velocidad 
				self.va_derecha = True
				self.va_izquierda = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		else:
			if self.x - self.velocidad > self.camino[0]:
				self.x += self.velocidad 
				self.va_izquierda = True
				self.va_derecha = False
			else:
				self.velocidad = self.velocidad * -1
				self.contador_pasos = 0
		

	# Detección de colisiones
	def se_encuentra_con(self, alguien):
		R1_ab = self.zona_impacto[1] + self.zona_impacto[3]
		R1_ar = self.zona_impacto[1]
		R1_iz = self.zona_impacto[0]
		R1_de = self.zona_impacto[0] + self.zona_impacto[2]
		R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3]
		R2_ar = alguien.zona_impacto[1]
		R2_iz = alguien.zona_impacto[0]
		R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2]

		return R1_de > R2_iz and R1_iz < R2_de and R1_ar < R2_ab and R1_ab > R2_ar

# --------------------- Disparo ---------------------------(Falta añadir el martillo)
class proyectil(object):
	# Caracteristicas del disparo
	def __init__(self, x,y,radio,color, direccion):
		self.x = x
		self.y = y
		self.radio = radio
		self.color = color
		self.direccion = direccion
		self.velocidad = 12 * direccion
		self.zona_impacto = (self.x-self.radio, self.y-self.radio, self.radio*2, self.radio*2)
		self.imagen = [pygame.image.load("img/disparo1.png"), pygame.image.load("img/disparo2.png")]

	# Dibujar en pantalla
	def dibujar(self, cuadro):
		# Dibujar zona de impacto del disparo
		self.zona_impacto = (self.x-self.radio, self.y-self.radio, self.radio*2, self.radio*2)

		if direccion>0:
			ventana.blit(self.imagen[0], (self.x, self.y))
		else:
			ventana.blit(self.imagen[1], (self.x, self.y))
		
		#pygame.draw.circle(cuadro, self.color, (self.x, self.y), self.radio)
		#pygame.draw.rect(cuadro, (255,0,0), self.zona_impacto, 2)

	# Si la bala impacta a un enemigo
	def impacta_a(self, alguien):
		if alguien.salud > 0:
			alguien.salud -= 25
		else:
			#alguien.es_visible = False
			del(alguien)


# ----------------  Función para repintar el cuadro de juego -----------------
def repintar_cuadro_juego():
	# Dibujar y mantener el fondo de pantalla
	if nivel <= nivel_maximo:
		ventana.blit(imagen_fondo[nivel],(0,0))
	else: 
		ventana.fill(negro)

	# Dibujar Héroe
	heroe.dibujar(ventana)

	# Dibujar Villano
	villanos[nivel].dibujar(ventana)

	# Dibujar Balas
	for bala in balas:
		bala.dibujar(ventana)

	#Crear textos
	puntos = texto_puntos.render('Puntaje: ' + str(puntaje), 1, (250,250,250))
	nivel_actual = texto_nivel.render('Nivel: ' + str(lvl), 1, (250,250,250))
	#Dibujar textos
	ventana.blit(puntos, (650, 30))
	ventana.blit(nivel_actual, (350, 30))
	# Se refresca la imagen
	pygame.display.update()
	
# Se encarga de subir nivel
def subir_nivel():
	global nivel
	global nivel_maximo
	global villano
	global musica_fondo
	global ventana
	global esta_jugando
	global lvl
	global gana

	nivel +=1
	
	texto = pygame.font.SysFont('comicsans', 100)
	marcador = texto.render('Subes de nivel!', 1, (255,0,0))

	if villanos[nivel] == villanos[2]:
		lvl+=1
		ventana.blit(marcador, (250 - (marcador.get_width()//3), 200))
	
	if villanos[nivel] == villanos[5]:
		lvl+=1
		ventana.blit(marcador, (250 - (marcador.get_width()//3), 200))
		
	pygame.display.update()
	pygame.time.delay(0)

	# Verifica el nivel y revisa si acaba el juego o no
	if nivel > nivel_maximo:
		pygame.mixer.music.stop()
		esta_jugando = False
		lvl=1
		gana=True
	# En casode pasar nivel intermedio se actualiza el enemigo y la musica 
	"""else:
		villano = villanos[nivel]
		pygame.mixer.music.stop()
		musica_fondo = pygame.mixer.music.load(ruta_musica[nivel])
		pygame.mixer.music.play(-1)"""

		
# Variable que controla la repeticion del juego completo con todas sus pantallas
repetir = True 

# ------------------------- Ciclo de repeticion de todo el juego ---------------------------
while repetir:
	# Inicializacion de elementos del juego
	nivel = 0
	nivel_maximo = 5
	imagen_fondo = [pygame.image.load('img/fondobasico.jpg'), pygame.image.load('img/fondobasico.jpg'), pygame.image.load('img/fondobasico.jpg'), pygame.image.load('img/fondobasico.jpg'), pygame.image.load('img/fondobasico.jpg'),pygame.image.load('img/fondobasico.jpg'),pygame.image.load('img/fondobasico.jpg')]
	ruta_musica = ["sounds/music.mp3", "sounds/music.mp3", "sounds/music.mp3", "sounds/music.mp3", "sounds/music.mp3", "sounds/music.mp3", "sounds/music.mp3"]
	musica_fondo = pygame.mixer.music.load(ruta_musica[nivel])
	pygame.mixer.music.play(-1)
	puntaje = 0
	texto_puntos = pygame.font.SysFont('comicsans', 30, True)
	texto_nivel = pygame.font.SysFont('comicsans', 30, True)
	texto_intro = pygame.font.SysFont('console', 30, True)
	texto_resultado = pygame.font.SysFont('console', 80, True)
	esta_en_intro = True
	gana = False
	personaje_intro = personaje(50,150,"heroe",700)

	# Dibujar vikingo
	heroe=personaje(int(30), int(325),"heroe", ventana_x)
	villanos = [robodog(int(600), int(385),"villano",int(720)),
				robodog(int(600), int(385),"villano",int(720)), 
				robot(int(300), int(345),"villano",int(720)),
				robodog(int(600), int(385),"villano",int(720)),
				robot(int(300), int(345),"villano",int(720)),
				jefe(int(700), int(330),"villano",int(720)),
				]
	
	
	# Variables Balas
	tanda_disparos = 0
	balas = []

	# Seccion de intro
	while esta_en_intro:
		# control de velocidad del juego
		reloj.tick(27)
		# evento de boton de cierre de ventana
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				quit()

		ventana.fill((0,0,0)) # pinta el fondo de negro
		titulo = texto_intro.render('EL JARL', 1, (255,0,0))
		personaje_intro.se_mueve_solo(1)
		instrucciones = texto_intro.render('Presione ENTER para continuar...', 1, (255,255,255))
		ventana.blit(titulo, ((ventana_x//2)-titulo.get_width()//2, 10))
		ventana.blit(instrucciones, ((ventana_x//2)-instrucciones.get_width()//2, 300))

		tecla = pygame.key.get_pressed()

		if tecla[pygame.K_RETURN]:
			esta_en_intro=False
			esta_jugando = True

		personaje_intro.dibujar(ventana)
		pygame.display.update()
	
	# Seccion de juego
	esta_jugando=True
	while esta_jugando:
		# Control de velocidad del juego
		reloj.tick(27)
		# Evento de boton de cierre de ventana
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				quit()
		

		# Teclas presionadas
		teclas=pygame.key.get_pressed()
		heroe.se_mueve_segun(teclas,pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE)

		# Mantener movimiento automatico del perro cyborg
		villanos[nivel].se_mueve_solo()

		# Verificar si colisiona el vikingo con perro cyborg

		if heroe.se_encuentra_con(villanos[nivel]):
			heroe.es_golpeado()
			puntaje -= 5
			heroe.salud -= villanos[nivel].daño
		
		# Manejo de los disparos
		if tanda_disparos > 0:
			tanda_disparos += 1
		if tanda_disparos > 2:
			tanda_disparos = 0

		# Contacto de disparo con el perro cyborg
		for bala in balas:
			if villanos[nivel].se_encuentra_con(bala):
				bala.impacta_a(villanos[nivel])
				balas.pop(balas.index(bala)) # se elimina la bala del impacto
			# Movimiento de la bala dentro de los limites de la ventana
			if bala.x < ventana_x and bala.x > 0:
				bala.x += bala.velocidad
			else:
				balas.pop(balas.index(bala)) 

		# Capturar evento del disparo
		if teclas[pygame.K_x] and tanda_disparos == 0:
			if heroe.va_izquierda:
				direccion = -1
			elif heroe.va_derecha:
				direccion = 1
			else:
				direccion = -1

			if len(balas) < 1: 
				balas.append(proyectil(round(heroe.x + heroe.ancho // 2), round(heroe.y + heroe.alto // 2), 6, (0,0,0), direccion))
			tanda_disparos = 1

		# Consulta para saber si se sube de nivel o no
		if villanos[nivel].salud <= 0:
			subir_nivel()
			puntaje += villanos[nivel].puntos
		# Consulta para ver si pierde
		if heroe.salud < 1:
			esta_jugando = False
			lvl = 1
		
		
		repintar_cuadro_juego()


	# Seccion de pantalla final
	final = True
	while final:
		# evento de boton de cierre de ventana
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
		ventana.fill((0,0,0)) # pinta el fondo de negro
		titulo = texto_intro.render('JUEGO TERMINADO', 1, (255,0,0))
		if gana:
			resultado = texto_resultado.render('HAS GANADO! B)', 1, (255,0,0))
		else:
			resultado = texto_resultado.render('HAS PERDIDO! :c', 1, (255,0,0))
		pts = texto_intro.render('Puntaje Total: '+str(puntaje), 1, (255,255,255))
		instrucciones = texto_intro.render('Presione ENTER para cerrar...', 1, (255,255,255))
		reintentar = texto_intro.render('Presione R para volver al juego...', 1, (255,255,255))
		ventana.blit(titulo, ((ventana_x//2)-titulo.get_width()//2, 10))
		ventana.blit(resultado, ((ventana_x//2)-resultado.get_width()//2, 200))
		ventana.blit(pts,((ventana_x//2)-titulo.get_width()//2, 100))
		ventana.blit(instrucciones, ((ventana_x//2)-instrucciones.get_width()//2, 300))
		ventana.blit(reintentar, ((ventana_x//2)-reintentar.get_width()//2, 350))
		pygame.display.update()

		tecla = pygame.key.get_pressed()

		if tecla[pygame.K_RETURN]:
			repetir=False
			final=False

		if tecla[pygame.K_r]:
			repetir=True
			final=False
			# se asegura de eliminar los objetos de cada personaje
			del(heroe)
			del(villanos)
# ---------------------- Termina el juego y finaliza los elementos de pygame -------------------------------
pygame.quit()  

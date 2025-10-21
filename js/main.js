// ===== COPY PASTE DE JUEGO.PY PERO EN JAVASCRIPT =====
// NO USAR FISICA DE PHASER, SOLO CANVAS HTML5

let gameCanvas;
let gameCtx;
let gameAssets = {};
let gameState = {
    nivel: 0,
    puntaje: 0,
    estaBenjugando: true,
    estaEnIntro: true,
    gana: false
};

const VENTANA_X = 850;
const VENTANA_Y = 480;
const GROUND_Y = 325;

// ===== CARGAR ASSETS =====
function loadAssets() {
    const imagenes = [
        'viking-idle', 'img/vikingo.png',
        'viking-right', 'img/vikingoderecha1.png',
        'viking-left', 'img/vikingoizquierda1.png',
        'robodog', 'img/robodog.png',
        'robodog-left', 'img/robodogizquierda.png',
        'robot', 'img/superrobot.png',
        'robot-right', 'img/superrobotderecha.png',
        'boss', 'img/jefe.png',
        'boss-right', 'img/jefederecha.png',
        'projectile-1', 'img/disparo1.png',
        'projectile-2', 'img/disparo2.png',
        'background', 'img/fondobasico.jpg'
    ];

    for (let i = 0; i < imagenes.length; i += 2) {
        const name = imagenes[i];
        const path = imagenes[i + 1];
        const img = new Image();
        img.src = path;
        gameAssets[name] = img;
    }
}

// ===== CLASES =====
class Personaje {
    constructor(x, y, limite) {
        this.x = x;
        this.y = y;
        this.velocidad = 15;
        this.ha_saltado = false;
        this.impulso_salto = 10;
        this.va_izquierda = false;
        this.va_derecha = false;
        this.contador_pasos = 0;
        this.ancho = 120;
        this.alto = 130;
        this.camino = [100, limite];
        this.salud = 100;
        this.zona_impacto = [this.x + 8, this.y, 80, 100];
    }
    
    se_mueve_segun(keys) {
        if (keys['ArrowLeft'] && this.x > this.velocidad) {
            this.x -= this.velocidad;
            this.va_izquierda = true;
            this.va_derecha = false;
        } else if (keys['ArrowRight'] && this.x < VENTANA_X - this.ancho - this.velocidad) {
            this.x += this.velocidad;
            this.va_derecha = true;
            this.va_izquierda = false;
        } else {
            this.va_izquierda = false;
            this.va_derecha = false;
            this.contador_pasos = 0;
        }
        
        if (this.ha_saltado) {
            if (this.impulso_salto >= -10) {
                if (this.impulso_salto < 0) {
                    this.y -= (this.impulso_salto ** 2) * 0.5 * -1;
                } else {
                    this.y -= (this.impulso_salto ** 2) * 0.5;
                }
                this.impulso_salto -= 1;
            } else {
                this.ha_saltado = false;
                this.impulso_salto = 10;
            }
        } else {
            if (keys[' ']) {
                this.ha_saltado = true;
                this.va_izquierda = false;
                this.va_derecha = false;
                this.contador_pasos = 0;
            } else {
                this.y += 10;
                if (this.y > 325) {
                    this.y = 325;
                }
            }
        }
        
        this.zona_impacto = [this.x + 8, this.y, 80, 100];
    }
    
    se_encuentra_con(alguien) {
        const R1_ab = this.zona_impacto[1] + this.zona_impacto[3];
        const R1_ar = this.zona_impacto[1];
        const R1_iz = this.zona_impacto[0];
        const R1_de = this.zona_impacto[0] + this.zona_impacto[2];
        const R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3];
        const R2_ar = alguien.zona_impacto[1];
        const R2_iz = alguien.zona_impacto[0];
        const R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2];
        
        return R1_de > R2_iz && R1_iz < R2_de && R1_ar < R2_ab && R1_ab > R2_ar;
    }
    
    es_golpeado() {
        this.ha_saltado = false;
        this.impulso_salto = 10;
        this.x = 5;
        this.y = 355;
        this.contador_pasos = 0;
    }
    
    dibujar(ctx) {
        let sprite = gameAssets['viking-idle'];
        if (this.va_izquierda) {
            sprite = gameAssets['viking-left'];
            this.contador_pasos += 1;
        } else if (this.va_derecha) {
            sprite = gameAssets['viking-right'];
            this.contador_pasos += 1;
        }
        
        if (sprite && sprite.width > 0) {
            ctx.drawImage(sprite, this.x, this.y, 120, 130);
        }
    }
}

class Robot {
    constructor(x, y, limite) {
        this.x = x;
        this.y = y;
        this.velocidad = 5;
        this.daño = 15;
        this.puntos = 10;
        this.va_izquierda = false;
        this.va_derecha = false;
        this.contador_pasos = 0;
        this.ancho = 91;
        this.alto = 109;
        this.camino = [100, limite];
        this.salud = 100;
        this.zona_impacto = [this.x, this.y, 130, 80];
    }
    
    se_mueve_solo() {
        if (this.velocidad > 0) {
            if (this.x + this.velocidad < this.camino[1]) {
                this.x += this.velocidad;
                this.va_derecha = true;
                this.va_izquierda = false;
            } else {
                this.velocidad = this.velocidad * -1;
                this.contador_pasos = 0;
            }
        } else {
            if (this.x - this.velocidad > this.camino[0]) {
                this.x += this.velocidad;
                this.va_izquierda = true;
                this.va_derecha = false;
            } else {
                this.velocidad = this.velocidad * -1;
                this.contador_pasos = 0;
            }
        }
        
        this.zona_impacto = [this.x, this.y, 130, 80];
    }
    
    se_encuentra_con(alguien) {
        const R1_ab = this.zona_impacto[1] + this.zona_impacto[3];
        const R1_ar = this.zona_impacto[1];
        const R1_iz = this.zona_impacto[0];
        const R1_de = this.zona_impacto[0] + this.zona_impacto[2];
        const R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3];
        const R2_ar = alguien.zona_impacto[1];
        const R2_iz = alguien.zona_impacto[0];
        const R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2];
        
        return R1_de > R2_iz && R1_iz < R2_de && R1_ar < R2_ab && R1_ab > R2_ar;
    }
    
    dibujar(ctx) {
        let sprite = this.va_derecha ? gameAssets['robot-right'] : gameAssets['robot'];
        if (sprite) {
            ctx.drawImage(sprite, this.x, this.y, this.ancho, this.alto);
        }
        
        ctx.fillStyle = 'red';
        ctx.fillRect(this.x + 15, this.y - 15, 100, 10);
        ctx.fillStyle = 'green';
        ctx.fillRect(this.x + 15, this.y - 15, this.salud, 10);
    }
}

class RoboDog {
    constructor(x, y, limite) {
        this.x = x;
        this.y = y;
        this.velocidad = 10;
        this.puntos = 10;
        this.daño = 10;
        this.va_izquierda = false;
        this.va_derecha = false;
        this.contador_pasos = 0;
        this.ancho = 100;
        this.alto = 68;
        this.camino = [120, limite];
        this.salud = 100;
        this.zona_impacto = [this.x, this.y, 130, 80];
    }
    
    se_mueve_solo() {
        if (this.velocidad > 0) {
            if (this.x + this.velocidad < this.camino[1]) {
                this.x += this.velocidad;
                this.va_derecha = true;
                this.va_izquierda = false;
            } else {
                this.velocidad = this.velocidad * -1;
                this.contador_pasos = 0;
            }
        } else {
            if (this.x - this.velocidad > this.camino[0]) {
                this.x += this.velocidad;
                this.va_izquierda = true;
                this.va_derecha = false;
            } else {
                this.velocidad = this.velocidad * -1;
                this.contador_pasos = 0;
            }
        }
        
        this.zona_impacto = [this.x, this.y, 130, 80];
    }
    
    se_encuentra_con(alguien) {
        const R1_ab = this.zona_impacto[1] + this.zona_impacto[3];
        const R1_ar = this.zona_impacto[1];
        const R1_iz = this.zona_impacto[0];
        const R1_de = this.zona_impacto[0] + this.zona_impacto[2];
        const R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3];
        const R2_ar = alguien.zona_impacto[1];
        const R2_iz = alguien.zona_impacto[0];
        const R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2];
        
        return R1_de > R2_iz && R1_iz < R2_de && R1_ar < R2_ab && R1_ab > R2_ar;
    }
    
    dibujar(ctx) {
        let sprite = this.va_derecha ? gameAssets['robodog'] : gameAssets['robodog-left'];
        if (sprite) {
            ctx.drawImage(sprite, this.x, this.y, this.ancho, this.alto);
        }
        
        ctx.fillStyle = 'red';
        ctx.fillRect(this.x + 15, this.y - 15, 100, 10);
        ctx.fillStyle = 'green';
        ctx.fillRect(this.x + 15, this.y - 15, this.salud, 10);
    }
}

class Jefe {
    constructor(x, y, limite) {
        this.x = x;
        this.y = y;
        this.velocidad = 5;
        this.puntos = 100;
        this.daño = 25;
        this.va_izquierda = false;
        this.va_derecha = false;
        this.contador_pasos = 0;
        this.ancho = 130;
        this.alto = 130;
        this.camino = [120, limite];
        this.salud = 350;
        this.zona_impacto = [this.x, this.y, 130, 80];
    }
    
    se_mueve_solo() {
        if (this.velocidad > 0) {
            if (this.x + this.velocidad < this.camino[1]) {
                this.x += this.velocidad;
                this.va_derecha = true;
                this.va_izquierda = false;
            } else {
                this.velocidad = this.velocidad * -1;
                this.contador_pasos = 0;
            }
        } else {
            if (this.x - this.velocidad > this.camino[0]) {
                this.x += this.velocidad;
                this.va_izquierda = true;
                this.va_derecha = false;
            } else {
                this.velocidad = this.velocidad * -1;
                this.contador_pasos = 0;
            }
        }
        
        this.zona_impacto = [this.x, this.y, 130, 80];
    }
    
    se_encuentra_con(alguien) {
        const R1_ab = this.zona_impacto[1] + this.zona_impacto[3];
        const R1_ar = this.zona_impacto[1];
        const R1_iz = this.zona_impacto[0];
        const R1_de = this.zona_impacto[0] + this.zona_impacto[2];
        const R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3];
        const R2_ar = alguien.zona_impacto[1];
        const R2_iz = alguien.zona_impacto[0];
        const R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2];
        
        return R1_de > R2_iz && R1_iz < R2_de && R1_ar < R2_ab && R1_ab > R2_ar;
    }
    
    dibujar(ctx) {
        let sprite = this.va_derecha ? gameAssets['boss-right'] : gameAssets['boss'];
        if (sprite) {
            ctx.drawImage(sprite, this.x, this.y, this.ancho, this.alto);
        }
        
        ctx.fillStyle = 'red';
        ctx.fillRect(this.x, this.y - 25, 175, 10);
        ctx.fillStyle = 'green';
        ctx.fillRect(this.x, this.y - 25, this.salud / 2, 10);
    }
}

class Proyectil {
    constructor(x, y, direccion) {
        this.x = x;
        this.y = y;
        this.direccion = direccion;
        this.velocidad = 12 * direccion;
        this.zona_impacto = [this.x - 5, this.y - 5, 10, 10];
        this.imagen = direccion > 0 ? gameAssets['projectile-1'] : gameAssets['projectile-2'];
    }
    
    se_encuentra_con(alguien) {
        const R1_ab = this.zona_impacto[1] + this.zona_impacto[3];
        const R1_ar = this.zona_impacto[1];
        const R1_iz = this.zona_impacto[0];
        const R1_de = this.zona_impacto[0] + this.zona_impacto[2];
        const R2_ab = alguien.zona_impacto[1] + alguien.zona_impacto[3];
        const R2_ar = alguien.zona_impacto[1];
        const R2_iz = alguien.zona_impacto[0];
        const R2_de = alguien.zona_impacto[0] + alguien.zona_impacto[2];
        
        return R1_de > R2_iz && R1_iz < R2_de && R1_ar < R2_ab && R1_ab > R2_ar;
    }
    
    dibujar(ctx) {
        if (this.imagen) {
            ctx.drawImage(this.imagen, this.x - 22, this.y - 17, 45, 34);
        }
        this.zona_impacto = [this.x - 5, this.y - 5, 10, 10];
    }
}

// ===== GAME VARIABLES =====
let heroe;
let villanos;
let balas;
let nivel;
let puntaje;
let tanda_disparos;
let keys = {};
const nivel_maximo = 5;

function init() {
    heroe = new Personaje(30, 325, VENTANA_X);
    villanos = [
        new RoboDog(600, 385, 720),  // Nivel 1 - Velocidad reducida
        new RoboDog(600, 385, 720),
        new Robot(300, 345, 720),
        new RoboDog(600, 385, 720),
        new Robot(300, 345, 720),
        new Jefe(700, 330, 720)
    ];
    
    // Reducir velocidad del primer RoboDog (Nivel 1)
    villanos[0].velocidad = 5;
    
    balas = [];
    nivel = 0;
    puntaje = 0;
    tanda_disparos = 0;
    gameState.nivel = 1;
    gameState.puntaje = 0;
    gameState.estaBenjugando = true;
    gameState.estaEnIntro = true;
    gameState.gana = false;
}

function update() {
    if (!gameState.estaBenjugando) return;
    
    heroe.se_mueve_segun(keys);
    villanos[nivel].se_mueve_solo();
    
    if (heroe.se_encuentra_con(villanos[nivel])) {
        heroe.es_golpeado();
        puntaje -= 5;
        heroe.salud -= villanos[nivel].daño;
    }
    
    if (tanda_disparos > 0) {
        tanda_disparos += 1;
    }
    if (tanda_disparos > 2) {
        tanda_disparos = 0;
    }
    
    for (let i = balas.length - 1; i >= 0; i--) {
        const bala = balas[i];
        
        if (villanos[nivel].se_encuentra_con(bala)) {
            villanos[nivel].salud -= 25;
            balas.splice(i, 1);
            
            if (villanos[nivel].salud <= 0) {
                puntaje += villanos[nivel].puntos;
                nivel++;
                
                if (nivel > nivel_maximo) {
                    gameState.gana = true;
                    gameState.estaBenjugando = false;
                } else {
                    gameState.nivel = Math.floor(nivel / 2) + 1;
                }
            }
        } else {
            bala.x += bala.velocidad;
            
            if (bala.x < 0 || bala.x > VENTANA_X) {
                balas.splice(i, 1);
            }
        }
    }
    
    if (keys['x'] && tanda_disparos === 0) {
        let direccion = heroe.va_izquierda ? -1 : (heroe.va_derecha ? 1 : -1);
        
        if (balas.length < 1) {
            balas.push(new Proyectil(heroe.x + heroe.ancho / 2, heroe.y + heroe.alto / 2, direccion));
        }
        tanda_disparos = 1;
    }
    
    if (heroe.salud < 1) {
        gameState.estaBenjugando = false;
        gameState.gana = false;
    }
}

function draw() {
    gameCtx.fillStyle = 'black';
    gameCtx.fillRect(0, 0, VENTANA_X, VENTANA_Y);
    
    if (gameAssets['background']) {
        gameCtx.drawImage(gameAssets['background'], 0, 0, VENTANA_X, VENTANA_Y);
    }
    
    heroe.dibujar(gameCtx);
    if (villanos[nivel]) {
        villanos[nivel].dibujar(gameCtx);
    }
    
    for (let bala of balas) {
        bala.dibujar(gameCtx);
    }
    
    gameCtx.fillStyle = 'green';
    gameCtx.font = '18px Arial';
    gameCtx.fillText(`Vida: ${heroe.salud}`, 40, 40);
    gameCtx.fillStyle = 'yellow';
    gameCtx.fillText(`Nivel: ${gameState.nivel}`, 380, 40);
    gameCtx.fillText(`Puntaje: ${puntaje}`, 750, 40);
}

function showIntro() {
    gameCtx.fillStyle = 'rgba(0, 0, 0, 0.8)';
    gameCtx.fillRect(0, 0, VENTANA_X, VENTANA_Y);
    
    gameCtx.fillStyle = 'red';
    gameCtx.font = 'bold 80px Arial';
    gameCtx.textAlign = 'center';
    gameCtx.fillText('EL JARL', VENTANA_X / 2, 100);
    
    gameCtx.fillStyle = 'white';
    gameCtx.font = '30px Arial';
    gameCtx.fillText('Presione ENTER para continuar...', VENTANA_X / 2, 300);
}

function showGameOver() {
    gameCtx.fillStyle = 'rgba(0, 0, 0, 0.95)';
    gameCtx.fillRect(0, 0, VENTANA_X, VENTANA_Y);
    
    gameCtx.fillStyle = 'red';
    gameCtx.font = 'bold 60px Arial';
    gameCtx.textAlign = 'center';
    gameCtx.fillText('JUEGO TERMINADO', VENTANA_X / 2, 80);
    
    const txt = gameState.gana ? '¡HAS GANADO! :D' : 'HAS PERDIDO :(';
    const col = gameState.gana ? 'green' : 'red';
    gameCtx.fillStyle = col;
    gameCtx.font = 'bold 50px Arial';
    gameCtx.fillText(txt, VENTANA_X / 2, 200);
    
    gameCtx.fillStyle = 'yellow';
    gameCtx.font = '30px Arial';
    gameCtx.fillText(`Puntaje Total: ${puntaje}`, VENTANA_X / 2, 300);
    
    gameCtx.fillStyle = 'white';
    gameCtx.font = '24px Arial';
    gameCtx.fillText('ENTER para cerrar', VENTANA_X / 2, 370);
    gameCtx.fillText('R para reintentar', VENTANA_X / 2, 410);
}

function gameLoop() {
    if (gameState.estaEnIntro) {
        draw();
        showIntro();
    } else if (gameState.estaBenjugando) {
        update();
        draw();
    } else {
        draw();
        showGameOver();
    }
    
    requestAnimationFrame(gameLoop);
}

// ===== INICIALIZACION =====
window.addEventListener('load', () => {
    gameCanvas = document.getElementById('gameCanvas');
    gameCtx = gameCanvas.getContext('2d');
    
    loadAssets();
    init();
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && gameState.estaEnIntro) {
            gameState.estaEnIntro = false;
            gameState.estaBenjugando = true;
        } else if (e.key === 'Enter' && !gameState.estaBenjugando) {
            location.reload();
        } else if (e.key.toLowerCase() === 'r' && !gameState.estaBenjugando) {
            init();
            gameState.estaEnIntro = false;
            gameState.estaBenjugando = true;
        }
        keys[e.key] = true;
    });
    
    document.addEventListener('keyup', (e) => {
        keys[e.key] = false;
    });
    
    gameLoop();
});

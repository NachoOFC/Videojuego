# 🎮 El Jarl - Versión Web (Phaser.js)

Una reescritura completa del juego "El Jarl" usando **Phaser.js** para que se pueda jugar directamente en el navegador.

## 📋 Características

✅ Versión 100% funcional en navegador
✅ Controles igual al juego original
✅ 6 niveles con diferentes enemigos
✅ Jefe final con más salud y desafío
✅ Sistema de puntuación
✅ Animaciones de enemigos
✅ Barras de salud visuales
✅ Interfaz retro-arcade
✅ Compatible con todos los navegadores modernos

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| **← →** | Mover izquierda/derecha |
| **ESPACIO** | Saltar |
| **X** | Disparar |
| **ENTER** | Comenzar juego |
| **R** | Reintentar (en pantalla de Game Over) |

## 🚀 Cómo ejecutar

### Opción 1: Servidor Web Simple (Recomendado)

#### Windows (PowerShell):
```powershell
# Instalar dependencias (solo primera vez)
npm install

# Iniciar servidor
npm start
```

Luego abre tu navegador en: `http://localhost:8000`

#### macOS/Linux:
```bash
# Instalar dependencias (solo primera vez)
npm install

# Iniciar servidor
npm start
```

### Opción 2: Usar Python

#### Python 3.7+:
```bash
python -m http.server 8000
```

#### Python 2.7:
```bash
python -m SimpleHTTPServer 8000
```

Luego abre: `http://localhost:8000`

### Opción 3: Directamente en el navegador

Si solo quieres probar rápidamente, simplemente abre el archivo `index.html` con doble clic (funciona, pero sin recarga automática en cambios).

## 📁 Estructura del Proyecto

```
.
├── index.html          # Página principal HTML
├── js/
│   └── main.js        # Lógica del juego con Phaser.js
├── img/               # Imágenes de sprites (reutilizadas del original)
│   ├── vikingo.png
│   ├── vikingoderecha1.png
│   ├── vikingoizquierda1.png
│   ├── robodog.png
│   ├── robodogizquierda.png
│   ├── superrobot.png
│   ├── superrobotderecha.png
│   ├── jefe.png
│   ├── jefederecha.png
│   ├── jefe2.png
│   ├── jefe3.png
│   ├── disparo1.png
│   ├── disparo2.png
│   ├── fondobasico.jpg
│   └── ...
├── sounds/            # Audio (reutilizado del original)
│   └── music.mp3
├── package.json       # Dependencias npm
└── README.md         # Este archivo
```

## 🔄 Actualización desde Python

Si necesitas actualizar algo:

1. **Assets (imágenes y sonidos)**: Mantén todo en las carpetas `img/` y `sounds/`
2. **Lógica del juego**: Está en `js/main.js` - puedes editarlo directamente
3. **Estilos**: Están en `index.html` dentro de la etiqueta `<style>`

## 📊 Niveles

| Nivel | Enemigo | Salud | Daño | Puntos |
|-------|---------|-------|------|--------|
| 1 | Robodog | 100 | 10 | 10 |
| 2 | Robodog | 100 | 10 | 10 |
| 3 | Robot | 100 | 15 | 10 |
| 4 | Robodog | 100 | 10 | 10 |
| 5 | Robot | 100 | 15 | 10 |
| 6 | **JEFE** | 350 | 25 | 100 |

## 🌐 Desplegar en Netlify (Gratis)

1. Crea una cuenta en [netlify.com](https://netlify.com)
2. Conecta tu repositorio de GitHub
3. Netlify detectará automáticamente que es un sitio estático
4. ¡Tu juego estará en vivo en minutos!

Alternativa drag-and-drop:
```
1. Crea un ZIP con todo el contenido
2. Ve a https://app.netlify.com/drop
3. Arrastra y suelta tu ZIP
4. ¡Listo! Tu juego está en internet
```

## 🔧 Personalización

### Cambiar dificultad

En `js/main.js`, busca `createLevelEnemies()` y modifica:
- `health`: Salud del enemigo
- `speed`: Velocidad de movimiento
- `damage`: Daño que inflige

### Cambiar velocidad del jugador

Busca `createPlayer()` y modifica:
- `speed: 200` - Velocidad de movimiento
- `jumpPower: 500` - Potencia del salto

### Agregar nuevos niveles

En `createLevelEnemies()`, añade más objetos al array `levelEnemies`:

```javascript
{ type: 'robodog', x: 600, y: 385, health: 120 },
// ... más niveles
```

## 🐛 Posibles mejoras futuras

- [ ] Efectos de sonido para disparos y saltos
- [ ] Partículas de explosión
- [ ] Múltiples armas
- [ ] Poderes especiales
- [ ] Sistema de guardado de puntuación con localStorage
- [ ] Pantalla de leaderboard
- [ ] Animaciones mejoradas con sprites animados
- [ ] Sistema de movimientos especiales

## 📝 Notas técnicas

- Usa **Phaser 3.55** (última versión estable)
- Sin dependencias externas (solo Phaser desde CDN)
- Compatible con navegadores modernos (Chrome, Firefox, Safari, Edge)
- Responsive pero optimizado para pantallas de escritorio

## 🎨 Créditos

- **Concepto original**: Juego Python original "El Jarl"
- **Framework**: [Phaser.js](https://phaser.io/)
- **Hosting**: Netlify/Vercel/GitHub Pages

## 📞 Soporte

Si tienes dudas o problemas:

1. Verifica que todas las imágenes y sonidos estén en las carpetas correctas
2. Comprueba la consola del navegador (F12) para ver errores
3. Asegúrate de que el servidor está corriendo en `localhost:8000`

¡Que disfrutes el juego! 🎮

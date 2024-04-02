# Introducción al desarrollo de videojuegos
Prácticas de la asignatura de Introducción al desarrollo de videojuegos que consiste en la generación de rectángulos con colores
predefinidos en el archivo `enemies.json`. Los rectángulos aparecerán en la posición definida en el archivo `level_01.json` 
y se moverán en una dirección aleatoria. De igual manera, la configuración general de la pantalla se encuentra en el archivo
`window.json`.

## Prerrequisitos
* Python v3.9 o posterior
* Pygame-ce v2.0.1
* esper v3.2
* pyinstaller v6.5.0
* packaging v24.0

#### Instalación
Primero, se debe iniciar un entorno virtual de Python. Para ello, se debe ejecutar el siguiente comando:
```bash
python -m venv venv
```
Posteriormente, se debe activar el entorno virtual. Para ello, se debe ejecutar el siguiente comando:
```bash
source venv/bin/activate
```
Finalmente, se debe instalar Pygame y demás paquetes.
```bash
pip install -r requirements.txt
```

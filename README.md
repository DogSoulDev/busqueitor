# Instrucciones para Configurar y Usar el Proyecto

## Creación de un Entorno Virtual y Configuración del Proyecto

Un entorno virtual es un ambiente aislado que permite administrar las dependencias específicas de un proyecto Python sin interferir con los paquetes instalados globalmente o en otros entornos virtuales. Esto facilita el manejo de diferentes versiones de paquetes y evita conflictos entre proyectos.

### Pasos para Configurar y Ejecutar `busqueitor.py`

1. **Crea una nueva carpeta para el proyecto**:

   ```bash
   mkdir mi_proyecto
   cd mi_proyecto
   ```

2. **Crea el entorno virtual**:

   Este comando crea un nuevo entorno virtual en un directorio llamado `.venv` dentro de tu proyecto.

   ```bash
   python3 -m venv .venv
   ```

3. **Activa el entorno virtual**:

   Esto activa el entorno virtual para que puedas instalar paquetes y ejecutar scripts dentro de él.

   ```bash
   source .venv/bin/activate
   ```

4. **Descarga el repositorio desde GitHub**:

   Clona el repositorio del proyecto en tu nueva carpeta.

   ```bash
   git clone https://github.com/tu_usuario/Busqueitor.git
   cd Busqueitor
   ```

5. **Instala las dependencias necesarias**:

   Para que `busqueitor.py` funcione correctamente, necesitas instalar las dependencias listadas en el archivo `requirements.txt`. Usa el siguiente comando para instalarlas:

   ```bash
   pip install -r requirements.txt
   ```

   Alternativamente, puedes instalar las dependencias manualmente con los siguientes comandos:

   ```bash
   pip install requests
   pip install pdfplumber
   pip install PyPDF2
   pip install colorama
   ```

6. **Ejecuta el script `busqueitor.py`**:

   Utiliza el siguiente comando para ejecutar el script y sigue las opciones que aparecerán en la Shell.

   ```bash
   python3 busqueitor.py
   ```

   ## ¡Gracias por Usar Este Script! 😊

   ¡Estoy muy agradecido de que uses mi pequeño script, Busqueitor! Espero que este script te sea de gran ayuda y facilite tu trabajo. Si te ha sido útil, no olvides dar una estrellita ⭐, eso siempre mola 😄

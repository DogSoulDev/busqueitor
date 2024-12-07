# Instrucciones para Configurar y Usar el Proyecto

## Creación de un Entorno Virtual

Un entorno virtual es un ambiente aislado que permite administrar las dependencias específicas de un proyecto Python sin interferir con los paquetes instalados globalmente o en otros entornos virtuales. Esto facilita el manejo de diferentes versiones de paquetes y evita conflictos entre proyectos.

### Pasos para Crear y Activar un Entorno Virtual

1. **Navega al directorio de tu proyecto**:

   Reemplaza `mi_proyecto` con el nombre de tu directorio de proyecto.

   ```bash
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

4. **Instala las dependencias necesarias**:

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

5. **Desactiva el entorno virtual cuando hayas terminado**:

   Es importante desactivar el entorno virtual para evitar conflictos con otros proyectos.

   ```bash
   deactivate
   ```

## Uso del Script `busqueitor.py`

El script `busqueitor.py` es una herramienta diseñada para facilitar la búsqueda de DNIs, NIFs y NIEs en documentos PDF dentro de un directorio específico. Este script ha sido creado por DogSoulDev. A continuación, se presentan los pasos para utilizar este script de manera efectiva.

### Pasos para Usar `busqueitor.py`

1. **Asegúrate de tener el entorno virtual activado**:

   Antes de ejecutar el script, asegúrate de que el entorno virtual esté activado.

   ```bash
   source .venv/bin/activate
   ```

2. **Navega al directorio donde se encuentra `busqueitor.py`**:

   Reemplaza `mi_proyecto` con el nombre de tu directorio de proyecto.

   ```bash
   cd mi_proyecto
   ```

3. **Ejecuta el script `busqueitor.py`**:

   Utiliza el siguiente comando para ejecutar el script. Asegúrate de reemplazar `directorio_a_buscar` con el directorio en el que deseas realizar la búsqueda.

   ```bash
   python busqueitor.py directorio_a_buscar
   ```

4. **Interpreta los resultados**:

   El script mostrará una lista de archivos PDF encontrados en el directorio especificado que contienen DNIs, NIFs o NIEs. Revisa la salida en la terminal para ver los resultados.

### Ejemplo de Uso de `busqueitor.py` para Usuarios sin Conocimientos Técnicos

A continuación, se presenta un ejemplo ficticio de cómo un usuario sin conocimientos técnicos puede utilizar el script `busqueitor.py` en un sistema operativo Linux.

1. **Abre una terminal**:

   En tu sistema Linux, abre una terminal. Puedes hacerlo buscando "Terminal" en el menú de aplicaciones o utilizando el atajo de teclado `Ctrl + Alt + T`.

2. **Navega al directorio del proyecto**:

   Supongamos que tu proyecto se encuentra en el escritorio en una carpeta llamada `Busqueitor`. Utiliza el siguiente comando para navegar a esa carpeta:

   ```bash
   cd ~/Desktop/Busqueitor
   ```

3. **Activa el entorno virtual**:

   Antes de ejecutar el script, necesitas activar el entorno virtual. Usa el siguiente comando:

   ```bash
   source .venv/bin/activate
   ```

4. **Ejecuta el script `busqueitor.py`**:

   Ahora, ejecuta el script para buscar en una carpeta específica. Supongamos que deseas buscar en una carpeta llamada `Documentos` en tu escritorio. Utiliza el siguiente comando:

   ```bash
   python busqueitor.py ~/Desktop/Documentos
   ```

5. **Revisa los resultados**:

   Después de ejecutar el comando anterior, el script mostrará una lista de archivos PDF que contienen DNIs, NIFs o NIEs en la terminal. Lee los resultados para ver qué documentos contienen la información buscada.

Este ejemplo te guía paso a paso para utilizar el script `busqueitor.py` en un sistema Linux, incluso si no tienes conocimientos técnicos previos.

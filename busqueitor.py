# Importar el módulo re para trabajar con expresiones regulares
# Documentación: https://docs.python.org/3/library/re.html
import re

# Importar el módulo shlex para dividir cadenas de texto en tokens
# Documentación: https://docs.python.org/3/library/shlex.html
import shlex

# Importar el módulo csv para manejar archivos CSV
# Documentación: https://docs.python.org/3/library/csv.html
import csv

# Importar el módulo logging para registro de errores y depuración
# Documentación: https://docs.python.org/3/library/logging.html
import logging

# Importar List y Dict de typing para tipado estático
# Documentación: https://docs.python.org/3/library/typing.html
from typing import List, Dict

# Importar Path de pathlib para manejo de rutas de archivos
# Documentación: https://docs.python.org/3/library/pathlib.html
from pathlib import Path

# Importar datetime para manejo de fechas y horas
# Documentación: https://docs.python.org/3/library/datetime.html
from datetime import datetime

# Importar requests para realizar peticiones HTTP
# Documentación: https://docs.python-requests.org/en/latest/
import requests

# Importar pdfplumber para extraer texto de PDFs (método principal)
# Documentación: https://github.com/jsvine/pdfplumber
import pdfplumber

# Importar PyPDF2 para extraer texto de PDFs (método alternativo)
# Documentación: https://pypdf2.readthedocs.io/en/latest/
from PyPDF2 import PdfFileReader

# Importar init, Fore y Style de colorama para colorear la salida en terminal
# Documentación: https://pypi.org/project/colorama/
from colorama import init, Fore, Style

# Importar os para funcionalidades dependientes del sistema operativo (Linux, Windows, Mac)
# Documentación: https://docs.python.org/3/library/os.html
import os

# Inicializar colorama para soporte multiplataforma de texto coloreado en terminal
init()

# Configurar logging para depuración y seguimiento de errores
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DocumentValidator:
    """
    Clase para validar documentos de identidad españoles (DNI, NIE, NIF) y procesar archivos PDF para extraer y validar dichos documentos.
    Atributos:
        LETRAS_VALIDACION (str): Letras de validación para el cálculo del dígito de control del DNI y NIE.
        PATRON_DNI (str): Patrón regex para identificar un DNI.
        PATRON_NIE (str): Patrón regex para identificar un NIE.
        PATRON_NIF (str): Patrón regex para identificar un NIF.
        stats (dict): Diccionario para almacenar estadísticas del procesamiento de documentos.
    Métodos:
        clean_document(doc: str) -> str:
            Limpia un documento eliminando espacios, puntos y guiones, y lo convierte a mayúsculas.
        validate_dni(dni: str) -> bool:
            Valida un DNI español.
        validate_nie(nie: str) -> bool:
            Valida un NIE español.
        validate_nif(nif: str) -> bool:
            Valida un NIF español.
        download_pdf(url: str, output_path: str) -> bool:
            Descarga un archivo PDF desde una URL y lo guarda en la ruta especificada.
        process_pdf(source: str, is_url: bool = False) -> List[Dict]:
            Procesa un archivo PDF para extraer y validar documentos de identidad españoles.
        save_results(resultados: List[Dict], archivo: str):
            Guarda los resultados del procesamiento en un archivo CSV.
    """

    LETRAS_VALIDACION = 'TRWAGMYFPDXBNJZSQVHLCKET'
    PATRON_DNI = r'\b\d{8}[A-Z]\b'
    PATRON_NIE = r'\b[XYZ]\d{7}[A-Z]\b'
    PATRON_NIF = r'\b[A-HJNP-SUVW]\d{7}[0-9A-Z]\b'

    def __init__(self):
        self.stats = {
            'archivos_procesados': 0,
            'dni_validos': 0,
            'nie_validos': 0,
            'nif_validos': 0,
            'docs_invalidos': 0
        }

    @staticmethod
    def clean_document(doc: str) -> str:
        return re.sub(r'[\s.-]', '', doc).upper()

    @classmethod
    def validate_dni(cls, dni: str) -> bool:
        dni = cls.clean_document(dni)
        try:
            if not re.match(r'^\d{8}[A-Z]$', dni):
                return False
            numbers, letter = dni[:-1], dni[-1]
            return letter == cls.LETRAS_VALIDACION[int(numbers) % 23]
        except (IndexError, ValueError):
            return False

    @classmethod
    def validate_nie(cls, nie: str) -> bool:
        nie = cls.clean_document(nie)
        try:
            if not re.match(r'^[XYZ]\d{7}[A-Z]$', nie):
                return False
            prefix = {'X': '0', 'Y': '1', 'Z': '2'}
            numbers = prefix[nie[0]] + nie[1:-1]
            return nie[-1] == cls.LETRAS_VALIDACION[int(numbers) % 23]
        except (IndexError, ValueError, KeyError):
            return False

    @classmethod
    def validate_nif(cls, nif: str) -> bool:
        nif = cls.clean_document(nif)
        return bool(re.match(r'^[A-HJNP-SUVW]\d{7}[0-9A-Z]$', nif))

    def download_pdf(self, url: str, output_path: str) -> bool:
        """
        Descarga un archivo PDF desde una URL y lo guarda en la ruta especificada.

        Args:
            url (str): URL del archivo PDF.
            output_path (str): Ruta de salida para guardar el archivo PDF.

        Returns:
            bool: True si la descarga fue exitosa, False si hubo un error.
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            logging.error(f"Error descargando el PDF: {str(e)}")
            return False

    def process_pdf(self, source: str, is_url: bool = False) -> List[Dict]:
        """
        Procesa un archivo PDF para extraer y validar documentos de identidad españoles.

        Args:
            source (str): Ruta del archivo PDF o URL del archivo PDF.
            is_url (bool): Indica si la fuente es una URL.

        Returns:
            List[Dict]: Lista de resultados del análisis.
        """
        temp_pdf = "temp_download.pdf" if is_url else source
        resultados = []

        try:
            if is_url:
                print(f"{Fore.YELLOW}⌛ Descargando PDF...{Style.RESET_ALL}")
                if not self.download_pdf(source, temp_pdf):
                    print(f"{Fore.RED}✗ Error descargando el PDF{Style.RESET_ALL}")
                    return resultados

            print(f"{Fore.YELLOW}⌛ Extrayendo texto...{Style.RESET_ALL}")
            try:
                with pdfplumber.open(temp_pdf) as pdf:
                    texto = ""
                    total_paginas = len(pdf.pages)
                    for i, pagina in enumerate(pdf.pages, 1):
                        print(f"\rProcesando página {i}/{total_paginas}...", end="", flush=True)
                        texto += pagina.extract_text() or ""
                    print(f"\n{Fore.GREEN}✓ Texto extraído con éxito{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.YELLOW}⌛ Intentando método alternativo...{Style.RESET_ALL}")
                with open(temp_pdf, 'rb') as archivo:
                    reader = PdfFileReader(archivo)
                    texto = ""
                    total_paginas = len(reader.pages)
                    for i, pagina in enumerate(reader.pages, 1):
                        print(f"\rProcesando página {i}/{total_paginas}...", end="", flush=True)
                        texto += pagina.extract_text() or ""
                    print(f"\n{Fore.GREEN}✓ Texto extraído con éxito{Style.RESET_ALL}")

            print(f"{Fore.YELLOW}⌛ Buscando documentos...{Style.RESET_ALL}")
            for patron, tipo in [
                (self.PATRON_DNI, 'DNI'),
                (self.PATRON_NIE, 'NIE'),
                (self.PATRON_NIF, 'NIF')
            ]:
                coincidencias = list(re.finditer(patron, texto))
                if coincidencias:
                    print(f"{Fore.CYAN}Se encontraron {len(coincidencias)} {tipo}(s){Style.RESET_ALL}")

                for match in coincidencias:
                    doc = match.group()
                    doc_limpio = self.clean_document(doc)

                    es_valido = False
                    if tipo == 'DNI':
                        es_valido = self.validate_dni(doc_limpio)
                        if es_valido:
                            self.stats['dni_validos'] += 1
                    elif tipo == 'NIE':
                        es_valido = self.validate_nie(doc_limpio)
                        if es_valido:
                            self.stats['nie_validos'] += 1
                    elif tipo == 'NIF':
                        es_valido = self.validate_nif(doc_limpio)
                        if es_valido:
                            self.stats['nif_validos'] += 1

                    if not es_valido:
                        self.stats['docs_invalidos'] += 1

                    resultados.append({
                        'tipo': tipo,
                        'documento': doc,
                        'documento_limpio': doc_limpio,
                        'valido': es_valido
                    })

            self.stats['archivos_procesados'] += 1
            return resultados

        except Exception as e:
            print(f"{Fore.RED}Error procesando el PDF: {str(e)}{Style.RESET_ALL}")
            return resultados

        finally:
            if is_url and Path(temp_pdf).exists():
                try:
                    Path(temp_pdf).unlink()
                    print(f"{Fore.GREEN}✓ Archivo temporal eliminado{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Error eliminando el archivo temporal: {str(e)}{Style.RESET_ALL}")

    def save_results(self, resultados: List[Dict], archivo: str):
        """
        Guardar los resultados en un archivo CSV.

        Args:
            resultados: Lista de documentos encontrados.
            archivo: Nombre del archivo CSV de salida.
        """
        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['Tipo', 'Documento', 'Documento Limpio', 'Valido']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for resultado in resultados:
                    valido = 'Sí' if resultado['valido'] else 'No'
                    simbolo = '✓' if resultado['valido'] else '⚠'
                    writer.writerow({
                        'Tipo': resultado['tipo'],
                        'Documento': resultado['documento'],
                        'Documento Limpio': resultado['documento_limpio'],
                        'Valido': f"{simbolo} {valido}"
                    })
                    
                    # Mostrar en la terminal con colores
                    estado_color = Fore.GREEN if resultado['valido'] else Fore.RED
                    print(f"{Fore.CYAN}Tipo: {Style.RESET_ALL}{resultado['tipo']}")
                    print(f"{Fore.CYAN}Documento: {Style.RESET_ALL}{resultado['documento']}")
                    print(f"{Fore.CYAN}Documento Limpio: {Style.RESET_ALL}{resultado['documento_limpio']}")
                    print(f"{Fore.CYAN}Valido: {estado_color}{simbolo} {valido}{Style.RESET_ALL}")
                    print()

                # Agregar resumen al final del archivo CSV
                writer.writerow({})
                writer.writerow({'Tipo': 'Resumen'})
                writer.writerow({'Tipo': 'Total DNI', 'Documento': self.stats['dni_validos']})
                writer.writerow({'Tipo': 'Total NIE', 'Documento': self.stats['nie_validos']})
                writer.writerow({'Tipo': 'Total NIF', 'Documento': self.stats['nif_validos']})
                writer.writerow({'Tipo': 'Total Documentos', 'Documento': len(resultados)})

            print(f"{Fore.GREEN}✓ Results saved to {archivo}{Style.RESET_ALL}")
        except Exception as e:
            error_msg = f"Error saving results: {str(e)}"
            logging.error(error_msg)
            print(f"{Fore.RED}✗ {error_msg}{Style.RESET_ALL}")
            raise

def print_banner():
    """
    Muestra un banner en la terminal.
    """
    banner = rf"""{Fore.CYAN}
    /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\\
   ( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )
    > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ < 
    /\_/\     ____                             _ _                 /\_/\\
   ( o.o )   | __ ) _   _ ___  __ _ _   _  ___(_) |_ ___  _ __    ( o.o )
    > ^ <    |  _ \| | | / __|/ _` | | | |/ _ \ | __/ _ \| '__|    > ^ < 
    /\_/\    | |_) | |_| \__ \ (_| | |_| |  __/ | || (_) | |       /\_/\\
   ( o.o )   |____/ \__,_|___/\__, |\__,_|\___|_|\__\___/|_|      ( o.o )
    > ^ <                        |_|                                 > ^ < 
    /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\  /\_/\\
   ( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )( o.o )
    > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ <  > ^ < 
{Style.RESET_ALL}"""
    print(banner)

def mostrar_menu() -> int:
    """
    Muestra el menú principal y obtiene la elección del usuario.

    Returns:
        int: La opción de menú seleccionada.
    """
    print_banner()
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Añadir URL de archivo PDF")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Subir o arrastrar y analizar uno o más archivos PDF desde el ordenador")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Mostrar ayuda")
    print(f"{Fore.GREEN}4.{Style.RESET_ALL} Salir del script")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")

    while True:
        try:
            opcion = int(input(f"\n{Fore.CYAN}Seleccione una opción (1-4):{Style.RESET_ALL} "))
            if 1 <= opcion <= 4:
                return opcion
            print(f"{Fore.RED}Error: Por favor seleccione una opción válida (1-4){Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Error: Por favor ingrese un número válido{Style.RESET_ALL}")

def sanitize_path(path: str) -> str:
    """
    Limpia la ruta del archivo eliminando caracteres no permitidos que puedan interferir con el análisis.

    Args:
        path (str): Ruta original del archivo.

    Returns:
        str: Ruta del archivo sanitizada.
    """
    # Eliminar comillas simples o dobles al inicio y al final
    path = path.strip().strip('\'"')

    # Eliminar caracteres no deseados utilizando una expresión regular
    # Permitimos letras, números, espacios y los símbolos / \ . _ - : ~ ( ) á é í ó ú Á É Í Ó Ú
    path = re.sub(r'[^\w\s/\\\.\_\-\:\~\(\)áéíóúÁÉÍÓÚ]', '', path)

    # Expandir ruta de usuario (manejar '~' correctamente)
    path = os.path.expanduser(path)

    # Convertir a ruta absoluta
    path = os.path.abspath(path)

    return path    

def analizar_archivo(validador: DocumentValidator) -> List[Dict]:
    """
    Analiza un archivo PDF local o arrastrado al terminal.
    
    Args:
        validador: Instancia de DocumentValidator para procesar el archivo

    Returns:
        List[Dict]: Lista de resultados del análisis
    """
    print(f"\n{Fore.CYAN}Arrastra y suelta el archivo PDF en el terminal o ingresa la ruta del archivo:{Style.RESET_ALL} ")
    input_str = input().strip()

    # Usar shlex para dividir correctamente la entrada
    tokens = shlex.split(input_str)
    if not tokens:
        print(f"{Fore.RED}Error: No se ingresó ninguna ruta de archivo{Style.RESET_ALL}")
        return []

    ruta_archivo = tokens[0]
    ruta_archivo = sanitize_path(ruta_archivo)

    if not Path(ruta_archivo).is_file():
        print(f"{Fore.RED}Error: El archivo no existe o la ruta es incorrecta:{Style.RESET_ALL} {ruta_archivo}")
        return []

    ext = Path(ruta_archivo).suffix.lower()
    if ext == '.pdf':
        print(f"\n{Fore.YELLOW}⌛ Analizando documento PDF...{Style.RESET_ALL}")
        resultados = validador.process_pdf(ruta_archivo)
    else:
        print(f"{Fore.RED}Error: Solo se admiten archivos PDF{Style.RESET_ALL}")
        resultados = []

    if resultados:
        print(f"\n{Fore.GREEN}✓ Se encontraron {len(resultados)} documentos:{Style.RESET_ALL}")
        for doc in resultados:
            estado = f"{Fore.GREEN}✓{Style.RESET_ALL}" if doc['valido'] else f"{Fore.RED}⚠{Style.RESET_ALL}"
            print(f"{estado} {doc['tipo']}: {doc['documento']}")
    else:
        print(f"{Fore.RED}No se encontraron documentos.{Style.RESET_ALL}")
    return resultados

def analizar_multiples_archivos(validador: DocumentValidator) -> List[Dict]:
    """
    Analiza múltiples archivos PDF locales o arrastrados al terminal.

    Args:
        validador: Instancia de DocumentValidator para procesar los archivos

    Returns:
        List[Dict]: Lista de resultados del análisis
    """
    print(f"\n{Fore.CYAN}Arrastra y suelta los archivos PDF en el terminal o ingresa las rutas de los archivos separadas por comas:{Style.RESET_ALL} ")
    input_str = input().strip()

    # Usar shlex para dividir correctamente la entrada
    tokens = shlex.split(input_str)
    rutas_archivos = [sanitize_path(ruta) for ruta in tokens]
    resultados_totales = []

    for ruta_archivo in rutas_archivos:
        if not Path(ruta_archivo).is_file():
            print(f"{Fore.RED}Error: El archivo no existe o la ruta es incorrecta:{Style.RESET_ALL} {ruta_archivo}")
            continue

        ext = Path(ruta_archivo).suffix.lower()
        if ext == '.pdf':
            print(f"\n{Fore.YELLOW}⌛ Analizando documento PDF: {ruta_archivo}...{Style.RESET_ALL}")
            resultados = validador.process_pdf(ruta_archivo)
            if resultados:
                print(f"\n{Fore.GREEN}✓ Se encontraron {len(resultados)} documentos en {ruta_archivo}:{Style.RESET_ALL}")
                for doc in resultados:
                    estado = f"{Fore.GREEN}✓{Style.RESET_ALL}" if doc['valido'] else f"{Fore.RED}⚠{Style.RESET_ALL}"
                    print(f"{estado} {doc['tipo']}: {doc['documento']}")
                resultados_totales.extend(resultados)
            else:
                print(f"{Fore.RED}No se encontraron documentos en {ruta_archivo}.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Solo se admiten archivos PDF: {ruta_archivo}{Style.RESET_ALL}")

    return resultados_totales

def exportar_resultados(validador: DocumentValidator, resultados: List[Dict]):
    """
    Exportar los resultados a un archivo CSV.

    Args:
        validador: Instancia de DocumentValidator.
        resultados: Lista de documentos encontrados.
    """
    nombre_archivo = input(f"\n{Fore.CYAN}Ingrese el nombre del archivo CSV (sin extensión):{Style.RESET_ALL} ").strip()
    output_file = f"{nombre_archivo}.csv"
    try:
        validador.save_results(resultados, output_file)
        print(f"\n{Fore.GREEN}✓ Resultados guardados en {output_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}⚠ Error exportando: {str(e)}{Style.RESET_ALL}")

def mostrar_ayuda():
    """
    Mostrar la ayuda detallada sobre cómo usar el script.
    """
    print(f"{Fore.CYAN}Ayuda de Busqueitor{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Añadir URL de archivo PDF: Permite ingresar la URL de un archivo PDF para analizar.")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Subir y analizar archivo PDF desde el ordenador: Permite seleccionar un archivo PDF local para analizar.")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Exportar resultados a CSV: Exporta los resultados del análisis a un archivo CSV.")
    print(f"{Fore.GREEN}4.{Style.RESET_ALL} Mostrar ayuda: Muestra esta ayuda detallada.")
    print(f"{Fore.GREEN}5.{Style.RESET_ALL} Salir del script: Cierra el script.")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.RED}Recuerde eliminar cualquier espacio que tenga una vez arrastrados a la Shell sus documentos PDF, para que se puedan analizar correctamente.{Style.RESET_ALL}")

    while True:
        try:
            opcion = int(input(f"\n{Fore.CYAN}¿Necesita más ayuda o desea dejar feedback?{Style.RESET_ALL}\n"
                               f"{Fore.GREEN}1.{Style.RESET_ALL} Volver al menú principal\n"
                               f"{Fore.GREEN}2.{Style.RESET_ALL} Dejar feedback en GitHub\n"
                               f"{Fore.GREEN}3.{Style.RESET_ALL} Salir del script\n"
                               f"{Fore.CYAN}Seleccione una opción (1-3):{Style.RESET_ALL} "))
            if opcion == 1:
                return
            elif opcion == 2:
                print(f"\n{Fore.CYAN}Por favor, deje su feedback en el siguiente enlace:{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}https://github.com/DogSoulDev{Style.RESET_ALL}\n")
            elif opcion == 3:
                print(f"{Fore.MAGENTA}Gracias por utilizar {Fore.YELLOW}Busqueitor{Fore.MAGENTA}, hasta la proxima! {Style.RESET_ALL}")
                exit()
            else:
                print(f"{Fore.RED}Error: Por favor seleccione una opción válida (1-3){Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Error: Por favor ingrese un número válido{Style.RESET_ALL}")

def main():
    """
    Función principal con menú interactivo para usar el validador de documentos.
    """
    validador = DocumentValidator()
    url = None
    resultados = []

    while True:
        try:
            opcion = mostrar_menu()

            if opcion == 1:
                # Obtener la URL del PDF del usuario
                url = input(f"\n{Fore.CYAN}Ingrese la URL del archivo PDF:{Style.RESET_ALL} ").strip()
                if not url.startswith(('http://', 'https://')):
                    print(f"{Fore.RED}Error: La URL debe comenzar con http:// o https://{Style.RESET_ALL}")
                    url = None
                    continue
                print(f"\n{Fore.GREEN}✓ URL registrada:{Style.RESET_ALL} {url}")

                # Analizar el documento en busca de documentos de identidad
                print(f"\n{Fore.YELLOW}⌛ Analizando documentos de identidad...{Style.RESET_ALL}")
                resultados = validador.process_pdf(url, is_url=True)
                if resultados:
                    print(f"\n{Fore.GREEN}✓ Se encontraron {len(resultados)} documentos:{Style.RESET_ALL}")
                    for doc in resultados:
                        estado = f"{Fore.GREEN}✓{Style.RESET_ALL}" if doc['valido'] else f"{Fore.RED}⚠{Style.RESET_ALL}"
                        print(f"{estado} {doc['tipo']}: {doc['documento']}")
                else:
                    print(f"{Fore.RED}No se encontraron documentos.{Style.RESET_ALL}")

            elif opcion == 2:
                # Subir o arrastrar y analizar uno o más archivos PDF desde el ordenador
                resultados = analizar_multiples_archivos(validador)

            elif opcion == 3:
                # Mostrar ayuda
                mostrar_ayuda()

            elif opcion == 4:
                # Salir del programa
                print(f"{Fore.MAGENTA}Gracias por utilizar {Fore.YELLOW}Busqueitor{Fore.MAGENTA}, hasta la proxima! {Style.RESET_ALL}")
                break

            # Alternativas adicionales después de seleccionar una opción
            while resultados:
                print(f"\n{Fore.CYAN}¿Desea realizar otra acción?{Style.RESET_ALL}")
                print(f"{Fore.GREEN}1.{Style.RESET_ALL} Volver al menú principal")
                print(f"{Fore.GREEN}2.{Style.RESET_ALL} Exportar resultados a CSV (individualmente)")
                print(f"{Fore.GREEN}3.{Style.RESET_ALL} Exportar todos los resultados a un solo CSV")
                print(f"{Fore.GREEN}4.{Style.RESET_ALL} Mostrar ayuda de Busqueitor")
                print(f"{Fore.GREEN}5.{Style.RESET_ALL} Salir del script")
                try:
                    sub_opcion = int(input(f"\n{Fore.CYAN}Seleccione una opción (1-5):{Style.RESET_ALL} "))
                    if sub_opcion == 1:
                        break
                    elif sub_opcion == 2:
                        for resultado in resultados:
                            nombre_archivo = input(f"\n{Fore.CYAN}Ingrese el nombre del archivo CSV para {resultado['documento']} (sin extensión):{Style.RESET_ALL} ").strip()
                            output_file = f"{nombre_archivo}.csv"
                            validador.save_results([resultado], output_file)
                            print(f"\n{Fore.GREEN}✓ Resultados guardados en {output_file}{Style.RESET_ALL}")
                    elif sub_opcion == 3:
                        nombre_archivo = input(f"\n{Fore.CYAN}Ingrese el nombre del archivo CSV (sin extensión):{Style.RESET_ALL} ").strip()
                        output_file = f"{nombre_archivo}.csv"
                        validador.save_results(resultados, output_file)
                        print(f"\n{Fore.GREEN}✓ Resultados guardados en {output_file}{Style.RESET_ALL}")
                    elif sub_opcion == 4:
                        mostrar_ayuda()
                    elif sub_opcion == 5:
                        print(f"{Fore.MAGENTA}Gracias por utilizar {Fore.YELLOW}Busqueitor{Fore.MAGENTA}, hasta la proxima! {Style.RESET_ALL}")
                        return
                    else:
                        print(f"{Fore.RED}Error: Por favor seleccione una opción válida (1-5){Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Error: Por favor ingrese un número válido{Style.RESET_ALL}")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Programa interrumpido por el usuario{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
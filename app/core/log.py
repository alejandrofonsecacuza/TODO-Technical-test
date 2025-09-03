import logging
import sys



def setup_logging():
    """
    Configura y devuelve un logger para el backend.

    Este logger:
    - Escribe logs de nivel DEBUG y superiores en un archivo llamado 'backend_todo_.log'.
    - Escribe logs de nivel INFO y superiores en la consola (stderr).
    - Utiliza un formato detallado para los logs del archivo.
    - Utiliza un formato más simple para los logs de la consola.
    """
    # 1. Crea el objeto logger principal
    logger = logging.getLogger('backend_logger')
    logger.setLevel(logging.DEBUG)  # Nivel mínimo de log para el logger principal

    # Asegura que el logger no propague logs a handlers del logger raíz
    logger.propagate = False

    # 2. Crea un formatter para el archivo de log (formato detallado)
    file_formatter = logging.Formatter(
        '[%(asctime)s] - [%(levelname)s] - [%(name)s] - [%(funcName)s:%(lineno)d] - %(message)s'
    )

    # 3. Crea un formatter para la consola (formato simple)
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # 4. Crea un handler para escribir en un archivo (FileHandler)
    file_handler = logging.FileHandler('backend.log')
    file_handler.setLevel(logging.DEBUG)  # Nivel de log para el archivo
    file_handler.setFormatter(file_formatter)

    # 5. Crea un handler para escribir en la consola (StreamHandler)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)  # Nivel de log para la consola
    console_handler.setFormatter(console_formatter)

    # 6. Agrega los handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# --- Uso del logger ---
logger = setup_logging()
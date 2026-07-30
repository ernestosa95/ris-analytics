import eel
import os
import sys
from tkinter import Tk, filedialog

# Importamos tu motor de PDF (asegúrate de que el archivo se llame pdf_engine.py)
from pdf_engine import generar_reporte_ris_corporativo

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE RUTAS (Vital para cuando compiles a .exe)
# ---------------------------------------------------------
def get_web_dir():
    """Obtiene la ruta correcta de la carpeta 'web' ya sea ejecutando en Python o compilado en .exe"""
    if hasattr(sys, '_MEIPASS'):
        # Si está ejecutándose como un ejecutable compilado con PyInstaller
        return os.path.join(sys._MEIPASS, 'web')
    # Si está ejecutándose normalmente desde el script .py
    return 'web'

# Inicializamos Eel apuntando a la carpeta de nuestro frontend
eel.init(get_web_dir())

# ---------------------------------------------------------
# 2. FUNCIONES EXPUESTAS AL FRONTEND (JavaScript)
# ---------------------------------------------------------
@eel.expose
def generar_pdf_local(payload):
    """
    Recibe los datos del frontend, abre el cuadro de diálogo para guardar 
    y ejecuta el motor de PDF.
    """
    try:
        # A. Inicializamos Tkinter (de forma oculta) para el cuadro de diálogo
        root = Tk()
        root.withdraw() # Oculta la ventana principal gris de Tkinter
        root.attributes('-topmost', True) # Fuerza que el cuadro de diálogo aparezca por encima de la app

        # B. Armamos un nombre de archivo sugerido y limpio
        hospital_name = payload.get('hospital_name', 'Institucion')
        # Limpiamos caracteres raros para el nombre del archivo
        nombre_limpio = "".join(c if c.isalnum() else "_" for c in hospital_name)
        nombre_sugerido = f"Reporte_RIS_{nombre_limpio}.pdf"

        # C. Abrimos el cuadro "Guardar Como..."
        ruta_salida = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Documentos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            initialfile=nombre_sugerido,
            title="Guardar Informe RIS Analytics"
        )

        root.destroy() # Destruimos la instancia de Tkinter para liberar memoria

        # D. Verificamos si el usuario le dio a "Cancelar"
        if not ruta_salida:
            return {"status": "cancelado", "mensaje": "Operación cancelada por el usuario"}

        # E. Ejecutamos tu motor de PDF enviándole los datos y la ruta elegida
        generar_reporte_ris_corporativo(payload, ruta_salida)

        # F. Si todo sale bien, respondemos con éxito a JavaScript
        return {"status": "exito", "ruta": ruta_salida}

    except Exception as e:
        # Si algo falla en Python o en la generación del PDF, se lo enviamos a la consola de JS
        error_msg = str(e)
        print(f"Error al generar PDF: {error_msg}")
        return {"status": "error", "mensaje": error_msg}

# ---------------------------------------------------------
# 3. ARRANQUE DE LA APLICACIÓN
# ---------------------------------------------------------
if __name__ == '__main__':
    print("Iniciando TecnoMonitor - RIS Analytics...")
    
    # Iniciamos la app (abre una ventana del sistema simulando un programa nativo)
    try:
        eel.start(
            'index.html', 
            size=(1300, 850),          # Tamaño inicial de la ventana
            mode='chrome',             # Usa el motor de Chrome/Edge instalado en la PC
            port=0                     # Puerto aleatorio para evitar conflictos con otras apps
        )
    except (SystemExit, KeyboardInterrupt):
        print("Aplicación cerrada correctamente.")
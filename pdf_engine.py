import os
import sys
import io
import numpy as np
from datetime import datetime
import matplotlib
matplotlib.use('Agg') # Fundamental para que no intente abrir ventanas de gráficos
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.utils import ImageReader
import textwrap

# ==========================================
# RUTAS DE RECURSOS (Imágenes)
# ==========================================
def get_asset_path(filename):
    """Devuelve la ruta absoluta de la imagen, compatible con el .exe de PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'web', filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', filename)


# ==========================================
# COMPONENTES CORPORATIVOS (Tecnoimagen)
# ==========================================
def crear_portada(c, ancho, alto, tipo, hospital_id, hospital_nombre, fecha_desde, fecha_hasta):
    """Genera la portada institucional con ondas azules e imagen de fondo"""
    def formatear_fecha(fecha_str):
        if not fecha_str: return ""
        try:
            return datetime.strptime(str(fecha_str)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            return str(fecha_str)

    texto_periodo = f"{formatear_fecha(fecha_desde)} al {formatear_fecha(fecha_hasta)}" if fecha_desde and fecha_hasta else "Periodo no especificado"

    img_name = "imagen_informe_estadisticas.png"
    titulo_principal = "INFORME DE"
    titulo_secundario = "ESTADÍSTICAS RIS"

    img_path = get_asset_path(img_name)

    # Imagen de fondo
    try:
        if os.path.exists(img_path):
            c.drawImage(img_path, 0, 0, width=ancho, height=alto * 0.8, preserveAspectRatio=False)
        else:
            c.setFillColorRGB(0.9, 0.9, 0.9)
            c.rect(0, 0, ancho, alto * 0.8, fill=1, stroke=0)
    except Exception:
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(0, 0, ancho, alto * 0.8, fill=1, stroke=0)

    # Curva Blanca
    c.setFillColorRGB(1, 1, 1)
    path_blanco = c.beginPath()
    path_blanco.moveTo(0, alto)
    path_blanco.lineTo(ancho, alto)
    path_blanco.lineTo(ancho, alto * 0.65)
    path_blanco.curveTo(ancho * 0.6, alto * 0.35, ancho * 0.2, alto * 0.45, 0, alto * 0.5)
    path_blanco.close()
    c.drawPath(path_blanco, fill=1, stroke=0)

    # Ondas Azules Inferiores
    c.setFillColorRGB(0.0, 0.45, 0.70)
    path_azul1 = c.beginPath()
    path_azul1.moveTo(ancho, 0)
    path_azul1.lineTo(0, 0)
    path_azul1.lineTo(0, alto * 0.15)
    path_azul1.curveTo(ancho * 0.4, alto * 0.05, ancho * 0.7, alto * 0.35, ancho, alto * 0.6)
    path_azul1.close()
    c.drawPath(path_azul1, fill=1, stroke=0)

    c.setFillColorRGB(0.0, 0.65, 0.85)
    path_azul2 = c.beginPath()
    path_azul2.moveTo(ancho, 0)
    path_azul2.lineTo(ancho * 0.4, 0)
    path_azul2.curveTo(ancho * 0.7, alto * 0.1, ancho * 0.85, alto * 0.25, ancho, alto * 0.45)
    path_azul2.close()
    c.drawPath(path_azul2, fill=1, stroke=0)

    # Textos
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(ancho - 140, alto - 50, "TECNOIMAGEN")

    c.setFont("Helvetica", 28)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(50, alto - 120, titulo_principal)
    
    c.setFont("Helvetica-Bold", 34)
    c.setFillColorRGB(0.0, 0.45, 0.70)
    c.drawString(50, alto - 155, titulo_secundario)
    
    c.setFont("Helvetica", 16)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(50, alto - 185, texto_periodo)

    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(50, alto - 290, f"HOSPITAL: {hospital_id}")
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(50, alto - 305, hospital_nombre[:60].upper())

    c.showPage()

def crear_encabezado(c, ancho, alto, titulo_hoja, hospital_id, hospital_nombre, num_pagina):
    """Genera una cabecera azul fluida para las páginas internas"""
    c.setFillColorRGB(0.0, 0.65, 0.85)
    path1 = c.beginPath()
    path1.moveTo(0, alto)
    path1.lineTo(ancho, alto)
    path1.lineTo(ancho, alto - 35)
    path1.curveTo(ancho * 0.6, alto - 45, ancho * 0.4, alto - 15, 0, alto - 25)
    path1.close()
    c.drawPath(path1, fill=1, stroke=0)

    c.setFillColorRGB(0.0, 0.45, 0.70)
    path2 = c.beginPath()
    path2.moveTo(0, alto)
    path2.lineTo(ancho, alto)
    path2.lineTo(ancho, alto - 40)
    path2.curveTo(ancho * 0.7, alto - 15, ancho * 0.3, alto - 50, 0, alto - 40)
    path2.close()
    c.drawPath(path2, fill=1, stroke=0)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, alto - 22, f"HOSPITAL: {hospital_id}")
    c.drawString(ancho - 130, alto - 22, "TECNOIMAGEN")

    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica", 10)
    c.drawString(40, alto - 60, hospital_nombre[:70].upper())

    c.setFillColorRGB(0.17, 0.24, 0.31)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, alto - 80, titulo_hoja.upper())

    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.setLineWidth(1)
    c.line(40, alto - 95, ancho - 40, alto - 95)

    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica", 9)
    c.drawString(40, 30, "Monitoreo Inteligente de Infraestructura")
    c.drawString(ancho - 80, 30, f"Página {num_pagina}")

    return alto - 125


# ==========================================
# MOTORES GRÁFICOS (Matplotlib)
# ==========================================
def _wrap_label(s, width=16, max_lines=3):
    """Parte un texto largo en varias líneas; si excede max_lines, corta con …"""
    lineas = textwrap.wrap(str(s), width=width) or ['']
    if len(lineas) > max_lines:
        lineas = lineas[:max_lines]
        lineas[-1] = lineas[-1][:width-1].rstrip() + '…'
    return '\n'.join(lineas)

def _fmt_miles(x, pos=None):
    return f"{int(abs(x)):,}".replace(',', '.')

def _top_categorias(totales, max_n, otros='OTROS'):
    """Devuelve las claves de las max_n categorías con más volumen (orden descendente)
    y la lista de las que se agrupan en 'OTROS'."""
    orden = sorted(totales, key=lambda k: totales[k], reverse=True)
    if len(orden) <= max_n:
        return orden, []
    return orden[:max_n - 1], orden[max_n - 1:]

def _estilo_ejes(ax, n_cats, labels, eje_valores='y'):
    """Ejes legibles: etiquetas envueltas/rotadas según cantidad, separador de miles y grilla suave."""
    if n_cats <= 4:
        wrapped = [_wrap_label(l, width=18, max_lines=3) for l in labels]
        ax.set_xticks(range(n_cats)); ax.set_xticklabels(wrapped, rotation=0, ha='center', fontsize=7)
    elif n_cats <= 9:
        wrapped = [_wrap_label(l, width=12, max_lines=3) for l in labels]
        ax.set_xticks(range(n_cats)); ax.set_xticklabels(wrapped, rotation=0, ha='center', fontsize=6.5)
    else:
        wrapped = [_wrap_label(l, width=24, max_lines=2) for l in labels]
        ax.set_xticks(range(n_cats)); ax.set_xticklabels(wrapped, rotation=35, ha='right', rotation_mode='anchor', fontsize=6.5)
    eje = ax.yaxis if eje_valores == 'y' else ax.xaxis
    eje.set_major_formatter(ticker.FuncFormatter(_fmt_miles))
    eje.set_major_locator(ticker.MaxNLocator(nbins=6, integer=True))
    ax.tick_params(axis='y', labelsize=7)
    ax.grid(axis=eje_valores, color='#e5e5e5', linewidth=0.6)
    ax.set_axisbelow(True)
    for lado in ('top', 'right'):
        ax.spines[lado].set_visible(False)
    ax.set_xlim(-0.6, n_cats - 0.4)

def _a_buffer(fig):
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    plt.close(fig)
    return buf

def generar_grafico_barras_memoria(datos_dict, titulo, color_barra='#2c3e50', ordenar=True):
    if not datos_dict: return None
    items = sorted(datos_dict.items(), key=lambda x: x[1], reverse=True)[:12] if ordenar else list(datos_dict.items())
    labels = [k for k, v in items]
    sizes = [v for k, v in items]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    barras = ax.bar(range(len(labels)), sizes, color=color_barra, width=0.65)
    ax.bar_label(barras, labels=[_fmt_miles(v) for v in sizes], fontsize=6.5, padding=2, color='#444')
    ax.margins(y=0.12)
    _estilo_ejes(ax, len(labels), labels)
    return _a_buffer(fig)

def generar_grafico_torta_sexo(datos_dict):
    if not datos_dict: return None
    fig, ax = plt.subplots(figsize=(4, 3))
    labels, sizes = list(datos_dict.keys()), list(datos_dict.values())
    colores = ['#3399ff' if str(l).upper().startswith('M') else '#ff66b2' if str(l).upper().startswith('F') else '#bdc3c7' for l in labels]
    ax.pie(sizes, labels=labels, colors=colores, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.4, edgecolor='white'))
    return _a_buffer(fig)

def generar_grafico_piramide_memoria(datos_piramide):
    labels = datos_piramide.get('labels', [])
    M, F = datos_piramide.get('M', []), datos_piramide.get('F', [])
    if not labels or (sum(M) == 0 and sum(F) == 0): return None
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.barh(y, [-m for m in M], color='#3399ff', label='Masculino', edgecolor='white')
    ax.barh(y, F, color='#ff66b2', label='Femenino', edgecolor='white')
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=7)
    lim = max(max(M), max(F)) * 1.1
    ax.set_xlim(-lim, lim)
    ax.axvline(0, color='#999', linewidth=0.6)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(_fmt_miles))
    ax.tick_params(axis='x', labelsize=7)
    ax.grid(axis='x', color='#e5e5e5', linewidth=0.6); ax.set_axisbelow(True)
    for lado in ('top', 'right'): ax.spines[lado].set_visible(False)
    ax.legend(loc='upper right', frameon=False, fontsize=7)
    return _a_buffer(fig)

def generar_grafico_apilado_sexo_tipo(datos_dict):
    if not datos_dict: return None
    totales = {k: v.get('M', 0) + v.get('F', 0) for k, v in datos_dict.items()}
    if sum(totales.values()) == 0: return None
    top, resto = _top_categorias(totales, 10)
    labels = top + (['OTROS'] if resto else [])
    M = [datos_dict[l].get('M', 0) for l in top] + ([sum(datos_dict[l].get('M', 0) for l in resto)] if resto else [])
    F = [datos_dict[l].get('F', 0) for l in top] + ([sum(datos_dict[l].get('F', 0) for l in resto)] if resto else [])
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(x, M, 0.6, label='Masculino', color='#3399ff', edgecolor='white')
    ax.bar(x, F, 0.6, bottom=M, label='Femenino', color='#ff66b2', edgecolor='white')
    _estilo_ejes(ax, len(labels), labels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=7)
    return _a_buffer(fig)

def generar_mapa_calor(datos_dict):
    if not datos_dict: return None
    tot_origen = {o: sum(v.values()) for o, v in datos_dict.items()}
    tot_tipo = {}
    for v in datos_dict.values():
        for t, n in v.items():
            tot_tipo[t] = tot_tipo.get(t, 0) + n
    if not tot_origen or not tot_tipo: return None

    origenes, origenes_resto = _top_categorias(tot_origen, 10)
    tipos, tipos_resto = _top_categorias(tot_tipo, 10)
    filas = origenes + (['OTROS'] if origenes_resto else [])
    cols = tipos + (['OTROS'] if tipos_resto else [])

    def valor(o, t):
        os_ = origenes_resto if o == 'OTROS' else [o]
        ts_ = tipos_resto if t == 'OTROS' else [t]
        return sum(datos_dict.get(oo, {}).get(tt, 0) for oo in os_ for tt in ts_)

    matrix = np.array([[valor(o, t) for t in cols] for o in filas])
    fig, ax = plt.subplots(figsize=(8, max(3, 0.45 * len(filas) + 1.8)))
    ax.imshow(matrix, cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([_wrap_label(t, width=14, max_lines=2) for t in cols],
                       rotation=0 if len(cols) <= 6 else 35,
                       ha='center' if len(cols) <= 6 else 'right', rotation_mode='anchor', fontsize=6.5)
    ax.set_yticks(range(len(filas)))
    ax.set_yticklabels([_wrap_label(o, width=24, max_lines=1) for o in filas], fontsize=6.5)
    ax.tick_params(length=0)
    for lado in ax.spines.values(): lado.set_visible(False)
    vmax = matrix.max() or 1
    for i in range(len(filas)):
        for j in range(len(cols)):
            if matrix[i, j] > 0:
                ax.text(j, i, _fmt_miles(matrix[i, j]), ha="center", va="center",
                        color="white" if matrix[i, j] > vmax / 2 else "#222", fontsize=6.5)
    return _a_buffer(fig)


# ==========================================
# GENERADOR PRINCIPAL DEL REPORTE
# ==========================================
def generar_reporte_ris_corporativo(datos: dict, ruta_salida: str):
    """
    Genera el informe PDF completo de RIS Analytics.
    Integra Portada, Tablero de KPIs, gráficos dinámicos y paginación automática.
    """
    c = canvas.Canvas(ruta_salida, pagesize=A4)
    ancho, alto = A4

    h_nombre = datos.get('hospital_name', 'Institución No Especificada')
    h_id = datos.get('hospital_id', 'S/D')
    f_desde, f_hasta = datos.get('fecha_desde', ''), datos.get('fecha_hasta', '')

    # PÁGINA 1: PORTADA
    crear_portada(c, ancho, alto, 'estadisticas', h_id, h_nombre, f_desde, f_hasta)

    # PÁGINA 2: COMIENZO DE ANÁLISIS
    pagina_actual = 2
    pos_y = crear_encabezado(c, ancho, alto, "ANÁLISIS DE DEMANDA RIS", h_id, h_nombre, pagina_actual)
    
    # Texto Auditoría
    pos_y -= 25
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(40, pos_y, f"Informe generado en base a la auditoría de {datos.get('kpi_total_registros', 0):,} registros analizados.")

    # TABLERO DE KPIs (4 Cajas)
    pos_y -= 85
    kpis = [
        ("TOTAL ESTUDIOS", f"{datos.get('kpi_total_estudios', 0):,}"), 
        ("PACIENTES ÚNICOS", f"{datos['kpi_pacientes']:,}" if datos.get('kpi_pacientes') is not None else "—"),
        ("EDAD PROMEDIO", f"{datos.get('kpi_edad_promedio', 0):.1f}" if datos.get('kpi_edad_promedio') else "—"),
        ("ORÍGENES", str(datos['kpi_origenes_distintos']) if datos.get('kpi_origenes_distintos') is not None else "—")
    ]

    for i, (label, val) in enumerate(kpis):
        x = 45 + i * 125
        # Sombra
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.roundRect(x+2, pos_y-2, 115, 65, 6, fill=1, stroke=0)
        # Fondo Azul
        c.setFillColor(colors.HexColor('#004c99'))
        c.roundRect(x, pos_y, 115, 65, 6, fill=1, stroke=0)
        # Valores
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(x+57.5, pos_y+32, str(val).replace(',', '.'))
        c.setFillColorRGB(0.8, 0.9, 1)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(x+57.5, pos_y+12, label)

    pos_y -= 50

    # Lógica de Paginación Dinámica
    def check_p(py, pa, alto_necesario=210):
        if py - alto_necesario < 50:
            c.showPage()
            pa += 1
            return crear_encabezado(c, ancho, alto, "ANÁLISIS DE DEMANDA (CONT.)", h_id, h_nombre, pa) - 30, pa
        return py, pa

    # RENDERIZADO DEFENSIVO DE GRÁFICOS
    secciones = [
        ('datos_estado_informes', "ESTUDIOS TOTALES VS. INFORMADOS", None, generar_grafico_agrupado_estado),
        ('datos_tipo', "ESTUDIOS POR TIPO (MODALIDAD)", "#1abc9c", generar_grafico_barras_memoria),
        ('datos_obrasocial_cruce', "MODALIDADES POR OBRA SOCIAL (TOP 10)", None, generar_grafico_apilado_obrasocial),
        ('datos_obrasocial', "DISTRIBUCIÓN POR OBRA SOCIAL", "#9b59b6", generar_grafico_barras_memoria),
        ('datos_practica', "TOP PRÁCTICAS REALIZADAS", "#e67e22", generar_grafico_barras_memoria),
        ('datos_sexo', "DISTRIBUCIÓN POR SEXO", None, generar_grafico_torta_sexo),
        ('datos_piramide', "PIRÁMIDE POBLACIONAL (EDAD Y SEXO)", None, generar_grafico_piramide_memoria),
        ('datos_sexo_tipo', "SEXO POR TIPO DE ESTUDIO", None, generar_grafico_apilado_sexo_tipo),
        ('datos_mapa_calor', "MAPA DE CALOR: ORIGEN VS MODALIDAD", None, generar_mapa_calor),
        ('datos_edad', "DISTRIBUCIÓN POR RANGO DE EDAD", "#d35400", generar_grafico_barras_memoria),
        ('datos_equipos', "VOLUMEN DE ESTUDIOS POR EQUIPO", "#3399ff", generar_grafico_barras_memoria),
        ('datos_origen', "DISTRIBUCIÓN POR ORIGEN", "#004c99", generar_grafico_barras_memoria)
    ]

    for key, title, color, func in secciones:
        if not datos.get(key): continue
        if key == 'datos_edad':  # rangos de edad: respetar el orden natural, no por volumen
            img = generar_grafico_barras_memoria(datos[key], "", color, ordenar=False)
        else:
            img = func(datos[key], "", color) if color else func(datos[key])
        if not img: continue  # sin datos útiles: no se dibuja ni el título

        h_img = 250 if key == 'datos_mapa_calor' else 200 # El mapa necesita más altura
        pos_y, pagina_actual = check_p(pos_y, pagina_actual, h_img + 10)
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(0.17, 0.24, 0.31)
        c.drawString(40, pos_y, title)
        pos_y -= 10

        c.drawImage(ImageReader(img), 40, pos_y - h_img, width=ancho-80, height=h_img, mask='auto', preserveAspectRatio=True)
        pos_y -= (h_img + 40)

    c.save()

def generar_grafico_agrupado_estado(datos_dict):
    """Genera el gráfico de barras agrupadas: Totales vs Informados"""
    if not datos_dict: return None
    totales_d = {k: v.get('Totales', 0) for k, v in datos_dict.items()}
    top, resto = _top_categorias(totales_d, 10)
    labels = top + (['OTROS'] if resto else [])
    totales = [datos_dict[l].get('Totales', 0) for l in top] + ([sum(datos_dict[l].get('Totales', 0) for l in resto)] if resto else [])
    informados = [datos_dict[l].get('Informados', 0) for l in top] + ([sum(datos_dict[l].get('Informados', 0) for l in resto)] if resto else [])

    x = np.arange(len(labels))
    width = 0.38
    fig, ax = plt.subplots(figsize=(8, 4))
    b1 = ax.bar(x - width/2, totales, width, label='Estudios Totales', color='#3498db', edgecolor='white')
    b2 = ax.bar(x + width/2, informados, width, label='Informados (Con Médico)', color='#2ecc71', edgecolor='white')
    ax.bar_label(b1, labels=[_fmt_miles(v) for v in totales], fontsize=6, padding=2, color='#444')
    ax.bar_label(b2, labels=[_fmt_miles(v) for v in informados], fontsize=6, padding=2, color='#444')
    ax.margins(y=0.12)
    _estilo_ejes(ax, len(labels), labels)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=7)
    return _a_buffer(fig)

def generar_grafico_apilado_obrasocial(datos_dict):
    """Genera gráfico apilado para Obras Sociales vs Modalidades"""
    if not datos_dict: return None
    PALETTE = ['#3498db','#e67e22','#2ecc71','#e74c3c','#9b59b6','#1abc9c','#f39c12','#27ae60','#c0392b','#2980b9']

    obras_sociales = list(datos_dict.keys())
    tot_mod = {}
    for mods in datos_dict.values():
        for mod, n in mods.items():
            tot_mod[mod] = tot_mod.get(mod, 0) + n
    top, resto = _top_categorias(tot_mod, 10)
    modalidades = top + (['OTROS'] if resto else [])

    x = np.arange(len(modalidades))
    fig, ax = plt.subplots(figsize=(8, 5))
    bottoms = np.zeros(len(modalidades))

    for i, os_name in enumerate(obras_sociales):
        d = datos_dict[os_name]
        valores = [d.get(mod, 0) for mod in top] + ([sum(d.get(m, 0) for m in resto)] if resto else [])
        color = PALETTE[i % len(PALETTE)] if os_name != 'OTROS' else '#bdc3c7'
        nombre_legenda = os_name[:15] + '..' if len(os_name) > 15 else os_name
        ax.bar(x, valores, 0.6, bottom=bottoms, label=nombre_legenda, color=color, edgecolor='white')
        bottoms += np.array(valores)

    _estilo_ejes(ax, len(modalidades), modalidades)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=4, fontsize=6.5, frameon=False)
    return _a_buffer(fig)

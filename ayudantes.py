import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

# FUNCIÓN PARA GENERAR EL GRÁFICO DE COMPATIBILIDAD
def generar_grafico_compatibilidad(compatibilidad):
    compatibilidad = compatibilidad / 100  # Asegúrate de que esté en escala de 0 a 1 para porcentajes

    # Estilo ultra minimalista y moderno
    sns.set_theme(style="white", rc={
        "axes.edgecolor": "0.92",
        "axes.linewidth": 0.5,
        "axes.grid": False,
        "xtick.bottom": False,
        "ytick.left": False,
        "font.family": "sans-serif",
        "font.sans-serif": "Inter, Segoe UI, Roboto, Arial, sans-serif",
        "font.size": 11  # Tamaño original
    })
    fig, ax = plt.subplots(figsize=(6.5, 3.8))

    # Todas las barras y porcentajes en azul #3a86ff
    bar_color = "#3a86ff"
    bars = sns.barplot(
        x=compatibilidad.index,
        y=compatibilidad.values,
        ax=ax,
        color=bar_color,
        edgecolor=None
    )

    # Bordes y fondo ultra limpios
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(left=False, bottom=False)
    ax.set_axisbelow(False)
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Etiquetas minimalistas y modernas
    ax.set_xlabel('Inquilino', fontsize=12, fontweight='semibold', labelpad=10, color='#222')
    ax.set_ylabel('Similitud (%)', fontsize=12, fontweight='semibold', labelpad=10, color='#222')
    # Eje X
    xticks = ax.get_xticks()
    ax.set_xticks(xticks)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=18, ha='right', fontsize=11, color='#444')
    # Eje Y
    yticks = ax.get_yticks()
    ax.set_yticks(yticks)
    ax.set_yticklabels(['{:.0f}%'.format(y * 100) for y in yticks], fontsize=10, color='#888')

    # Etiquetas sobre las barras, en negro
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(
            '{:.1f}%'.format(height * 100),
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='bottom',
            xytext=(0, 5),
            textcoords='offset points',
            fontsize=10,
            fontweight='semibold',
            color='black'
        )

    # Espacio extra para look aireado
    plt.tight_layout(pad=1.5)

    return(fig)


# FUNCIÓN PARA GENERAR LA TABLA DE COMPAÑEROS
def generar_tabla_compatibilidad(resultado):
    resultado_0_with_index = resultado[0].reset_index()
    resultado_0_with_index.rename(columns={'index': 'ATRIBUTO'}, inplace=True)

    # Encabezado azul moderno, celdas glassmorphism
    header_color = '#3a86ff'  # Azul de la paleta de la gráfica
    cell_color1 = 'rgba(245,250,255,0.85)'
    cell_color2 = 'rgba(230,240,255,0.85)'
    border_color = 'rgba(180,200,255,0.25)'

    fig_table = go.Figure(data=[go.Table(
        columnwidth=[32] + [15] * (len(resultado_0_with_index.columns) - 1),
        header=dict(
            values=[f"<b>{col}</b>" for col in resultado_0_with_index.columns],
            fill_color=header_color,
            font=dict(color='white', size=16, family="Inter, Segoe UI, Roboto, Arial, sans-serif"),
            align='center',
            line_color=border_color,
            height=32
        ),
        cells=dict(
            values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns],
            fill_color=[[cell_color1, cell_color2] * (len(resultado_0_with_index) // 2 + 1)],
            font=dict(color='#222', size=15, family="Inter, Segoe UI, Roboto, Arial, sans-serif"),
            align='center',
            line_color=border_color,
            height=28
        )
    )])

    fig_table.update_layout(
        template=None,
        width=770, height=320,
        margin=dict(l=0, r=0, t=12, b=0),
        paper_bgcolor='rgba(255,255,255,0.7)'
    )

    return(fig_table)


#FUNCIÓN PARA GENERAR LA LISTA DE INQUILINOS SEMILLA
def obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn):
    # Crea una lista con los identificadores de inquilinos ingresados y los convierte a enteros
    id_inquilinos = []
    for inquilino in [inquilino1, inquilino2, inquilino3]:
        try:
            if inquilino:  # Si hay algún texto en el input
                id_inquilinos.append(int(inquilino))  # Convierte a entero y agrega a la lista
        except ValueError:
            st.error(f"El identificador del inquilino '{inquilino}' no es un número válido.")
            id_inquilinos = []  # Vaciar la lista si hay un error
            break  # Salir del bucle

    return(id_inquilinos)


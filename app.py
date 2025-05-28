import streamlit as st 
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

# --- Configuración de la página ---
st.set_page_config(
    page_title="Roommate Finder",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Título Principal ---
st.title("🏠 Encuentra a tu Compañero de Piso Ideal")
st.subheader("¡Simplificando la búsqueda de convivencia compatible!")
st.markdown("---")

# --- Barra lateral ---
with st.sidebar:
    st.header("¿Quiénes ya están en el piso?")
    st.info("Ingresa los nombres de los inquilinos actuales.")

    inquilino1 = st.text_input("Inquilino 1", key="inq1_input")
    inquilino2 = st.text_input("Inquilino 2", key="inq2_input")
    inquilino3 = st.text_input("Inquilino 3", key="inq3_input")

    st.markdown("---")

    st.header("¿Cuántos nuevos compañeros buscas?")
    num_compañeros = st.slider(
        "Selecciona la cantidad de nuevos compañeros a buscar:",
        min_value=1,
        max_value=10,
        value=3,
        key="num_comp_slider"
    )

    if st.button('🚀 BUSCAR NUEVOS COMPAÑEROS', use_container_width=True):
        with st.spinner('Buscando los compañeros más compatibles...'):
            try:
                topn = int(num_compañeros)
            except ValueError:
                st.error("Por favor, ingresa un número válido.")
                topn = None

            if topn is not None:
                id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn)

                if id_inquilinos:
                    resultado = inquilinos_compatibles(id_inquilinos, topn)
                else:
                    st.warning("Asegúrate de ingresar al menos un nombre válido.")

# --- Resultados ---
resultado = locals().get("resultado", None)

if isinstance(resultado, str):
    st.error(resultado)
elif resultado is not None:
    st.success("¡Hemos encontrado posibles compañeros de piso!")

    tab1, tab2 = st.tabs(["📊 Nivel de Compatibilidad", "📋 Comparativa Detallada"])

    with tab1:
        st.subheader("Nivel de Compatibilidad de Cada Nuevo Candidato")
        st.markdown("Este gráfico muestra qué tan bien cada candidato se alinea con los inquilinos existentes.")
        fig_grafico = generar_grafico_compatibilidad(resultado[1])
        st.pyplot(fig_grafico)

    with tab2:
        st.subheader("Comparativa Detallada entre Candidatos")
        st.markdown("Explora las características clave de cada candidato y cómo se comparan.")
        fig_tabla = generar_tabla_compatibilidad(resultado)
        st.plotly_chart(fig_tabla, use_container_width=True)

else:
    st.info("Ingresa los detalles en la barra lateral y haz clic en 'BUSCAR NUEVOS COMPAÑEROS' para comenzar.")

# --- Pie de página ---
st.markdown("---")
st.markdown(
    "<footer><p style='text-align: center;'>Aplicación desarrollada para ayudarte a encontrar el compañero de piso perfecto.</p></footer>",
    unsafe_allow_html=True
)

import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

# --- Page Configuration ---
st.set_page_config(
    page_title="Roommate Finder",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a modern look ---
st.markdown(
    """
    <style>
    /* General body styling */
    body, .stApp {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        background-color: #f0f2f6; /* Light gray background */
        color: #333333;
        font-size: 18px !important; /* Tamaño base adecuado */
        line-height: 1.6;
    }

    /* Header styling */
    .stApp > header {
        background-color: #ffffff; /* White header background */
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 10px 20px;
        border-bottom: 1px solid #e0e0e0;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }

    /* Title and text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #004d99; /* Darker blue for headings */
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2rem !important; }
    h3 { font-size: 1.5rem !important; }
    h4, h5, h6 { font-size: 1.2rem !important; }

    .stMarkdown, .stText, .stDataFrame, .stTable, .stAlert, .stMetricLabel, .stMetricValue {
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
    }

    /* Sidebar styling */
    .stSidebar {
        background-color: #ffffff; /* White sidebar background */
        padding: 30px 20px;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
    }

    .stSidebar .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #cccccc;
        padding: 10px;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
    }

    /* Button styling */
    .stButton > button {
        background-color: #007bff; /* Bright blue button */
        color: white !important;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s, color 0.3s, border-color 0.3s;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
        border: 2px solid #007bff !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:active {
        color: #fff !important;
        border: 2px solid #fff !important;
        background-color: #007bff !important;
        box-shadow: 0 0 0 2px #fff !important;
        outline: none !important;
    }

    /* Expander styling (if used) */
    .streamlit-expanderHeader {
        background-color: #e6f2ff; /* Light blue background for expander headers */
        color: #004d99;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
    }

    /* Info/Error messages */
    .stAlert {
        border-radius: 8px;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
    }

    /* Metric boxes (if used) */
    [data-testid="stMetricValue"] {
        font-size: 3rem;
        color: #007bff;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    }
    [data-testid="stMetricLabel"] {
        color: #555555;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
    }

    /* Adjust main content area padding */
    .main .block-container {
        padding-top: 30px;
        padding-bottom: 30px;
        padding-left: 50px;
        padding-right: 50px;
        font-family: 'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

resultado = None

# --- Header Section with Title Only ---
st.markdown("<h1>Encuentra a tu Compañero de Piso Ideal</h1>", unsafe_allow_html=True)
st.markdown("### ¡Simplificando la búsqueda de convivencia compatible!", unsafe_allow_html=True)

st.markdown("---") # Línea horizontal para separación


# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("¿Quiénes ya están en el piso?")
    st.info("Ingresa los nombres de los inquilinos actuales.")

    inquilino1 = st.text_input("Inquilino 1", key="inq1_input")
    inquilino2 = st.text_input("Inquilino 2", key="inq2_input")
    inquilino3 = st.text_input("Inquilino 3", key="inq3_input")

    st.markdown("---") # Separator in sidebar

    st.header("¿Cuántos nuevos compañeros buscas?")
    num_compañeros = st.slider(
        "Selecciona la cantidad de nuevos compañeros a buscar:",
        min_value=1,
        max_value=10, # Adjust max as needed
        value=3,
        key="num_comp_slider"
    )

    st.markdown(f'<div style="margin-top: 30px;"></div>', unsafe_allow_html=True) # Space

    if st.button('🚀 BUSCAR NUEVOS COMPAÑEROS', use_container_width=True):
        with st.spinner('Buscando los compañeros más compatibles...'):
            try:
                topn = int(num_compañeros)
            except ValueError:
                st.error("Por favor, ingresa un número válido para el número de compañeros.")
                topn = None

            if topn is not None:
                id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn)

                if id_inquilinos:
                    resultado = inquilinos_compatibles(id_inquilinos, topn)
                else:
                    st.warning("Asegúrate de ingresar al menos un nombre de inquilino existente.")

# --- Main Content Area ---
st.markdown(f'<div style="margin-top: 40px;"></div>', unsafe_allow_html=True)

# Display results
if isinstance(resultado, str):
    st.error(resultado) # Display error messages from the backend logic
elif resultado is not None:
    st.success("¡Hemos encontrado posibles compañeros de piso!")

    # Using st.tabs for better organization if you have multiple result views
    tab1, tab2 = st.tabs(["📊 Nivel de Compatibilidad", "📋 Comparativa Detallada"])

    with tab1:
        st.subheader("Nivel de Compatibilidad de Cada Nuevo Candidato")
        st.markdown("Este gráfico muestra qué tan bien cada candidato se alinea con los inquilinos existentes.")
        fig_grafico = generar_grafico_compatibilidad(resultado[1])
        st.pyplot(fig_grafico)
        # fig_grafico = generar_grafico_compatibilidad(resultado[1])
        # st.plotly_chart(fig_grafico, use_container_width=True)

    with tab2:
        st.subheader("Comparativa Detallada entre Candidatos")
        st.markdown("Explora las características clave de cada candidato y cómo se comparan.")
        fig_tabla = generar_tabla_compatibilidad(resultado)
        st.plotly_chart(fig_tabla, use_container_width=True)

else:
    st.info("Ingresa los detalles en la barra lateral y haz clic en 'BUSCAR NUEVOS COMPAÑEROS' para comenzar.")

st.markdown("---")
st.markdown("<footer><p style='text-align: center; color: #888;'>Aplicación desarrollada para ayudarte a encontrar el compañero de piso perfecto.</p></footer>", unsafe_allow_html=True)
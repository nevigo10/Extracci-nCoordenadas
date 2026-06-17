import streamlit as st
import pdfplumber
import pandas as pd
import re

# Configuración de la página
st.set_page_config(
    page_title="PDF Coordinate Extractor",
    page_icon="🌎",
    layout="wide"
)

# Título
st.title("🌎 PDF Coordinate Extractor")
st.write("Extrae coordenadas UTM desde documentos PDF y exporta resultados.")

# Cargar PDF
archivo = st.file_uploader(
    "Seleccione un archivo PDF",
    type=["pdf"]
)

if archivo:

    texto = ""

    with pdfplumber.open(archivo) as pdf:
        for pagina in pdf.pages:

            contenido = pagina.extract_text()

            if contenido:
                texto += contenido + "\n"

    st.subheader("Texto extraído")

    st.text_area(
        "",
        texto,
        height=250
    )

    # Buscar coordenadas UTM
    patron_utm = r'(\d{6,8}\.\d+)\s+(\d{6,8}\.\d+)'

    coordenadas = re.findall(
        patron_utm,
        texto
    )

    if coordenadas:

        df = pd.DataFrame(
            coordenadas,
            columns=["Y", "X"]
        )

        st.subheader("Coordenadas encontradas")

        st.dataframe(df)

        # Guardar CSV en memoria
        csv = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="coordenadas_extraidas.csv",
            mime="text/csv"
        )

    else:

        st.warning(
            "No se encontraron coordenadas con el patrón configurado."
        )

# Créditos
st.markdown("---")
st.markdown(
    """
    **Elaborado por:**  
    **Neemias Villalovos Gonzales**  
    Especialista SIG y Ordenamiento Territorial
    """
)
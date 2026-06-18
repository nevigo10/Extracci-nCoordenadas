import streamlit as st
import pdfplumber
import pandas as pd
import re
import streamlit.components.v1 as components

# ----------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ----------------------------------

st.set_page_config(
    page_title="Extractor de Coordenadas PDF",
    page_icon="🌎",
    layout="wide"
)

# ----------------------------------
# GOOGLE ANALYTICS GA4
# ----------------------------------

components.html(
    """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-37RXM995LJ"></script>

    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-37RXM995LJ');
    </script>
    """,
    height=0
)

# ----------------------------------
# TÍTULO
# ----------------------------------

st.title("🌎 Extractor de coordenadas PDF")

st.write(
    "Extrae coordenadas UTM desde documentos PDF y exporta los resultados a CSV."
)

# ----------------------------------
# CARGAR PDF
# ----------------------------------

archivo = st.file_uploader(
    "Seleccione un archivo PDF",
    type=["pdf"]
)

# ----------------------------------
# PROCESAMIENTO
# ----------------------------------

if archivo:

    texto = ""

    try:

        with pdfplumber.open(archivo) as pdf:

            for pagina in pdf.pages:

                contenido = pagina.extract_text()

                if contenido:
                    texto += contenido + "\n"

        st.subheader("📄 Texto extraído")

        st.text_area(
            "",
            texto,
            height=250
        )

        # ----------------------------------
        # BUSCAR COORDENADAS UTM
        # ----------------------------------

        patron_utm = r'(\d{6,8}\.\d+)\s+(\d{6,8}\.\d+)'

        coordenadas = re.findall(
            patron_utm,
            texto
        )

        if coordenadas:

            df = pd.DataFrame(
                coordenadas,
                columns=["NORTE_Y", "ESTE_X"]
            )

            st.success(
                f"✅ Se encontraron {len(df)} coordenadas."
            )

            st.subheader("📍 Coordenadas encontradas")

            st.dataframe(
                df,
                use_container_width=True
            )

            # ----------------------------------
            # DESCARGA CSV
            # ----------------------------------

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
                "⚠️ No se encontraron coordenadas con el patrón configurado."
            )

    except Exception as e:

        st.error(
            f"Error al procesar el PDF: {e}"
        )

# ----------------------------------
# CRÉDITOS
# ----------------------------------

st.markdown("---")

st.markdown(
    """
### 👨‍💻 Elaborado por

**Neemias Villalovos Gonzales**  
Especialista SIG y Ordenamiento Territorial

🌐 https://neemiasvillalovos.com

---
Versión 1.0
"""
)

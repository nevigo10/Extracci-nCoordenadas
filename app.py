import streamlit as st
import pdfplumber
import pandas as pd
import re
import streamlit.components.v1 as components

# ----------------------------------
# CONFIGURACIÓN
# ----------------------------------

st.set_page_config(
    page_title="Extractor de Coordenadas PDF",
    page_icon="🌎",
    layout="wide"
)

# ----------------------------------
# GOOGLE ANALYTICS
# ----------------------------------

components.html(
    """
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
# INTERFAZ
# ----------------------------------

st.title("🌎 Extractor de Coordenadas PDF")

st.write(
    "Extrae coordenadas UTM desde documentos PDF y exporta resultados."
)

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

        coordenadas_limpias = []

        # ----------------------------------
        # FORMATO:
        # 1550555.850 546436.452
        # 1,748,334.31 409,023.26
        # ----------------------------------

        patron_general = r'([\d,]+\.\d+)\s+([\d,]+\.\d+)'

        coincidencias = re.findall(
            patron_general,
            texto
        )

        for y, x in coincidencias:

            try:

                y = float(
                    y.replace(",", "")
                )

                x = float(
                    x.replace(",", "")
                )

                coordenadas_limpias.append(
                    [y, x]
                )

            except:
                pass

        # ----------------------------------
        # ELIMINAR DUPLICADOS
        # ----------------------------------

        coordenadas_limpias = list(
            dict.fromkeys(
                tuple(i) for i in coordenadas_limpias
            )
        )

        if coordenadas_limpias:

            df = pd.DataFrame(
                coordenadas_limpias,
                columns=[
                    "NORTE_Y",
                    "ESTE_X"
                ]
            )

            st.success(
                f"✅ Se encontraron {len(df)} coordenadas."
            )

            st.subheader(
                "📍 Coordenadas encontradas"
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            # CSV

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
                "⚠️ No se encontraron coordenadas."
            )

    except Exception as e:

        st.error(
            f"Error al procesar PDF: {e}"
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
Versión 2.0
"""
)

import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os

# Configuración de página
st.set_page_config(page_title="Facturas - R.D. Avendano Solutions", layout="centered", page_icon="🧾")

# 1. DISEÑO ESTÉTICO DE ALTA GAMA (CSS Inyectado)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500;600&display=swap');
    
    .stApp { background-color: #f1f5f9; }
    
    /* Contenedor principal estilo "hoja de papel" */
    .block-container {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
        padding: 2.5rem 2.5rem !important;
        max-width: 850px;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    h1, h2, h3, p, span, div, label { font-family: 'Inter', sans-serif; }
    
    .company-title { font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; color: #1e293b; margin-bottom: 2px; }
    .invoice-title { font-family: 'Space Grotesk', sans-serif; font-size: 34px; font-weight: 700; color: #c97a6e; text-align: right; margin-bottom: 2px; }
    .details-text { font-size: 13px; color: #64748b; line-height: 1.6; }
    
    /* Diseño del botón de descarga */
    div[data-testid="stDownloadButton"] > button {
        background-color: #c97a6e; color: white; width: 100%; padding: 12px; 
        font-size: 15px; font-weight: 600; border: none; border-radius: 8px; transition: all 0.2s;
    }
    div[data-testid="stDownloadButton"] > button:hover { background-color: #b0665a; color: white; }
    
    /* Botón secundario (Avanzar Factura) */
    .stButton > button { background-color: #1e293b; color: white; width: 100%; padding: 12px; font-weight: 500; border-radius: 8px; }
    .stButton > button:hover { background-color: #334155; color: white; }
</style>
""", unsafe_allow_html=True)

# 2. LÓGICA DE MEMORIA Y AUTOMATIZACIÓN
if 'invoice_seq' not in st.session_state:
    st.session_state.invoice_seq = 1

if 'clientes_db' not in st.session_state:
    st.session_state.clientes_db = {"Comercial Client LLC": "Houston, TX"}

if 'df_items' not in st.session_state:
    st.session_state.df_items = pd.DataFrame([{"Descripción": "Servicio eléctrico general", "Cant.": 1.0, "Precio U.": 150.0}])

fecha_actual = datetime.now().strftime('%Y-%m-%d')
year = datetime.now().year
num_factura = f"{year}-{st.session_state.invoice_seq:03d}"

# 3. ENCABEZADO VISUAL ELEGANTE
c1, c2 = st.columns([1.5, 1])
with c1:
    st.markdown('<p class="company-title">R.D. AVENDANO SOLUTIONS</p>', unsafe_allow_html=True)
    st.markdown('<p class="details-text">ID: Ricardo Avendano<br>Tel: +1 346 333 5819 | Correo: ricardodario.a@gmail.com<br>7150 Foxbrick Ln, Apt 4105, Humble, TX 77338</p>', unsafe_allow_html=True)
with c2:
    st.markdown('<p class="invoice-title">FACTURA</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="details-text" style="text-align: right;"><strong>Fecha:</strong> {fecha_actual}<br><strong>Nº:</strong> {num_factura}</p>', unsafe_allow_html=True)

st.markdown("<hr style='margin-top:10px; border-color:#e2e8f0;'>", unsafe_allow_html=True)

# 4. BASE DE DATOS DE CLIENTES DINÁMICA
st.markdown("### 👤 Facturar a:")
col_cl1, col_cl2 = st.columns(2)
cliente_seleccionado = col_cl1.selectbox("Seleccionar Cliente Guardado", ["-- Crear Nuevo Cliente --"] + list(st.session_state.clientes_db.keys()))

if cliente_seleccionado == "-- Crear Nuevo Cliente --":
    cliente_nombre = col_cl1.text_input("Nombre de la Empresa o Cliente")
    cliente_dir = col_cl2.text_area("Dirección del Cliente")
    if col_cl2.button("💾 Guardar Nuevo Cliente"):
        if cliente_nombre:
            st.session_state.clientes_db[cliente_nombre] = cliente_dir
            st.rerun()
else:
    cliente_nombre = cliente_seleccionado
    cliente_dir = col_cl2.text_area("Dirección", value=st.session_state.clientes_db[cliente_nombre])

# 5. TABLA DE CONCEPTOS OPTIMIZADA PARA CELULAR
st.markdown("---")
st.markdown("### 🛒 Conceptos y Servicios")
edited_df = st.data_editor(
    st.session_state.df_items,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "Descripción": st.column_config.TextColumn("Descripción", required=True),
        "Cant.": st.column_config.NumberColumn("Cant.", min_value=0.1, step=0.5, format="%.1f", required=True),
        "Precio U.": st.column_config.NumberColumn("Precio U.", min_value=0.0, step=5.0, format="$%.2f", required=True)
    }
)
st.session_state.df_items = edited_df

# 6. CÁLCULOS AUTOMÁTICOS
edited_df["Importe"] = edited_df["Cant."] * edited_df["Precio U."]
subtotal = edited_df["Importe"].sum()
tax = subtotal * 0.0825
total = subtotal + tax

# 7. TOTALES Y TÉRMINOS
st.markdown("---")
col_t1, col_t2 = st.columns([1.2, 1])
with col_t1:
    st.markdown("**💳 Condiciones de Pago:**")
    terminos = st.selectbox("Condiciones", ["Pagadero al recibir esta factura", "A 15 días (Net 15)", "A 30 días (Net 30)", "50% anticipo, 50% al finalizar"], label_visibility="collapsed")
    st.markdown("<p class='details-text' style='margin-top:10px;'><strong>Métodos:</strong> Zelle, Cheque (Ricardo Avendano), Efectivo</p>", unsafe_allow_html=True)

with col_t2:
    st.markdown(f"""
    <div style="text-align: right;">
        <p class="details-text" style="font-size: 15px; margin-bottom: 5px;">Subtotal: &nbsp;<strong>${subtotal:,.2f}</strong></p>
        <p class="details-text" style="font-size: 15px; margin-bottom: 5px;">Impuestos (8.25%): &nbsp;<strong>${tax:,.2f}</strong></p>
        <p style="font-size: 26px; font-weight: 700; color: #c97a6e; margin-top: 10px;">TOTAL: ${total:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)

# 8. GENERADOR DE PDF NATIVO
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 8, txt="R.D. AVENDANO SOLUTIONS", ln=True, align='C')
    pdf.set_font("Arial", size=9)
    pdf.cell(200, 4, txt="7150 Foxbrick Ln, Apt 4105, Humble, TX 77338", ln=True, align='C')
    pdf.cell(200, 4, txt="Tel: +1 346 333 5819 | Email: ricardodario.a@gmail.com", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 8, txt="FACTURA / INVOICE", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 6, txt=f"Fecha: {fecha_actual} | Factura #: {num_factura}", ln=True, align='R')
    pdf.cell(200, 6, txt=f"Cliente: {cliente_nombre}", ln=True, align='L')
    pdf.cell(200, 6, txt=f"Direccion: {cliente_dir.replace(chr(10), ' ')}", ln=True, align='L')
    pdf.ln(5)
    
    pdf.set_fill_color(220, 230, 242)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(105, 8, "Descripcion", border=1, fill=True)
    pdf.cell(15, 8, "Cant", border=1, align='C', fill=True)
    pdf.cell(35, 8, "Precio U.", border=1, align='C', fill=True)
    pdf.cell(35, 8, "Importe", border=1, align='C', fill=True)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    for _, row in edited_df.iterrows():
        desc = str(row['Descripción'])[:50]
        c_val = row['Cant.']
        p_val = row['Precio U.']
        imp = c_val * p_val
        pdf.cell(105, 8, desc, border=1)
        pdf.cell(15, 8, f"{c_val:.1f}", border=1, align='C')
        pdf.cell(35, 8, f"${p_val:.2f}", border=1, align='C')
        pdf.cell(35, 8, f"${imp:.2f}", border=1, align='C')
        pdf.ln()
        
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(155, 7, "Subtotal:", align='R')
    pdf.cell(35, 7, f"${subtotal:.2f}", ln=True, align='R', border=1)
    pdf.cell(155, 7, "Tax (8.25%):", align='R')
    pdf.cell(35, 7, f"${tax:.2f}", ln=True, align='R', border=1)
    pdf.set_fill_color(200, 255, 200)
    pdf.cell(155, 8, "TOTAL:", align='R')
    pdf.cell(35, 8, f"${total:.2f}", ln=True, align='R', border=1, fill=True)
    
    pdf.ln(8)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 5, txt="Condiciones de Pago:", ln=True)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(200, 4, txt=f"{terminos}. Metodos: Zelle, Cheque (Ricardo Avendano), Efectivo.")
    
    tmp = f"{num_factura}.pdf"
    pdf.output(tmp)
    with open(tmp, "rb") as f:
        data = f.read()
    os.remove(tmp)
    return data

st.markdown("---")
col_b1, col_b2 = st.columns(2)

with col_b1:
    st.download_button(
        label="📥 DESCARGAR FACTURA (PDF)",
        data=generar_pdf(),
        file_name=f"Factura_{num_factura}.pdf",
        mime="application/pdf"
    )

with col_b2:
    if st.button("✅ Factura Cobrada (Avanzar al siguiente Nº)"):
        st.session_state.invoice_seq += 1
        st.session_state.df_items = pd.DataFrame([{"Descripción": "Servicio eléctrico general", "Cant.": 1.0, "Precio U.": 150.0}])
        st.rerun()

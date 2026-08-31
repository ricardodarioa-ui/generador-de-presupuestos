import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64
import os

st.set_page_config(page_title="Facturas - R.D. Avendano Solution", layout="wide", page_icon="🧾")

# Estilo ultra fluido optimizado para celular
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    h1, h2, h3 { color: #1e293b; }
</style>
""", unsafe_allow_html=True)

idioma = st.sidebar.radio("🌐 Idioma / Language", ["Español", "English"])
is_es = idioma == "Español"

st.title("🧾 R.D. Avendano Solutions")
st.markdown("*7150 Foxbrick Ln, Apt 4105, Humble, TX 77338 • Tel: +1 346 333 5819*")

# Memoria automática para el número de factura y datos
if 'secuencia_factura' not in st.session_state:
    st.session_state.secuencia_factura = 1

st.sidebar.header("📋 Datos de la Factura")
year = datetime.now().year
default_inv = f"{year}-{st.session_state.secuencia_factura:03d}"
codigo_factura = st.sidebar.text_input("Nº de Factura (Auto)", value=default_inv)
fecha_factura = st.sidebar.date_input("Fecha", datetime.now())
tax_rate = st.sidebar.number_input("Impuesto / Tax (%)", value=8.25, step=0.25) / 100

st.sidebar.markdown("---")
cliente_nombre = st.sidebar.text_input("Nombre del Cliente", "Comercial Client LLC")
cliente_direccion = st.sidebar.text_area("Dirección del Cliente", "Houston, TX")

st.markdown("### 🛒 Partidas de la Factura")

if 'factura_items' not in st.session_state:
    st.session_state.factura_items = [{"descripcion": "Servicio eléctrico general", "cantidad": 1.0, "precio": 150.0}]

with st.form("form_item", clear_on_submit=True):
    c1, c2, c3 = st.columns([4, 1, 1])
    d_input = c1.text_input("Descripción del servicio o material")
    c_input = c2.number_input("Cant.", min_value=0.5, value=1.0, step=0.5)
    p_input = c3.number_input("Precio U. ($)", min_value=0.0, value=50.0, step=5.0)
    submitted = st.form_submit_button("➕ Agregar Concepto")
    if submitted and d_input:
        st.session_state.factura_items.append({"descripcion": d_input, "cantidad": c_input, "precio": p_input})
        st.rerun()

subtotal_gen = 0.0
to_delete = []

if st.session_state.factura_items:
    for idx, item in enumerate(st.session_state.factura_items):
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        item['descripcion'] = col1.text_input(f"Desc {idx+1}", value=item['descripcion'], key=f"d_{idx}")
        item['cantidad'] = col2.number_input(f"Cant {idx+1}", value=float(item['cantidad']), min_value=0.1, step=0.5, key=f"c_{idx}")
        item['precio'] = col3.number_input(f"Precio {idx+1}", value=float(item['precio']), min_value=0.0, step=5.0, key=f"p_{idx}")
        sub_i = item['cantidad'] * item['precio']
        subtotal_gen += sub_i
        col4.metric(f"Sub {idx+1}", f"${sub_i:.2f}")
        if col5.button("❌", key=f"del_{idx}"):
            to_delete.append(idx)

    if to_delete:
        for i in sorted(to_delete, reverse=True):
            st.session_state.factura_items.pop(i)
        st.rerun()

    if st.button("🗑️ Vaciar lista"):
        st.session_state.factura_items = []
        st.rerun()

st.markdown("---")
st.subheader("💳 Condiciones y Términos")
terminos_texto = st.selectbox("Términos de Pago", [
    "Pagadero al recibir esta factura. Agradecemos su pronto pago.",
    "Neto 15 días. El pago debe efectuarse en un plazo de 15 días.",
    "Neto 30 días. El pago debe efectuarse en un plazo de 30 días.",
    "El pago debe realizarse al finalizar el trabajo.",
    "50% de anticipo, 50% restante al finalizar."
])
metodos_pago = "- Zelle\n- Cheque (Ricardo Avendano)\n- Efectivo"

if st.session_state.factura_items:
    monto_tax = subtotal_gen * tax_rate
    total_final = subtotal_gen + monto_tax

    st.markdown("---")
    st.markdown("### 📊 Totales")
    r1, r2, r3 = st.columns(3)
    r1.info(f"**Subtotal:** ${subtotal_gen:,.2f}")
    r2.warning(f"**Tax ({(tax_rate*100):.2f}%):** ${monto_tax:,.2f}")
    r3.success(f"**TOTAL:** ${total_final:,.2f}")

    def generar_pdf_nativo(cliente, dir_c, codigo, fecha_str, subtotal, tax, total, items, terminos, is_es):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 8, txt="R.D. AVENDANO SOLUTIONS", ln=True, align='C')
        pdf.set_font("Arial", size=9)
        pdf.cell(200, 4, txt="7150 Foxbrick Ln, Apt 4105, Humble, TX 77338", ln=True, align='C')
        pdf.cell(200, 4, txt="Tel: +1 346 333 5819 | Email: ricardodario.a@gmail.com", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 8, txt="FACTURA" if is_es else "INVOICE", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 6, txt=f"Fecha / Date: {fecha_str} | Factura #: {codigo}", ln=True, align='R')
        pdf.cell(200, 6, txt=f"Cliente: {cliente}", ln=True, align='L')
        pdf.cell(200, 6, txt=f"Dirección: {dir_c}", ln=True, align='L')
        pdf.ln(5)
        
        pdf.set_fill_color(220, 230, 242)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(105, 8, "Descripción" if is_es else "Description", border=1, fill=True)
        pdf.cell(15, 8, "Cant", border=1, align='C', fill=True)
        pdf.cell(35, 8, "Precio U.", border=1, align='C', fill=True)
        pdf.cell(35, 8, "Importe", border=1, align='C', fill=True)
        pdf.ln()
        
        pdf.set_font("Arial", size=10)
        for it in items:
            desc = it['descripcion'][:50]
            sub_it = it['cantidad'] * it['precio']
            pdf.cell(105, 8, desc, border=1)
            pdf.cell(15, 8, str(it['cantidad']), border=1, align='C')
            pdf.cell(35, 8, f"${it['precio']:.2f}", border=1, align='C')
            pdf.cell(35, 8, f"${sub_it:.2f}", border=1, align='C')
            pdf.ln()
            
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(155, 7, "Subtotal:", align='R')
        pdf.cell(35, 7, f"${subtotal:.2f}", ln=True, align='R', border=1)
        pdf.cell(155, 7, "Tax:", align='R')
        pdf.cell(35, 7, f"${tax:.2f}", ln=True, align='R', border=1)
        pdf.set_fill_color(200, 255, 200)
        pdf.cell(155, 8, "TOTAL:", align='R')
        pdf.cell(35, 8, f"${total:.2f}", ln=True, align='R', border=1, fill=True)
        
        pdf.ln(8)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 5, txt="Términos de Pago:", ln=True)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(200, 4, txt=terminos)
        
        tmp = f"{codigo.replace('/', '-')}.pdf"
        pdf.output(tmp)
        with open(tmp, "rb") as f:
            b = f.read()
        os.remove(tmp)
        return b

    pdf_bytes = generar_pdf_nativo(cliente_nombre, cliente_direccion, codigo_factura, fecha_factura.strftime('%Y-%m-%d'), subtotal_gen, monto_tax, total_final, st.session_state.factura_items, terminos_texto, is_es)
    
    st.markdown("---")
    b64 = base64.b64encode(pdf_bytes).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{codigo_factura}.pdf"><button style="width:100%; padding:15px; background-color:#1b5e20; color:white; font-size:18px; font-weight:bold; border:none; border-radius:8px; cursor:pointer;">📥 DESCARGAR FACTURA EN PDF</button></a>'
    st.markdown(href, unsafe_allow_html=True)

    # Botón para autoincrementar el número de factura para la siguiente vez
    if st.button("✅ Factura Emitida (Avanzar al siguiente número)"):
        st.session_state.secuencia_factura += 1
        st.success("¡Número de factura actualizado para la próxima!")
        st.rerun()

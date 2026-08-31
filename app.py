import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64
import os

st.set_page_config(page_title="Facturas - R.D. Avendano Solutions", layout="wide", page_icon="🧾")

# Selector de idioma en la barra lateral
idioma = st.sidebar.radio("🌐 Idioma / Language", ["Español", "English"])
is_es = idioma == "Español"

st.title("🧾 R.D. Avendano Solutions - Facturación")
st.markdown("*7150 Foxbridge Ln, Apt 4105, Humble, TX 77338 • Tel: +1 346 333 5819*")

# Datos del cliente en la barra lateral
st.sidebar.header("📋 Datos del Cliente / Client Info")
cliente_nombre = st.sidebar.text_input("Nombre del Cliente", "Comercial Client LLC")
cliente_direccion = st.sidebar.text_area("Dirección y Ciudad", "Houston, TX")

# Configuración de factura
year = datetime.now().year
codigo_factura = st.sidebar.text_input("Nº de Factura", f"{year}-001")
fecha_factura = st.sidebar.text_input("Fecha", datetime.now().strftime('%Y-%m-%d'))
tax_rate = st.sidebar.number_input("Impuesto / Tax (%)", value=8.25, step=0.25) / 100

st.markdown("---")
st.subheader("🛒 Partidas de la Factura / Invoice Items")

# Inicializar lista de ítems en sesión si no existe
if 'factura_items' not in st.session_state:
    st.session_state.factura_items = [{"descripcion": "Servicio eléctrico general", "cantidad": 1.0, "precio": 150.0}]

# Formulario para agregar filas
with st.form("form_agregar_item", clear_on_submit=True):
    col_f1, col_f2, col_f3 = st.columns([4, 1, 1])
    nueva_desc = col_f1.text_input("Descripción del servicio o material")
    nueva_cant = col_f2.number_input("Cantidad", min_value=0.5, value=1.0, step=0.5)
    nuevo_precio = col_f3.number_input("Precio U. ($)", min_value=0.0, value=50.0, step=5.0)
    agregar_btn = st.form_submit_button("➕ Agregar Fila")
    if agregar_btn and nueva_desc:
        st.session_state.factura_items.append({
            "descripcion": nueva_desc,
            "cantidad": nueva_cant,
            "precio": nuevo_precio
        })
        st.rerun()

subtotal_gen = 0.0
indices_a_eliminar = []

if st.session_state.factura_items:
    st.markdown("#### Detalle actual:")
    for i, item in enumerate(st.session_state.factura_items):
        c_i1, c_i2, c_i3, c_i4, c_i5 = st.columns([3, 1, 1, 1, 1])
        
        # Permitir edición rápida en pantalla
        item['descripcion'] = c_i1.text_input(f"Desc {i+1}", value=item['descripcion'], key=f"desc_{i}")
        item['cantidad'] = c_i2.number_input(f"Cant {i+1}", value=float(item['cantidad']), min_value=0.1, step=0.5, key=f"cant_{i}")
        item['precio'] = c_i3.number_input(f"Precio {i+1}", value=float(item['precio']), min_value=0.0, step=5.0, key=f"precio_{i}")
        
        sub_fila = item['cantidad'] * item['precio']
        subtotal_gen += sub_fila
        c_i4.metric(f"Importe {i+1}", f"${sub_fila:.2f}")
        
        if c_i5.button("❌", key=f"del_{i}"):
            indices_a_eliminar.append(i)

    if indices_a_eliminar:
        for idx in sorted(indices_a_eliminar, reverse=True):
            st.session_state.factura_items.pop(idx)
        st.rerun()

    if st.button("🗑️ Vaciar toda la factura"):
        st.session_state.factura_items = []
        st.rerun()

# Términos de pago
st.markdown("---")
st.subheader("💳 Términos y Métodos de Pago")
terminos_opciones = {
    "Pago inmediato / Due on receipt": "Pagadero al recibir esta factura. Agradecemos su pronto pago.",
    "A 15 días / Net 15": "Neto 15 días. El pago debe efectuarse en un plazo de 15 días.",
    "A 30 días / Net 30": "Neto 30 días. El pago debe efectuarse en un plazo de 30 días.",
    "Al finalizar / Upon completion": "El pago debe realizarse al finalizar el trabajo.",
    "50% y 50% / Half deposit": "50% de anticipo, 50% restante al finalizar."
}
terminos_seleccionados = st.selectbox("Seleccionar condiciones estándar", list(terminos_opciones.keys()))
terminos_texto = st.text_area("Texto de términos de pago", value=terminos_opciones[terminos_seleccionados])

metodos_pago = st.text_area("Métodos Aceptados", value="- Zelle\n- Cheque (Ricardo Avendano)\n- Efectivo")

if st.session_state.factura_items:
    monto_tax = subtotal_gen * tax_rate
    total_final = subtotal_gen + monto_tax
    
    st.markdown("---")
    st.markdown("### 📊 Resumen Financiero")
    c_res1, c_res2, c_res3 = st.columns(3)
    c_res1.info(f"**Subtotal:** ${subtotal_gen:,.2f}")
    c_res2.warning(f"**Impuestos ({(tax_rate*100):.2f}%):** ${monto_tax:,.2f}")
    c_res3.success(f"**TOTAL:** ${total_final:,.2f}")
    
    # Función para generar PDF profesional
    def generar_pdf_factura(cliente, dir_c, codigo, fecha, subtotal, tax, total, items, terminos, metodos, is_es):
        pdf = FPDF()
        pdf.add_page()
        
        # Encabezado
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 8, txt="R.D. AVENDANO SOLUTIONS", ln=True, align='C')
        pdf.set_font("Arial", size=9)
        pdf.cell(200, 4, txt="7150 Foxbridge Ln, Apt 4105, Humble, TX 77338", ln=True, align='C')
        pdf.cell(200, 4, txt="Tel: +1 346 333 5819 | Email: ricardodario.a@gmail.com", ln=True, align='C')
        pdf.ln(5)
        
        pdf.set_font("Arial", 'B', 14)
        titulo_doc = "FACTURA" if is_es else "INVOICE"
        pdf.cell(200, 8, txt=titulo_doc, ln=True, align='C')
        
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 6, txt=f"Fecha / Date: {fecha} | Factura # / Invoice #: {codigo}", ln=True, align='R')
        pdf.cell(200, 6, txt=f"Facturar a / Bill To: {cliente}", ln=True, align='L')
        pdf.cell(200, 6, txt=f"Dirección / Address: {dir_c}", ln=True, align='L')
        pdf.ln(5)
        
        # Tabla de items
        pdf.set_fill_color(220, 230, 242)
        pdf.set_font("Arial", 'B', 10)
        h_desc = "Descripción del Servicio" if is_es else "Description"
        pdf.cell(105, 8, h_desc, border=1, fill=True)
        pdf.cell(15, 8, "Cant", border=1, align='C', fill=True)
        pdf.cell(35, 8, "Precio U.", border=1, align='C', fill=True)
        pdf.cell(35, 8, "Importe", border=1, align='C', fill=True)
        pdf.ln()
        
        pdf.set_font("Arial", size=10)
        for it in items:
            desc = it['descripcion'][:55] + "..." if len(it['descripcion']) > 55 else it['descripcion']
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
        pdf.cell(155, 7, "Tax / Impuestos:", align='R')
        pdf.cell(35, 7, f"${tax:.2f}", ln=True, align='R', border=1)
        pdf.set_fill_color(200, 255, 200)
        pdf.cell(155, 8, "TOTAL:", align='R')
        pdf.cell(35, 8, f"${total:.2f}", ln=True, align='R', border=1, fill=True)
        
        # Términos y métodos
        pdf.ln(8)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 5, txt="Términos de Pago / Payment Terms:", ln=True)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(200, 4, txt=terminos)
        pdf.ln(2)
        
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 5, txt="Métodos Aceptados / Accepted Methods:", ln=True)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(200, 4, txt=metodos)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 9)
        t_gracias = "¡Gracias por su preferencia!" if is_es else "Thank you for your business!"
        pdf.cell(200, 5, txt=t_gracias, ln=True, align='C')
        
        tmp = f"{codigo}.pdf"
        pdf.output(tmp)
        with open(tmp, "rb") as f:
            b = f.read()
        os.remove(tmp)
        return b

    pdf_bytes = generar_pdf_factura(cliente_nombre, cliente_direccion, codigo_factura, fecha_factura, subtotal_gen, monto_tax, total_final, st.session_state.factura_items, terminos_texto, metodos_pago, is_es)
    
    st.markdown("---")
    st.subheader("👁️ Previsualización de la Factura en PDF")
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    st.markdown(f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{codigo_factura}.pdf"><button style="width:100%; padding:15px; background-color:#1b5e20; color:white; font-size:18px; font-weight:bold; border:none; border-radius:8px; cursor:pointer;">📥 DESCARGAR FACTURA EN PDF</button></a>'
    st.markdown(href, unsafe_allow_html=True)

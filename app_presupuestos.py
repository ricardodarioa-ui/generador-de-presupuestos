import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import base64
import os

def init_db():
    conn = sqlite3.connect("presupuestos_app.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS catalogo 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, item_es TEXT, item_en TEXT, precio_base REAL, unidad TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')
    
    cursor.execute("SELECT COUNT(*) FROM catalogo")
    if cursor.fetchone()[0] < 75:
        cursor.execute("DELETE FROM catalogo") 
        items_iniciales = [
            # 1. MANO DE OBRA Y SERVICIOS PROFESIONALES
            ("Mano de Obra", "Hora de Electricista (Comercial / Industrial)", "Electrician Hourly Rate (Commercial)", 95.0, "hora"),
            ("Mano de Obra", "Hora de Ayudante / General (Helper)", "Helper / General Labor Hourly Rate", 45.0, "hora"),
            ("Mano de Obra", "Llamada de Emergencia / Service Call (Fuera de horario)", "Emergency Call-Out Fee (After hours)", 150.0, "servicio"),
            ("Mano de Obra", "Diagnóstico avanzado de fallas / Troubleshooting", "Advanced Electrical Troubleshooting", 120.0, "servicio"),
            ("Mano de Obra", "Tirada de cable THHN (Solo Labor por pie)", "THHN Wire Pull (Labor only per ft)", 2.5, "ft"),
            ("Mano de Obra", "Tirada de Cable de Aluminio SER / XHHW-2 (Labor por ft)", "SER / XHHW-2 Aluminum Wire Pull (Labor per ft)", 4.5, "ft"),
            ("Mano de Obra", "Instalación de tubería EMT (Solo Labor por pie)", "EMT Conduit Install (Labor only per ft)", 4.5, "ft"),
            ("Mano de Obra", "Certificación e inspección de instalaciones", "Inspection & Code Compliance Check", 200.0, "servicio"),
            
            # 2. INSTALACIONES Y AUTOMATIZACIÓN
            ("Instalación", "Tomacorriente 120V 20A Comercial (Mat. + Labor)", "Commercial Receptacle 120V 20A (Mat. + Labor)", 65.0, "unidad"),
            ("Instalación", "Tomacorriente GFCI 20A (Mat. + Labor)", "GFCI 20A Receptacle (Mat. + Labor)", 85.0, "unidad"),
            ("Instalación", "Tomacorriente Twist-Lock 20A/30A (Mat. + Labor)", "Twist-Lock Receptacle 20A/30A (Mat. + Labor)", 125.0, "unidad"),
            ("Instalación", "Tomacorriente de Piso Comercial (Floor Box)", "Commercial Floor Box Receptacle Install", 175.0, "unidad"),
            ("Instalación", "Interruptor Simple (Single Pole Switch)", "Single Pole Switch (Mat. + Labor)", 45.0, "unidad"),
            ("Instalación", "Interruptor 3-Way / 4-Way (Mat. + Labor)", "3-Way / 4-Way Switch (Mat. + Labor)", 65.0, "unidad"),
            ("Instalación", "Interruptor Inteligente / Dimmer (Smart/Dimmer)", "Smart Switch / Dimmer Install", 85.0, "unidad"),
            ("Instalación", "Línea de Datos Cat6 / Red Comercial (Drop)", "Cat6 Data Drop / Commercial Networking", 120.0, "unidad"),
            ("Instalación", "Relé Inteligente / Control de Automatización (ESP32/Arduino/Sonoff)", "Smart Home Automation Relay / Module", 95.0, "unidad"),
            ("Instalación", "Cámara de Seguridad PoE (Cableado e Instalación)", "PoE Security Camera (Wiring & Install)", 180.0, "unidad"),
            
            # 3. ILUMINACIÓN COMERCIAL E INDUSTRIAL
            ("Iluminación", "Luminaria LED High Bay (Comercial/Industrial)", "LED High Bay Fixture Install", 220.0, "unidad"),
            ("Iluminación", "Luminaria LED Panel 2x4 (Troffer)", "2x4 LED Troffer Panel Install", 145.0, "unidad"),
            ("Iluminación", "Luminaria de Emergencia / Letrero Exit Sign", "Emergency / Exit Sign Fixture", 95.0, "unidad"),
            ("Iluminación", "Wall Pack LED Exterior con Fotocelda", "Exterior LED Wall Pack w/ Photocell", 180.0, "unidad"),
            ("Iluminación", "Reflector LED Exterior (Flood Light)", "Exterior LED Flood Light Install", 150.0, "unidad"),
            ("Iluminación", "Lámpara de Poste LED (Shoebox / Parking Lot Light)", "LED Shoebox / Parking Lot Light", 450.0, "unidad"),
            ("Iluminación", "Cambio de Balastro a Direct Wire LED Retrofit", "Ballast Bypass / Direct Wire LED Retrofit", 65.0, "unidad"),
            ("Iluminación", "Rocker / Sensor de Movimiento de Pared", "Wall Occupancy / Motion Sensor Install", 110.0, "unidad"),
            ("Iluminación", "Sensor Fotocelda Exterior 120-277V", "Exterior Photocell Sensor 120-277V", 45.0, "unidad"),
            
            # 4. PANELES, BREAKERS Y ALTA CARGA
            ("Paneles", "Reemplazo de Breaker 15A/20A (1 Polo)", "1-Pole Breaker 15A/20A Replacement", 75.0, "unidad"),
            ("Paneles", "Reemplazo de Breaker 30A/40A/50A (2 Polos)", "2-Pole Breaker 30A-50A Replacement", 120.0, "unidad"),
            ("Paneles", "Breaker Trifásico (3 Polos) Comercial", "3-Pole Commercial Breaker Replacement", 180.0, "unidad"),
            ("Paneles", "Breaker AFCI / GFCI (Arco/Falla a Tierra)", "AFCI / GFCI Breaker Install", 135.0, "unidad"),
            ("Paneles", "Instalación de Subpanel 100A / 125A", "100A / 125A Subpanel Installation", 550.0, "unidad"),
            ("Paneles", "Actualización de Panel Principal 200A Main", "200A Main Panel Upgrade", 1800.0, "servicio"),
            ("Paneles", "Centro de Carga Principal (Load Center) 3-Fases 225A", "3-Phase 225A Main Load Center Install", 1200.0, "servicio"),
            ("Paneles", "Cargador para Vehículo Eléctrico (EV Charger NEMA 14-50)", "EV Charger Installation (NEMA 14-50)", 450.0, "unidad"),
            ("Paneles", "Interruptor de Transferencia Manual 30A/50A (Generador)", "Manual Transfer Switch 30A/50A (Generator)", 350.0, "unidad"),
            ("Paneles", "Limpieza profunda, Torqueado e Inspección de Tablero", "Panel Torquing, Cleaning & Inspection", 150.0, "servicio"),
            ("Paneles", "Instalación de Supresor de Picos General (SPD)", "Whole-House / Commercial Surge Protector", 250.0, "unidad"),
            
            # 5. MOTORES, CONTACTORES, TRANSFORMADORES Y CONTROLES
            ("Equipos Comerciales", "Sustitución de Contactor de Iluminación Multipolo", "Multipole Lighting Contactor Replacement", 250.0, "unidad"),
            ("Equipos Comerciales", "Sustitución de Contactor de Motor / Starter", "Motor Contactor / Starter Replacement", 185.0, "unidad"),
            ("Equipos Comerciales", "Instalación de Disconnect / Safety Switch 30A/60A", "Disconnect / Safety Switch 30A/60A", 220.0, "unidad"),
            ("Equipos Comerciales", "Diagnóstico de Motor / Control / Variador (VFD)", "Motor / VFD Control Circuit Diagnostic", 140.0, "servicio"),
            ("Equipos Comerciales", "Mantenimiento a Motor Eléctrico (Limpieza y Megger Test)", "Electric Motor Maintenance & Megger Test", 180.0, "servicio"),
            ("Equipos Comerciales", "Instalación de Transformador Step-Down", "Step-Down Transformer Installation", 850.0, "unidad"),
            ("Equipos Comerciales", "Instalación de Relevador de Tiempo (Timer)", "Time Clock / Relay Installation", 130.0, "unidad"),
            
            # 6. MATERIALES Y SUMINISTROS (Supply)
            ("Materiales", "Rollo Cable THHN #12 (500 ft)", "THHN #12 Wire Roll (500 ft)", 115.0, "rollo"),
            ("Materiales", "Rollo Cable THHN #10 (500 ft)", "THHN #10 Wire Roll (500 ft)", 165.0, "rollo"),
            ("Materiales", "Carrete Cable THHN #8 (Por pie)", "THHN #8 Wire (Per ft)", 0.65, "ft"),
            ("Materiales", "Carrete Cable THHN #6 (Por pie)", "THHN #6 Wire (Per ft)", 1.10, "ft"),
            ("Materiales", "Tubo EMT 1/2 pulgada (10 ft)", "1/2 inch EMT Conduit (10 ft stick)", 8.5, "unidad"),
            ("Materiales", "Tubo EMT 3/4 pulgada (10 ft)", "3/4 inch EMT Conduit (10 ft stick)", 12.0, "unidad"),
            ("Materiales", "Tubo PVC Schedule 40 3/4 pulgada (10 ft)", "3/4 inch Schedule 40 PVC Conduit (10 ft)", 6.0, "unidad"),
            ("Materiales", "Tubo Rígido Galvanizado (GRC) 3/4 pulgada (10 ft)", "3/4 inch GRC Rigid Conduit (10 ft)", 28.0, "unidad"),
            ("Materiales", "Caja Condulet LB / LL / LR 3/4 pulgada", "3/4 inch LB / LL / LR Conduit Body", 12.0, "unidad"),
            ("Materiales", "Caja Eléctrica Metálica 4x4 o 4-11/16", "4x4 or 4-11/16 Metal Box", 4.5, "unidad"),
            ("Materiales", "Detector de Humo / Monóxido (Hardwired con batería)", "Smoke / CO Detector (Hardwired w/ Battery Backup)", 65.0, "unidad"),
            ("Materiales", "Lote Conectores, Coples y Abrazaderas EMT", "EMT Fittings & Straps (Lot)", 45.0, "lote"),
            ("Materiales", "Consumibles (Cinta, Wire Nuts, Pijas, Taquetes)", "Consumables (Tape, Wire Nuts, Screws)", 35.0, "lote"),
            
            # 7. HVAC, MECÁNICA, MANTENIMIENTO Y CONSTRUCCIÓN
            ("Mantenimiento", "Mantenimiento Preventivo A/C Comercial", "Commercial A/C Preventative Maintenance", 150.0, "servicio"),
            ("Mantenimiento", "Recarga de Refrigerante A/C (por libra)", "A/C Refrigerant Recharge (per lb)", 45.0, "libra"),
            ("Mantenimiento", "Sustitución de Banda / Polea / Balero de Equipo", "Equipment Belt / Pulley / Bearing Replacement", 130.0, "servicio"),
            ("Mantenimiento", "Reparación o ajuste mecánico general de piezas", "General Mechanical Part Repair / Adjustment", 110.0, "servicio"),
            ("Construcción", "Reparación de Tablaroca (Parche 2x2 con acabado)", "Drywall Patch & Repair (2x2 finished)", 85.0, "área"),
            ("Construcción", "Reparación de Tablaroca (Panel completo 4x8)", "Drywall Full Sheet Replacement", 180.0, "área"),
            ("Construcción", "Instalación de Tapa de Registro / Access Panel", "Access Panel Installation", 65.0, "unidad"),
            ("Construcción", "Renta de Elevador de Tijera (Scissor Lift) - Día", "Scissor Lift Rental (Daily)", 250.0, "día"),
            ("Construcción", "Base de concreto o soporte antivibratorio para equipo", "Concrete Pad / Equipment Mounting Base", 200.0, "servicio")
        ]
        cursor.executemany('INSERT INTO catalogo (categoria, item_es, item_en, precio_base, unidad) VALUES (?, ?, ?, ?, ?)', items_iniciales)
        conn.commit()
    conn.close()

init_db()

def crear_pdf(cliente, codigo, fecha, subtotal, tax, total, items, is_es):
    pdf = FPDF()
    pdf.add_page()
    
    # --- ENCABEZADO ACTUALIZADO CON LA DIRECCIÓN CORRECTA (Foxbrick) ---
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 8, txt="R.D. Avendano Solution", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, txt="7150 Foxbrick Ln, Apt 4105, Humble, TX 77338", ln=True, align='C')
    pdf.cell(200, 5, txt="Tel: (346) 333-5819 | Email: ricardodario.a@gmail.com", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    titulo = "PRESUPUESTO DE SERVICIO" if is_es else "SERVICE ESTIMATE"
    pdf.cell(200, 8, txt=titulo, ln=True, align='C')
    
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 6, txt=f"Fecha / Date: {fecha} | Ref: {codigo}", ln=True, align='R')
    pdf.cell(200, 6, txt=f"Cliente / Client: {cliente}", ln=True, align='L')
    pdf.ln(5)
    
    pdf.set_fill_color(220, 230, 242) # Ajustado al color elegante de facturas
    pdf.set_font("Arial", 'B', 10)
    h_desc = "Descripción de los Trabajos / Materiales" if is_es else "Job / Material Description"
    h_cant = "Cant" if is_es else "Qty"
    h_precio = "Precio U." if is_es else "Unit Price"
    pdf.cell(105, 8, h_desc, border=1, fill=True)
    pdf.cell(15, 8, h_cant, border=1, align='C', fill=True)
    pdf.cell(35, 8, h_precio, border=1, align='C', fill=True)
    pdf.cell(35, 8, "Subtotal", border=1, align='C', fill=True)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    for item in items:
        desc = item['descripcion'][:55] + "..." if len(item['descripcion']) > 55 else item['descripcion']
        pdf.cell(105, 8, desc, border=1)
        pdf.cell(15, 8, str(item['cantidad']), border=1, align='C')
        pdf.cell(35, 8, f"${item['precio_unitario']:.2f}", border=1, align='C')
        pdf.cell(35, 8, f"${item['subtotal']:.2f}", border=1, align='C')
        pdf.ln()
        
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    t_tax = "Impuestos (Tax):" if is_es else "Taxes:"
    pdf.cell(155, 7, "Subtotal:", align='R')
    pdf.cell(35, 7, f"${subtotal:.2f}", ln=True, align='R', border=1)
    pdf.cell(155, 7, t_tax, align='R')
    pdf.cell(35, 7, f"${tax:.2f}", ln=True, align='R', border=1)
    pdf.set_fill_color(200, 255, 200)
    pdf.cell(155, 8, "TOTAL:", align='R')
    pdf.cell(35, 8, f"${total:.2f}", ln=True, align='R', border=1, fill=True)
    
    pdf.ln(8)
    pdf.set_font("Arial", 'I', 9)
    nota = "Gracias por su preferencia. Este presupuesto es válido por 15 días." if is_es else "Thank you for your business. This estimate is valid for 15 days."
    pdf.cell(200, 5, txt=nota, ln=True, align='C')
    
    temp_filename = f"{codigo}.pdf"
    pdf.output(temp_filename)
    with open(temp_filename, "rb") as f:
        pdf_bytes = f.read()
    os.remove(temp_filename)
    return pdf_bytes

st.set_page_config(page_title="Presupuestos - R.D. Avendano Solution", layout="wide", page_icon="⚡")

# --- INYECCIÓN DE ESTÉTICA PREMIUM (Igual a la de Facturas) ---
estilo_estetico = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@500;700&display=swap');
    
    .stApp {
        background-color: #f1f5f9;
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #1e293b !important;
    }
    
    h1 {
        color: #c97a6e !important;
        font-weight: 700 !important;
    }
    
    /* Botones estilizados con el color terracota/salmón de la app de facturas */
    .stButton > button, div[data-testid="stFormSubmitButton"] > button, div[data-testid="stDownloadButton"] > button {
        background-color: #c97a6e !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        transition: all 0.2s !important;
        width: 100%;
    }
    .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
        background-color: #b0665a !important;
    }
    
    /* Barra lateral elegante */
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] input {
        background-color: #334155 !important;
        color: white !important;
        border: none !important;
    }
</style>
"""
st.markdown(estilo_estetico, unsafe_allow_html=True)

idioma = st.sidebar.radio("🌐 Idioma del PDF / PDF Language", ["Español", "English"])
is_es = idioma == "Español"

st.title("⚡ R.D. Avendano Solution - Presupuestos")
st.markdown("*Sistema profesional de cotización para servicios eléctricos y mantenimiento.*")

conn = sqlite3.connect("presupuestos_app.db")
cursor = conn.cursor()
cursor.execute("SELECT nombre FROM clientes")
clientes_db = [row[0] for row in cursor.fetchall()]

st.sidebar.header("📋 Datos del Cliente")
nuevo_cliente = st.sidebar.text_input("Agregar nuevo cliente a la BD", placeholder="Nombre o Empresa")
if st.sidebar.button("Guardar Cliente"):
    if nuevo_cliente and nuevo_cliente not in clientes_db:
        cursor.execute("INSERT INTO clientes (nombre) VALUES (?)", (nuevo_cliente,))
        conn.commit()
        st.sidebar.success("¡Cliente guardado!")
        st.rerun()

cursor.execute("SELECT nombre FROM clientes")
clientes_db = [row[0] for row in cursor.fetchall()]

if clientes_db:
    cliente_seleccionado = st.sidebar.selectbox("Seleccionar Cliente Guardado", clientes_db)
    cliente = st.sidebar.text_input("O editar nombre del cliente", value=cliente_seleccionado)
else:
    cliente = st.sidebar.text_input("Nombre / Client Name", "Cliente Comercial LLC")

codigo = f"EST-{datetime.now().strftime('%Y%m%d-%H%M')}"
fecha = datetime.now().strftime('%Y-%m-%d')
tax_rate = st.sidebar.number_input("Impuesto / Tax (%)", value=8.25, step=0.25) / 100

with st.expander("🧮 Herramientas, Calculadoras y Código NEC", expanded=False):
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["🏗️ EMT", "🔌 Watts/Amps", "⚡ Ley Ohm", "📉 Caída Tensión", "⚙️ Motores (HP)", "🔋 Transformadores", "📏 Tubería", "📖 Guía NEC"])
    
    with tab1:
        c1, c2 = st.columns(2)
        pies_tuberia = c1.number_input("Pies de EMT", min_value=0.0, step=10.0)
        precio_tuberia = c1.number_input("Precio por pie", value=2.0)
        horas_labor = c2.number_input("Horas estimadas", min_value=0.0, step=1.0)
        tarifa_hora = c2.number_input("Tarifa por hora", value=85.0)
        if st.button("Calcular EMT"):
            st.info(f"**Material:** ${pies_tuberia * precio_tuberia:.2f} | **Labor:** ${horas_labor * tarifa_hora:.2f} | **Total:** ${(pies_tuberia * precio_tuberia) + (horas_labor * tarifa_hora):.2f}")
            
    with tab2:
        c1, c2, c3 = st.columns(3)
        watts = c1.number_input("Potencia (Watts)", min_value=0, value=1500, step=100)
        volts_carga = c2.selectbox("Voltaje (V)", [120, 208, 240, 277, 480])
        fases = c3.radio("Fases", ["1 Ph", "3 Ph"])
        if st.button("Calcular Amperaje"):
            amps = watts / volts_carga if fases == "1 Ph" else watts / (volts_carga * 1.732)
            st.success(f"🔌 **Corriente:** {amps:.2f} A | 🛡️ **Breaker Recomendado:** {amps * 1.25:.2f} A")

    with tab3:
        opcion_ohm = st.radio("¿Qué buscas?", ["Voltaje", "Corriente", "Resistencia"], horizontal=True)
        c1, c2 = st.columns(2)
        if opcion_ohm == "Voltaje":
            i_val = c1.number_input("Corriente (A)", value=10.0)
            r_val = c2.number_input("Resistencia (Ohmios)", value=12.0)
            st.success(f"⚡ **Voltaje:** {i_val * r_val:.2f} V")
        elif opcion_ohm == "Corriente":
            v_val = c1.number_input("Voltaje (V)", value=120.0)
            r_val = c2.number_input("Resistencia (Ohmios)", value=12.0)
            st.success(f"⚡ **Corriente:** {v_val / r_val:.2f} A")
        else:
            v_val = c1.number_input("Voltaje (V)", value=120.0, key='v2')
            i_val = c2.number_input("Corriente (A)", value=10.0, key='i2')
            if i_val > 0: st.success(f"⚡ **Resistencia:** {v_val / i_val:.2f} Ohmios")

    with tab4:
        c1, c2, c3 = st.columns(3)
        vd_volts = c1.selectbox("Voltaje Sistema", [120, 208, 240, 277, 480], key='vdv')
        vd_fases = c1.radio("Fases", ["1 Ph", "3 Ph"], horizontal=True, key='vdf')
        vd_amps = c2.number_input("Amperaje de Carga", min_value=1.0, value=20.0)
        vd_dist = c2.number_input("Distancia (Pies)", min_value=1.0, value=100.0)
        vd_mat = c3.radio("Material del Cable", ["Cobre (Cu)", "Aluminio (Al)"])
        vd_awg = c3.selectbox("Calibre (AWG)", ['14', '12', '10', '8', '6', '4', '3', '2', '1', '1/0', '2/0', '3/0', '4/0'])
        cm_dict = {'14': 4110, '12': 6530, '10': 10380, '8': 16510, '6': 26240, '4': 41740, '3': 52620, '2': 66360, '1': 83690, '1/0': 105600, '2/0': 133100, '3/0': 167800, '4/0': 211600}
        if st.button("Calcular Caída"):
            K = 12.9 if "Cobre" in vd_mat else 21.2
            caida = ((2 if vd_fases == "1 Ph" else 1.732) * K * vd_amps * vd_dist) / cm_dict[vd_awg]
            porcentaje = (caida / vd_volts) * 100
            st.write(f"📉 **Voltaje Perdido:** {caida:.2f} V")
            if porcentaje <= 3.0: st.success(f"✅ **Caída:** {porcentaje:.2f}% (Aceptable NEC)")
            else: st.error(f"⚠️ **Caída:** {porcentaje:.2f}% (Excede 3%)")

    with tab5:
        c1, c2 = st.columns(2)
        hp_val = c1.number_input("Caballos de Fuerza (HP)", min_value=0.5, value=5.0, step=0.5)
        v_motor = c2.selectbox("Voltaje Motor", [120, 208, 230, 460])
        f_motor = c2.radio("Fases Motor", ["1 Ph", "3 Ph"], horizontal=True, key='fm')
        if st.button("Estimar Amps Motor"):
            watts_motor = hp_val * 746
            amps_m = watts_motor / (v_motor * 0.85 * 0.85) if f_motor == "1 Ph" else watts_motor / (v_motor * 1.732 * 0.85 * 0.85)
            st.info(f"⚙️ **Corriente Estimada:** {amps_m:.2f} A")
            
    with tab6:
        st.markdown("**Cálculo de Amperaje de Transformadores (kVA)**")
        c1, c2, c3 = st.columns(3)
        kva_val = c1.number_input("Capacidad (kVA)", min_value=1.0, value=75.0, step=5.0)
        v_trans = c2.selectbox("Voltaje (Primario o Secundario)", [120, 208, 240, 277, 480], index=4)
        f_trans = c3.radio("Fases Transformador", ["1 Ph", "3 Ph"], index=1)
        if st.button("Calcular Amps Transformador"):
            amps_t = (kva_val * 1000) / v_trans if f_trans == "1 Ph" else (kva_val * 1000) / (v_trans * 1.732)
            st.success(f"🔋 **Corriente a Plena Carga (FLA):** {amps_t:.2f} Amperios a {v_trans}V")

    with tab7:
        st.markdown("**Calculadora Rápida de Llenado de Tubería (Conduit Fill - 40% NEC)**")
        c1, c2 = st.columns(2)
        awg_fill = c1.selectbox("Calibre de Cable THHN", ["14", "12", "10", "8", "6", "4"])
        conduit_size = c2.selectbox("Tamaño de Tubería EMT", ["1/2 pulgada", "3/4 pulgada", "1 pulgada", "1 1/4 pulgada"])
        fill_data = {
            "1/2 pulgada": {"14": 12, "12": 9, "10": 5, "8": 3, "6": 1, "4": 1},
            "3/4 pulgada": {"14": 22, "12": 16, "10": 10, "8": 6, "6": 4, "4": 2},
            "1 pulgada": {"14": 35, "12": 26, "10": 16, "8": 9, "6": 7, "4": 4},
            "1 1/4 pulgada": {"14": 61, "12": 45, "10": 29, "8": 16, "6": 12, "4": 7}
        }
        if st.button("Ver Límite NEC"):
            max_cables = fill_data[conduit_size][awg_fill]
            st.info(f"📏 **Límite NEC (40%):** Puedes meter un máximo de **{max_cables} cables THHN #{awg_fill}** en un tubo EMT de {conduit_size}.")

    with tab8:
        st.markdown(
            "### 📖 Guía de Referencia Rápida del Código NEC\n"
            "* **Ampacidad (NEC 310.16):** La temperatura y aislamiento determinan el amperaje máximo. No exceder 75°C en equipo comercial.\n"
            "* **Carga Continua (NEC 210.19 / 215.2):** Circuitos $\ge 3$ horas se calculan al $125\%$.\n"
            "* **Llenado de Cajas (Box Fill 314.16):** Volumen mínimo requerido por cable (ej. 2.25 in³ para #12 AWG). Caja 4x4x1.5 = máx 9 cables #12.\n"
            "* **Soportes para EMT (NEC 358.30):** Asegurar a un máximo de 3 pies (90 cm) de cada caja de conexión, y cada 10 pies (3 m) en línea recta.\n"
            "* **Desconexión de Motores (NEC 430.102):** El desconectador debe estar a la vista (a no más de 50 pies / 15 m) del motor.\n"
            "* **Espacio de Trabajo (NEC 110.26):** Para 120/250V: mínimo 3 pies al frente. Para 277/480V: 3 pies (Cond 1 - pared aislada), 3.5 pies (Cond 2 - muro aterrizado), o 4 pies (Cond 3 - equipo vivo enfrentado).\n"
            "* **Puesta a Tierra (NEC 250.66):** El calibre del Electrodo de Puesta a Tierra (GEC) se basa en el cable principal de acometida.\n"
            "* **Protección GFCI (NEC 210.8):** Obligatorio en áreas comerciales húmedas (techos, cocinas, baños, exteriores).\n"
            "* **Caída de Tensión:** Máximo recomendado $3\%$ en circuito derivado, $5\%$ sumando el alimentador."
        )

st.markdown("---")
st.subheader("🛒 Construir Presupuesto")

df_catalogo = pd.read_sql_query("SELECT * FROM catalogo", conn)
df_catalogo['display'] = df_catalogo['categoria'] + " - " + df_catalogo['item_es'] + " / " + df_catalogo['item_en']

items_seleccionados = st.multiselect("Busca materiales o mano de obra (bilingüe):", df_catalogo['display'].tolist(), key="selector_items")

filas = []
subtotal_gen = 0.0

if items_seleccionados:
    st.markdown("### 📝 Ajuste de Cantidades, Precios y Descripciones")
    for i, item in enumerate(items_seleccionados):
        row = df_catalogo[df_catalogo['display'] == item].iloc[0]
        c1, c2, c3, c4 = st.columns([4, 2, 2, 2])
        
        default_desc = row['item_es'] if is_es else row['item_en']
        
        desc = c1.text_input(f"Concepto {i+1}", value=default_desc, key=f"d_{i}_{is_es}")
        cant = c2.number_input(f"Cant ({row['unidad']})", min_value=0.5, value=1.0, step=0.5, key=f"c_{i}")
        precio = c3.number_input("Precio U. ($)", value=float(row['precio_base']), step=5.0, key=f"p_{i}")
        
        sub = cant * precio
        subtotal_gen += sub
        c4.metric("Subtotal", f"${sub:.2f}")
        
        filas.append({"descripcion": desc, "cantidad": cant, "precio_unitario": precio, "subtotal": sub})

with st.expander("➕ Agregar un concepto personalizado o extra"):
    c_l1, c_l2, c_l3, c_l4 = st.columns([4, 2, 2, 1])
    custom_desc = c_l1.text_input("Descripción extra", placeholder="Ej: Trabajo especial")
    custom_cant = c_l2.number_input("Cantidad", min_value=0.5, value=1.0, step=0.5, key="c_extra")
    custom_precio = c_l3.number_input("Precio U. ($)", min_value=0.0, value=50.0, step=5.0, key="p_extra")
    if c_l4.button("Añadir") and custom_desc:
        st.session_state[f"extra_{custom_desc}"] = {"desc": custom_desc, "cant": custom_cant, "precio": custom_precio}
        st.rerun()

extras_a_borrar = []
for key, val in list(st.session_state.items()):
    if key.startswith("extra_"):
        sub_extra = val["cant"] * val["precio"]
        subtotal_gen += sub_extra
        ex_c1, ex_c2, ex_c3, ex_c4, ex_c5 = st.columns([3, 2, 2, 2, 1])
        ex_c1.write(f"📌 **Extra:** {val['desc']}")
        ex_c2.write(f"Cant: {val['cant']}")
        ex_c3.write(f"Precio U: ${val['precio']:.2f}")
        ex_c4.metric("Subtotal", f"${sub_extra:.2f}")
        if ex_c5.button("❌", key=f"del_{key}"):
            extras_a_borrar.append(key)
        filas.append({"descripcion": val['desc'], "cantidad": val['cant'], "precio_unitario": val['precio'], "subtotal": sub_extra})

if extras_a_borrar:
    for k in extras_a_borrar:
        del st.session_state[k]
    st.rerun()

if filas:
    monto_tax = subtotal_gen * tax_rate
    total_final = subtotal_gen + monto_tax
    
    st.markdown("---")
    st.markdown("### 📊 Resumen Financiero")
    c_res1, c_res2, c_res3 = st.columns(3)
    c_res1.info(f"**Subtotal:** ${subtotal_gen:,.2f}")
    c_res2.warning(f"**Tax ({(tax_rate*100):.2f}%):** ${monto_tax:,.2f}")
    c_res3.success(f"**TOTAL:** ${total_final:,.2f}")
    
    pdf_bytes = crear_pdf(cliente, codigo, fecha, subtotal_gen, monto_tax, total_final, filas, is_es)
    
    st.markdown("---")
    st.subheader("👁️ Previsualización del Documento en PDF")
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    b64 = base64.b64encode(pdf_bytes).decode()
    st.markdown("<br>", unsafe_allow_html=True)
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{codigo}.pdf"><button style="width:100%; padding:15px; background-color:#c97a6e; color:white; font-size:18px; font-weight:bold; border:none; border-radius:8px; cursor:pointer;">📥 DESCARGAR PRESUPUESTO EN PDF</button></a>'
    st.markdown(href, unsafe_allow_html=True)
conn.close()

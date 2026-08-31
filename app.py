import streamlit.components.v1 as components
import streamlit as st

st.set_page_config(page_title="R.D. Avendano Solutions", layout="wide")

# Ocultar marcos de Streamlit para pantalla completa en celular
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.stApp { background-color: #f1f5f9; padding: 0px !important; }
iframe { width: 100% !important; border: none; -webkit-overflow-scrolling: touch; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <!-- Esta línea es la que soluciona los saltos y el zoom automático en el iPhone -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
    <title>Generador de Facturas - R.D. Avendano Solutions</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root { --accent-color: #c97a6e; --text-main: #1e293b; --text-muted: #64748b; --border-color: #e2e8f0; --bg-color: #ffffff; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', sans-serif; background-color: #f1f5f9; color: var(--text-main); padding: 10px; -webkit-text-size-adjust: 100%; }
        
        @media print { 
            body { background-color: transparent; padding: 0; } 
            .no-print { display: none !important; } 
            .invoice-box { box-shadow: none !important; margin: 0 !important; padding: 5px !important; width: 100% !important; } 
            @page { margin: 0.5cm; } 
        }

        .toolbar { max-width: 900px; margin: 0 auto 15px auto; background: #1e293b; padding: 10px; border-radius: 8px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: space-between; align-items: center; }
        .toolbar-group { display: flex; flex-wrap: wrap; gap: 6px; }
        button { background-color: var(--accent-color); color: white; border: none; padding: 8px 10px; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 12px; }
        button.secondary { background-color: #334155; }
        button.save { background-color: #10b981; }
        button.next { background-color: #3b82f6; }

        .invoice-box { max-width: 900px; margin: 0 auto; background: var(--bg-color); padding: 25px; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }
        
        [contenteditable="true"] { outline: none; border-radius: 4px; padding: 2px 4px; min-height: 20px; transition: background 0.2s; }
        [contenteditable="true"]:focus { background-color: rgba(201, 122, 110, 0.08); box-shadow: 0 0 0 2px rgba(201, 122, 110, 0.2); }

        header { display: flex; flex-direction: column; gap: 10px; border-bottom: 2px solid var(--border-color); padding-bottom: 15px; margin-bottom: 20px; }
        @media(min-width: 600px) { header { flex-direction: row; justify-content: space-between; } }
        
        .company-info h1 { font-family: 'Space Grotesk', sans-serif; font-size: 22px; letter-spacing: -0.5px; }
        .company-info .company-details { color: var(--text-muted); font-size: 12px; line-height: 1.4; }
        .invoice-title h2 { font-family: 'Space Grotesk', sans-serif; font-size: 28px; color: var(--accent-color); text-align: left; }
        @media(min-width: 600px) { .invoice-title h2 { text-align: right; } }

        .meta-section { display: flex; flex-direction: column; gap: 15px; margin-bottom: 20px; }
        @media(min-width: 600px) { .meta-section { flex-direction: row; justify-content: space-between; } }
        
        .bill-to { background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid var(--border-color); width: 100%; }
        @media(min-width: 600px) { .bill-to { width: 55%; } }
        .bill-to h3 { font-size: 11px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px; }
        
        select.client-selector { width: 100%; padding: 6px; margin-bottom: 10px; font-size: 12px; border-radius: 4px; border: 1px solid var(--border-color); }
        .client-details { font-size: 13px; font-weight: 500; line-height: 1.4; min-height: 40px; }
        
        .invoice-details table { width: 100%; font-size: 13px; }
        @media(min-width: 600px) { .invoice-details table { width: auto; margin-left: auto; } }
        .invoice-details td { padding: 4px; }
        .invoice-details td:first-child { color: var(--text-muted); }
        .invoice-details td:last-child { font-weight: 600; text-align: right; }

        .table-responsive { width: 100%; overflow-x: auto; margin-bottom: 20px; }
        .items-table { width: 100%; border-collapse: collapse; min-width: 450px; }
        .items-table th { background: #f8fafc; padding: 8px; font-size: 11px; color: var(--text-muted); text-transform: uppercase; border-bottom: 2px solid var(--border-color); text-align: left; }
        .items-table td { padding: 10px 8px; border-bottom: 1px solid var(--border-color); font-size: 13px; }
        .items-table td.center { text-align: center; } 
        .items-table td.right { text-align: right; }

        .footer-section { display: flex; flex-direction: column; gap: 15px; }
        @media(min-width: 600px) { .footer-section { flex-direction: row; justify-content: space-between; } }
        
        .payment-info { background: #f8fafc; padding: 15px; border-radius: 8px; border-left: 4px solid var(--accent-color); border: 1px solid var(--border-color); border-left-width: 4px; width: 100%; }
        @media(min-width: 600px) { .payment-info { width: 55%; } }
        .payment-info h4 { font-size: 11px; margin-bottom: 4px; } 
        .payment-info p { font-size: 12px; color: var(--text-muted); line-height: 1.4; }
        select.terms-selector { width: 100%; font-size: 11px; padding: 4px; margin-bottom: 8px; border-radius: 4px; border: 1px solid var(--border-color); }

        .totals { width: 100%; }
        @media(min-width: 600px) { .totals { width: 40%; } }
        .totals table { width: 100%; font-size: 13px; } 
        .totals td { padding: 6px 0; text-align: right; }
        .totals tr.total-due td { font-size: 16px; font-weight: 700; color: var(--accent-color); border-top: 2px solid var(--border-color); padding-top: 10px; }
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <div class="toolbar-group">
            <button class="secondary" onclick="setLanguage('es')">🇪🇸 ES</button>
            <button class="secondary" onclick="setLanguage('en')">🇺🇸 EN</button>
            <button class="secondary" onclick="addRow()">+ Fila</button>
        </div>
        <div class="toolbar-group">
            <button class="save" onclick="guardarCliente()">💾 Guardar Cliente</button>
            <button class="next" onclick="avanzarFactura()">✅ Siguiente Factura</button>
            <button onclick="window.print()">🖨️ PDF</button>
        </div>
    </div>

    <div class="invoice-box" id="invoice-content">
        <header>
            <div class="company-info">
                <h1>R.D. AVENDANO SOLUTIONS</h1>
                <div class="company-details">
                    <div><span id="lbl-id" contenteditable="true">Identificación</span>: Ricardo Avendano</div>
                    <div><span id="lbl-phone" contenteditable="true">Teléfono</span>: +1 346 333 5819 | <span id="lbl-email" contenteditable="true">Correo</span>: ricardodario.a@gmail.com</div>
                    <div id="company-address" contenteditable="true">7150 Foxbrick Ln, Apt 4105, Humble, TX 77338</div>
                </div>
            </div>
            <div class="invoice-title">
                <h2 id="lbl-invoice-title" contenteditable="true">FACTURA</h2>
            </div>
        </header>

        <div class="meta-section">
            <div class="bill-to">
                <h3 id="lbl-bill-to" contenteditable="true">Facturar a:</h3>
                <select id="client-selector" class="client-selector no-print" onchange="cargarCliente()">
                    <option value="">-- Base de Datos de Clientes --</option>
                </select>
                <div class="client-details" contenteditable="true" id="client-name">Nombre de la Empresa o Cliente<br>Dirección, TX</div>
            </div>
            <div class="invoice-details">
                <table>
                    <tr><td id="lbl-inv-no" contenteditable="true">Nº de Factura:</td><td contenteditable="true" id="invoice-number"></td></tr>
                    <tr><td id="lbl-date" contenteditable="true">Fecha:</td><td contenteditable="true" id="invoice-date"></td></tr>
                </table>
            </div>
        </div>

        <div class="table-responsive">
            <table class="items-table" id="table-body">
                <thead>
                    <tr>
                        <th style="width: 30px;" class="center">#</th>
                        <th id="lbl-desc" contenteditable="true">Descripción</th>
                        <th style="width: 60px;" class="center" id="lbl-qty" contenteditable="true">Cant.</th>
                        <th style="width: 80px;" class="right" id="lbl-price" contenteditable="true">Precio</th>
                        <th style="width: 80px;" class="right" id="lbl-amount" contenteditable="true">Importe</th>
                        <th style="width: 30px;" class="center no-print"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="center">1</td>
                        <td class="item-desc" contenteditable="true" onblur="formatSentenceCase(this)">Servicio eléctrico general</td>
                        <td class="center qty" contenteditable="true" oninput="calc()">1</td>
                        <td class="right price" contenteditable="true" oninput="calc()">150.00</td>
                        <td class="right amount">150.00</td>
                        <td class="center no-print">
                            <button type="button" onclick="deleteRow(this)" style="background: #ef4444; color: white; border: none; width: 22px; height: 22px; border-radius: 4px;">&times;</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="footer-section">
            <div class="payment-info">
                <h4 id="lbl-terms-title" contenteditable="true">Términos de Pago:</h4>
                <select id="terms-selector" class="terms-selector no-print" onchange="insertarTermino()">
                    <option value="">-- Autocompletar --</option>
                    <option value="receipt">Pago inmediato</option>
                    <option value="net15">A 15 días</option>
                    <option value="net30">A 30 días</option>
                    <option value="completion">Al finalizar</option>
                    <option value="half">50% y 50%</option>
                </select>
                <p id="lbl-terms-desc" contenteditable="true">Pagadero al recibir esta factura. Agradecemos su pronto pago.</p>
                
                <h4 id="lbl-methods-title" style="margin-top:10px;" contenteditable="true">Métodos Aceptados:</h4>
                <p id="lbl-methods-desc" contenteditable="true">- Zelle<br>- Cheque (Ricardo Avendano)<br>- Efectivo</p>
            </div>
            <div class="totals">
                <table>
                    <tr><td id="lbl-subtotal" contenteditable="true">Subtotal:</td><td>$<span id="val-subtotal">150.00</span></td></tr>
                    <tr><td id="lbl-tax" contenteditable="true">Impuestos (8.25%):</td><td contenteditable="true" id="val-tax" oninput="calcTax()">12.38</td></tr>
                    <tr class="total-due"><td id="lbl-total" contenteditable="true">TOTAL:</td><td>$<span id="val-total">162.38</span></td></tr>
                </table>
            </div>
        </div>
    </div>

    <script>
        let currentLang = 'es';

        window.onload = function() {
            // Fecha Automática
            const hoy = new Date();
            document.getElementById('invoice-date').innerText = hoy.toLocaleDateString('es-ES', {year: 'numeric', month: 'long', day: 'numeric'});
            
            // Secuencia Automática de Factura
            let currentSeq = localStorage.getItem('rd_secuencia_factura') || 1;
            document.getElementById('invoice-number').innerText = hoy.getFullYear() + "-" + String(currentSeq).padStart(3, '0');

            // Cargar base de datos de clientes
            actualizarListaClientes();
            calc();
        };

        // Función para guardar clientes en el celular
        function guardarCliente() {
            let nombre = prompt("Ingresa el nombre del cliente para guardarlo en tu lista:");
            if (nombre) {
                let detalles = document.getElementById('client-name').innerHTML;
                let bdClientes = JSON.parse(localStorage.getItem('rd_clientes_db')) || {};
                bdClientes[nombre] = detalles;
                localStorage.setItem('rd_clientes_db', JSON.stringify(bdClientes));
                alert("Cliente '" + nombre + "' guardado con éxito.");
                actualizarListaClientes();
            }
        }

        // Mostrar clientes en el menú
        function actualizarListaClientes() {
            let selector = document.getElementById('client-selector');
            selector.innerHTML = '<option value="">-- Base de Datos de Clientes --</option>';
            let bdClientes = JSON.parse(localStorage.getItem('rd_clientes_db')) || {};
            for (let nombre in bdClientes) {
                let opt = document.createElement('option');
                opt.value = bdClientes[nombre];
                opt.innerText = nombre;
                selector.appendChild(opt);
            }
        }

        // Cargar datos al seleccionar cliente
        function cargarCliente() {
            let selector = document.getElementById('client-selector');
            if(selector.value) {
                document.getElementById('client-name').innerHTML = selector.value;
            }
        }

        // Avanzar el número automáticamente
        function avanzarFactura() {
            if(confirm("¿Seguro que deseas avanzar al siguiente número de factura? Esto limpiará la pantalla actual.")) {
                let currentSeq = parseInt(localStorage.getItem('rd_secuencia_factura') || 1);
                localStorage.setItem('rd_secuencia_factura', currentSeq + 1);
                location.reload(); // Recarga la página y suma 1
            }
        }

        const standardTerms = {
            receipt: "Pagadero al recibir esta factura. Agradecemos su pronto pago.",
            net15: "Neto 15 días. El pago debe efectuarse en un plazo de 15 días.",
            net30: "Neto 30 días. El pago debe efectuarse en un plazo de 30 días.",
            completion: "El pago debe realizarse al finalizar el trabajo.",
            half: "50% de anticipo, 50% restante al finalizar."
        };

        function formatSentenceCase(el) {
            let text = el.innerText.trim();
            if (text.length > 0) { el.innerText = text.charAt(0).toUpperCase() + text.slice(1).toLowerCase(); }
        }

        function insertarTermino() {
            const selector = document.getElementById('terms-selector');
            if(selector.value) {
                document.getElementById('lbl-terms-desc').innerText = standardTerms[selector.value];
                selector.value = ""; 
            }
        }

        function addRow() {
            const tbody = document.querySelector('#table-body tbody');
            const tr = document.createElement('tr');
            tr.innerHTML = `<td class="center">${tbody.rows.length + 1}</td>
                <td class="item-desc" contenteditable="true" onblur="formatSentenceCase(this)"></td>
                <td class="center qty" contenteditable="true" oninput="calc()">1</td>
                <td class="right price" contenteditable="true" oninput="calc()">0.00</td>
                <td class="right amount">0.00</td>
                <td class="center no-print">
                    <button type="button" onclick="deleteRow(this)" style="background: #ef4444; color: white; border: none; width: 22px; height: 22px; border-radius: 4px;">&times;</button>
                </td>`;
            tbody.appendChild(tr);
            calc();
        }

        function deleteRow(btn) {
            const tbody = document.querySelector('#table-body tbody');
            if (tbody.rows.length <= 1) { return alert("Debe haber al menos un concepto."); }
            btn.closest('tr').remove();
            document.querySelectorAll('#table-body tbody tr').forEach((row, index) => {
                row.querySelector('td.center').innerText = index + 1;
            });
            calc();
        }

        function calc() {
            let sub = 0;
            document.querySelectorAll('#table-body tbody tr').forEach(row => {
                let q = parseFloat(row.querySelector('.qty').innerText) || 0;
                let p = parseFloat(row.querySelector('.price').innerText) || 0;
                row.querySelector('.amount').innerText = (q*p).toFixed(2);
                sub += (q*p);
            });
            document.getElementById('val-subtotal').innerText = sub.toFixed(2);
            let taxInput = parseFloat(document.getElementById('val-tax').innerText);
            let tax = isNaN(taxInput) ? sub * 0.0825 : taxInput;
            document.getElementById('val-total').innerText = (sub + tax).toFixed(2);
        }

        function calcTax() {
            let sub = parseFloat(document.getElementById('val-subtotal').innerText) || 0;
            let tax = parseFloat(document.getElementById('val-tax').innerText) || 0;
            document.getElementById('val-total').innerText = (sub + tax).toFixed(2);
        }

        function setLanguage(lang) {
            currentLang = lang;
            if (lang === 'en') {
                document.getElementById('lbl-invoice-title').innerText = "INVOICE";
                document.getElementById('lbl-bill-to').innerText = "Bill To:";
                document.getElementById('lbl-inv-no').innerText = "Invoice No:";
                document.getElementById('lbl-date').innerText = "Date:";
                document.getElementById('lbl-desc').innerText = "Description";
                document.getElementById('lbl-qty').innerText = "Qty";
                document.getElementById('lbl-price').innerText = "Price";
                document.getElementById('lbl-amount').innerText = "Amount";
                document.getElementById('lbl-terms-title').innerText = "Payment Terms:";
                document.getElementById('lbl-methods-title').innerText = "Accepted Methods:";
                document.getElementById('lbl-methods-desc').innerHTML = "- Zelle<br>- Check (Ricardo Avendano)<br>- Cash";
                document.getElementById('lbl-subtotal').innerText = "Subtotal:";
                document.getElementById('lbl-tax').innerText = "Tax (8.25%):";
                document.getElementById('lbl-total').innerText = "TOTAL:";
            } else {
                location.reload();
            }
        }
    </script>
</body>
</html>
"""

# Configurar un alto generoso para que en el celular deslices toda la página y no se trabe el marco
components.html(html_code, height=1400, scrolling=False)

import streamlit.components.v1 as components
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="R.D. Avendano Solutions - Facturas", layout="wide")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background-color: #f1f5f9; padding-top: 0px; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Generador de Facturas - R.D. Avendano Solutions</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root { --accent-color: #c97a6e; --text-main: #1e293b; --text-muted: #64748b; --border-color: #e2e8f0; --bg-color: #ffffff; --hover-bg: #f8fafc; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', sans-serif; background-color: #f1f5f9; color: var(--text-main); line-height: 1.6; padding: 20px; }
        
        @media print { 
            body { background-color: transparent; padding: 0; } 
            .no-print { display: none !important; } 
            .invoice-box { box-shadow: none !important; margin: 0 !important; padding: 10px !important; width: 100% !important; max-width: 100% !important; } 
            @page { margin: 1cm; } 
        }

        .toolbar { max-width: 900px; margin: 0 auto 20px auto; background: #1e293b; padding: 12px 24px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; color: white; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        button { background-color: var(--accent-color); color: white; border: none; padding: 9px 16px; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 13px; margin-left: 5px; transition: background 0.2s; }
        button:hover { background-color: #b0665a; }
        button.secondary { background-color: #334155; }
        button.secondary:hover { background-color: #475569; }

        .invoice-box { max-width: 900px; margin: 0 auto; background: var(--bg-color); padding: 50px; border-radius: 12px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); }
        
        [contenteditable="true"] { outline: none; border-radius: 4px; transition: all 0.2s; padding: 2px 4px; }
        [contenteditable="true"]:hover { background-color: rgba(201, 122, 110, 0.04); }
        [contenteditable="true"]:focus { background-color: rgba(201, 122, 110, 0.08); box-shadow: 0 0 0 2px rgba(201, 122, 110, 0.2); }

        header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 35px; border-bottom: 2px solid var(--border-color); padding-bottom: 25px; }
        .company-info { display: flex; flex-direction: column; gap: 4px; }
        .company-info h1 { font-family: 'Space Grotesk', sans-serif; font-size: 24px; color: var(--text-main); letter-spacing: -0.5px; margin-bottom: 4px; }
        .company-info .company-details { color: var(--text-muted); font-size: 13px; line-height: 1.5; }
        
        .invoice-title-container { text-align: right; }
        .invoice-title h2 { font-family: 'Space Grotesk', sans-serif; font-size: 36px; color: var(--accent-color); letter-spacing: 1px; line-height: 1.1; }

        .meta-section { display: flex; justify-content: space-between; margin-bottom: 35px; gap: 20px; }
        .bill-to { width: 55%; background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid var(--border-color); }
        .bill-to h3 { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; font-weight: 600; }
        .bill-to .client-details { font-size: 14px; font-weight: 500; min-height: 50px; color: var(--text-main); line-height: 1.5; }
        
        .invoice-details { text-align: right; display: flex; flex-direction: column; justify-content: center; }
        .invoice-details table { margin-left: auto; }
        .invoice-details td { padding: 6px 0 6px 20px; font-size: 14px; }
        .invoice-details td:first-child { color: var(--text-muted); font-weight: 500; }
        .invoice-details td:last-child { font-weight: 600; color: var(--text-main); }

        .items-table { width: 100%; border-collapse: collapse; margin-bottom: 35px; }
        .items-table th { background: #f8fafc; padding: 12px 16px; font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 2px solid var(--border-color); text-align: left; font-weight: 600; }
        .items-table td { padding: 16px; border-bottom: 1px solid var(--border-color); font-size: 14px; }
        .items-table td.center { text-align: center; } 
        .items-table td.right { text-align: right; }

        .footer-section { display: flex; justify-content: space-between; margin-top: 20px; gap: 30px; }
        .payment-info { width: 55%; background: #f8fafc; padding: 20px; border-left: 4px solid var(--accent-color); border-radius: 8px; border: 1px solid var(--border-color); border-left-width: 4px; }
        .payment-info h4 { font-size: 12px; color: var(--text-main); margin-bottom: 6px; font-weight: 600; } 
        .payment-info p { font-size: 13px; color: var(--text-muted); line-height: 1.5; }
        .terms-selector { font-size: 11px; padding: 4px 8px; border: 1px solid var(--border-color); border-radius: 4px; background: white; font-family: inherit; cursor: pointer; color: var(--text-main); margin-bottom: 8px; }

        .totals { width: 40%; }
        .totals table { width: 100%; } 
        .totals td { padding: 8px 0; text-align: right; font-size: 14px; }
        .totals td:first-child { color: var(--text-muted); font-weight: 500; }
        .totals td:last-child { font-weight: 600; color: var(--text-main); }
        .totals tr.total-due { border-top: 2px solid var(--border-color); }
        .totals tr.total-due td { font-size: 18px; font-weight: 700; color: var(--accent-color); padding-top: 12px; }

        .thank-you { text-align: center; margin-top: 50px; color: var(--text-muted); font-size: 14px; font-weight: 500; border-top: 1px solid var(--border-color); padding-top: 25px; }
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <div style="display: flex; align-items: center;">
            <button class="secondary" onclick="setLanguage('es')">🇪🇸 ES</button>
            <button class="secondary" onclick="setLanguage('en')">🇺🇸 EN</button>
            <button class="secondary" onclick="addRow()">+ Fila</button>
        </div>
        <div>
            <button onclick="window.print()">🖨️ Imprimir / Guardar PDF</button>
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
            <div class="invoice-title-container">
                <div class="invoice-title"><h2 id="lbl-invoice-title" contenteditable="true">FACTURA</h2></div>
            </div>
        </header>

        <div class="meta-section">
            <div class="bill-to">
                <h3 id="lbl-bill-to" contenteditable="true">Facturar a:</h3>
                <div class="client-details" contenteditable="true" id="client-name">Nombre del Cliente<br>Dirección y Ciudad, Estado</div>
            </div>
            <div class="invoice-details">
                <table>
                    <tr><td id="lbl-inv-no" contenteditable="true">Nº de Factura:</td><td contenteditable="true" id="invoice-number">2026-001</td></tr>
                    <tr><td id="lbl-date" contenteditable="true">Fecha:</td><td contenteditable="true" id="invoice-date"></td></tr>
                </table>
            </div>
        </div>

        <table class="items-table" id="table-body">
            <thead>
                <tr>
                    <th style="width: 40px;" class="center">#</th>
                    <th id="lbl-desc" contenteditable="true">Descripción</th>
                    <th style="width: 80px;" class="center" id="lbl-qty" contenteditable="true">Cant.</th>
                    <th style="width: 100px;" class="right" id="lbl-price" contenteditable="true">Precio</th>
                    <th style="width: 100px;" class="right" id="lbl-amount" contenteditable="true">Importe</th>
                    <th style="width: 40px;" class="center no-print"></th>
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
                        <button type="button" onclick="deleteRow(this)" style="background: #ef4444; color: white; border: none; border-radius: 4px; width: 22px; height: 22px; cursor: pointer; font-weight: bold;">&times;</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="footer-section">
            <div class="payment-info">
                <h4 id="lbl-terms-title" contenteditable="true">Términos de Pago:</h4>
                <select id="terms-selector" class="terms-selector no-print" onchange="insertarTermino()">
                    <option id="opt-0" value="">-- Autocompletar condiciones --</option>
                    <option id="opt-1" value="receipt">Pago inmediato</option>
                    <option id="opt-2" value="net15">A 15 días</option>
                    <option id="opt-3" value="net30">A 30 días</option>
                    <option id="opt-4" value="completion">Al finalizar</option>
                    <option id="opt-5" value="half">50% y 50%</option>
                </select>
                <p id="lbl-terms-desc" contenteditable="true">Pagadero al recibir esta factura. Agradecemos su pronto pago.</p>
                
                <h4 id="lbl-methods-title" style="margin-top:15px;" contenteditable="true">Métodos Aceptados:</h4>
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
        <div class="thank-you" id="lbl-thanks" contenteditable="true">¡Gracias por su preferencia!</div>
    </div>

    <script>
        let currentLang = 'es';

        window.onload = function() {
            const hoy = new Date();
            const dateField = document.getElementById('invoice-date');
            dateField.innerText = hoy.toLocaleDateString('es-ES', {year: 'numeric', month: 'long', day: 'numeric'});
            calc();
        };

        const i18n = {
            es: { 
                title: "FACTURA", billTo: "Facturar a:", invNo: "Nº de Factura:", date: "Fecha:", desc: "Descripción", qty: "Cant.", price: "Precio", amount: "Importe",
                id: "Identificación", phone: "Teléfono", email: "Correo", termsTitle: "Términos de Pago:", methodsTitle: "Métodos Aceptados:", 
                methodsDesc: "- Zelle<br>- Cheque (Ricardo Avendano)<br>- Efectivo",
                subtotal: "Subtotal:", tax: "Impuestos (8.25%):", total: "TOTAL:", thanks: "¡Gracias por su preferencia!",
                opt0: "-- Autocompletar condiciones --", opt1: "Pago inmediato", opt2: "A 15 días", opt3: "A 30 días", opt4: "Al finalizar", opt5: "50% y 50%"
            },
            en: { 
                title: "INVOICE", billTo: "Bill To:", invNo: "Invoice No:", date: "Date:", desc: "Description", qty: "Qty", price: "Price", amount: "Amount",
                id: "ID", phone: "Phone", email: "Email", termsTitle: "Payment Terms:", methodsTitle: "Accepted Methods:", 
                methodsDesc: "- Zelle<br>- Check (Ricardo Avendano)<br>- Cash",
                subtotal: "Subtotal:", tax: "Tax (8.25%):", total: "TOTAL:", thanks: "Thank you for your business!",
                opt0: "-- Autocomplete terms --", opt1: "Due on receipt", opt2: "Net 15", opt3: "Net 30", opt4: "Upon completion", opt5: "50% and 50%"
            }
        };

        const standardTerms = {
            es: {
                receipt: "Pagadero al recibir esta factura. Agradecemos su pronto pago.",
                net15: "Neto 15 días. El pago debe efectuarse en un plazo de 15 días.",
                net30: "Neto 30 días. El pago debe efectuarse en un plazo de 30 días.",
                completion: "El pago debe realizarse al finalizar el trabajo.",
                half: "50% de anticipo, 50% restante al finalizar."
            },
            en: {
                receipt: "Payable upon receipt of this invoice. We appreciate your prompt payment.",
                net15: "Net 15. Payment is due within 15 days of the invoice date.",
                net30: "Net 30. Payment is due within 30 days of the invoice date.",
                completion: "Payment is due in full upon satisfactory completion of the work.",
                half: "50% deposit to commence work, 50% remaining upon completion."
            }
        };

        function formatSentenceCase(el) {
            let text = el.innerText.trim();
            if (text.length > 0) {
                el.innerText = text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
            }
        }

        function setLanguage(lang) {
            currentLang = lang;
            const t = i18n[lang];
            document.getElementById('lbl-invoice-title').innerText = t.title;
            document.getElementById('lbl-bill-to').innerText = t.billTo;
            document.getElementById('lbl-inv-no').innerText = t.invNo;
            document.getElementById('lbl-date').innerText = t.date;
            document.getElementById('lbl-desc').innerText = t.desc;
            document.getElementById('lbl-qty').innerText = t.qty;
            document.getElementById('lbl-price').innerText = t.price;
            document.getElementById('lbl-amount').innerText = t.amount;
            document.getElementById('lbl-id').innerText = t.id;
            document.getElementById('lbl-phone').innerText = t.phone;
            document.getElementById('lbl-email').innerText = t.email;
            document.getElementById('lbl-terms-title').innerText = t.termsTitle;
            document.getElementById('lbl-methods-title').innerText = t.methodsTitle;
            document.getElementById('lbl-methods-desc').innerHTML = t.methodsDesc;
            document.getElementById('lbl-subtotal').innerText = t.subtotal;
            document.getElementById('lbl-tax').innerText = t.tax;
            document.getElementById('lbl-total').innerText = t.total;
            document.getElementById('lbl-thanks').innerText = t.thanks;
            document.getElementById('opt-0').innerText = t.opt0;
            document.getElementById('opt-1').innerText = t.opt1;
            document.getElementById('opt-2').innerText = t.opt2;
            document.getElementById('opt-3').innerText = t.opt3;
            document.getElementById('opt-4').innerText = t.opt4;
            document.getElementById('opt-5').innerText = t.opt5;
        }

        function insertarTermino() {
            const selector = document.getElementById('terms-selector');
            if(selector.value) {
                document.getElementById('lbl-terms-desc').innerText = standardTerms[currentLang][selector.value];
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
                    <button type="button" onclick="deleteRow(this)" style="background: #ef4444; color: white; border: none; border-radius: 4px; width: 22px; height: 22px; cursor: pointer; font-weight: bold;">&times;</button>
                </td>`;
            tbody.appendChild(tr);
            calc();
        }

        function deleteRow(btn) {
            const tbody = document.querySelector('#table-body tbody');
            if (tbody.rows.length <= 1) {
                alert("Debe mantener al menos una línea en la factura.");
                return;
            }
            const tr = btn.closest('tr');
            tr.remove();
            updateRowNumbers();
            calc();
        }

        function updateRowNumbers() {
            const rows = document.querySelectorAll('#table-body tbody tr');
            rows.forEach((row, index) => {
                row.querySelector('td.center').innerText = index + 1;
            });
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
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=True)

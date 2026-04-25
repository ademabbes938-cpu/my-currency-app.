from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# رابط جلب أسعار الصرف الحية
API_URL = "https://api.exchangerate-api.com/v4/latest/TND"

# القائمة الكاملة لـ 160 عملة بالفرنسية مرتبة أبجدياً
CURRENCIES = {
    "AFN": "Afghani afghan",
    "ALL": "Lek albanais",
    "DZD": "Dinar algérien",
    "EUR": "Euro",
    "AMD": "Dram arménien",
    "AWG": "Florin d'Aruba",
    "AUD": "Dollar australien",
    "AZN": "Manat azerbaïdjanais",
    "BSD": "Dollar bahaméen",
    "BHD": "Dinar bahreïni",
    "BDT": "Taka bangladais",
    "BBD": "Dollar barbadien",
    "BYN": "Rouble biélorusse",
    "BZD": "Dollar bélizien",
    "BMD": "Dollar bermudien",
    "BTN": "Ngultrum bhoutanais",
    "BOB": "Boliviano bolivien",
    "BAM": "Mark convertible bosniaque",
    "BWP": "Pula botswanais",
    "BRL": "Réal brésilien",
    "BND": "Dollar de Brunei",
    "BGN": "Lev bulgare",
    "BIF": "Franc burundais",
    "KHR": "Riel cambodgien",
    "CAD": "Dollar canadien",
    "CVE": "Escudo cap-verdien",
    "KYD": "Dollar des îles Caïmans",
    "XAF": "Franc CFA (BEAC)",
    "XOF": "Franc CFA (BCEAO)",
    "XPF": "Franc CFP",
    "CLP": "Peso chilien",
    "CNY": "Yuan chinois",
    "COP": "Peso colombien",
    "KMF": "Franc comorien",
    "CDF": "Franc congolais",
    "CRC": "Colón costaricain",
    "HRK": "Kuna croate",
    "CUP": "Peso cubain",
    "DKK": "Couronne danoise",
    "DJF": "Franc djiboutien",
    "DOP": "Peso dominicain",
    "XCD": "Dollar des Caraïbes orientales",
    "EGP": "Livre égyptienne",
    "ERN": "Nakfa érythréen",
    "ETB": "Birr éthiopien",
    "FKP": "Livre des îles Malouines",
    "FOK": "Couronne féroïenne",
    "FJD": "Dollar fidjien",
    "GMD": "Dalasi gambien",
    "GEL": "Lari géorgien",
    "GHS": "Cedi ghanéen",
    "GIP": "Livre de Gibraltar",
    "GTQ": "Quetzal guatémaltèque",
    "GGP": "Livre de Guernesey",
    "GNF": "Franc guinéen",
    "GYD": "Dollar guyanien",
    "HTG": "Gourde haïtienne",
    "HNL": "Lempira hondurien",
    "HKD": "Dollar de Hong Kong",
    "HUF": "Forint hongrois",
    "ISK": "Couronne islandaise",
    "INR": "Roupie indienne",
    "IDR": "Roupie indonésienne",
    "IRR": "Rial iranien",
    "IQD": "Dinar irakien",
    "ILS": "Shekel israélien",
    "JMD": "Dollar jamaïcain",
    "JPY": "Yen japonais",
    "JEP": "Livre de Jersey",
    "JOD": "Dinar jordanien",
    "KZT": "Tenge kazakh",
    "KES": "Shilling kényan",
    "KGS": "Som kirghize",
    "KWD": "Dinar koweïtien",
    "LAK": "Kip laotien",
    "LBP": "Livre libanaise",
    "LSL": "Loti lesothan",
    "LRD": "Dollar libérien",
    "LYD": "Dinar libyen",
    "MOP": "Pataca macanaise",
    "MKD": "Denar macédonien",
    "MGA": "Ariary malgache",
    "MWK": "Kwacha malawien",
    "MYR": "Ringgit malais",
    "MVR": "Rufiyaa maldivienne",
    "IMP": "Livre mannoise",
    "MRU": "Ouguiya mauritanienne",
    "MUR": "Roupie mauricienne",
    "MXN": "Peso mexicain",
    "MDL": "Leu moldave",
    "MNT": "Tugrik mongol",
    "MAD": "Dirham marocain",
    "MZN": "Metical mozambicain",
    "MMK": "Kyat birman",
    "NAD": "Dollar namibien",
    "NPR": "Roupie népalaise",
    "ANG": "Florin des Antilles néerlandaises",
    "TWD": "Nouveau dollar taïwanais",
    "NZD": "Dollar néo-zélandais",
    "NIO": "Córdoba nicaraguayen",
    "NGN": "Naira nigérian",
    "NOK": "Couronne norvégienne",
    "OMR": "Rial omanais",
    "PKR": "Roupie pakistanaise",
    "PAB": "Balboa panaméen",
    "PGK": "Kina papouan-guinéen",
    "PYG": "Guaraní paraguayen",
    "PEN": "Sol péruvien",
    "PHP": "Peso philippin",
    "PLN": "Zloty polonais",
    "GBP": "Livre sterling",
    "QAR": "Riyal qatari",
    "RON": "Leu roumain",
    "RUB": "Rouble russe",
    "RWF": "Franc rwandais",
    "SHP": "Livre de Sainte-Hélène",
    "WST": "Tala samoan",
    "STN": "Dobra santoméen",
    "SAR": "Riyal saoudien",
    "RSD": "Dinar serbe",
    "SCR": "Roupie seychelloise",
    "SLL": "Leone sierra-léonais",
    "SGD": "Dollar de Singapour",
    "SBD": "Dollar des îles Salomon",
    "SOS": "Shilling somalien",
    "ZAR": "Rand sud-africain",
    "KRW": "Won sud-coréen",
    "SSP": "Livre sud-soudanaise",
    "LKR": "Roupie srilankaise",
    "SDG": "Livre soudanaise",
    "SRD": "Dollar surinamais",
    "SZL": "Lilangeni swazi",
    "SEK": "Couronne suéدوise",
    "CHF": "Franc suisse",
    "SYP": "Livre syrienne",
    "TJS": "Somoni tadjik",
    "TZS": "Shilling tanzanien",
    "THB": "Baht thaïlandais",
    "TOP": "Pa'anga tongan",
    "TTD": "Dollar de Trinité-et-Tobago",
    "TND": "Dinar tunisien",
    "TRY": "Lire turque",
    "TMT": "Manat turkmène",
    "TVD": "Dollar tuvaluan",
    "UGX": "Shilling ougandais",
    "UAH": "Hryvnia ukrainienne",
    "AED": "Dirham des Émirats arabes unis",
    "USD": "Dollar américain",
    "UYU": "Peso uruguayen",
    "UZS": "Som ouzbek",
    "VUV": "Vatu vanuatais",
    "VES": "Bolivar vénézuélien",
    "VND": "Dong vietnamien",
    "YER": "Rial yéménite",
    "ZMW": "Kwacha zambien",
    "ZWL": "Dollar zimbabwéen"
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echange Dinar Tunisien</title>
    <style>
        :root { --primary: #d38b5d; --dark: #1e293b; --bg: #f1f5f9; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--bg); margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
        
        header { 
            background: var(--dark); color: white; padding: 2rem 1rem; text-align: center;
            border-bottom: 5px solid var(--primary);
        }

        .container { flex: 1; max-width: 500px; margin: 2rem auto; width: 90%; }
        
        .converter-card { 
            background: white; padding: 2rem; border-radius: 1.5rem; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        h1 { margin: 0; font-size: 1.5rem; letter-spacing: 1px; }
        .subtitle { color: var(--primary); font-weight: bold; margin-bottom: 2rem; display: block; }

        .form-group { margin-bottom: 1.5rem; text-align: left; }
        label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #64748b; font-size: 0.9rem; }
        input, select { 
            width: 100%; padding: 0.8rem; border: 2px solid #e2e8f0; border-radius: 0.75rem; 
            box-sizing: border-box; font-size: 1rem; transition: border-color 0.2s;
        }
        input:focus { border-color: var(--primary); outline: none; }

        .btn { 
            width: 100%; padding: 1rem; background: var(--primary); color: white; 
            border: none; border-radius: 0.75rem; font-weight: bold; cursor: pointer; 
            font-size: 1rem; transition: transform 0.2s, background 0.2s;
        }
        .btn:active { transform: scale(0.98); }

        .result-box { 
            margin-top: 2rem; padding: 1.5rem; background: #fff7ed; 
            border: 2px solid #ffedd5; border-radius: 1rem; text-align: center;
        }
        .result-val { font-size: 2rem; font-weight: 800; color: var(--primary); }

        footer { text-align: center; padding: 2rem; color: #94a3b8; font-size: 0.85rem; }
        .adam { color: var(--dark); font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <h1>Echange Dinar Tunisien</h1>
        <span class="subtitle">Convertisseur Officiel</span>
    </header>

    <div class="container">
        <div class="converter-card">
            <form method="POST">
                <div class="form-group">
                    <label>Montant en (TND)</label>
                    <input type="number" step="0.001" name="amount" value="{{ amount }}" required>
                </div>
                <div class="form-group">
                    <label>Devise Cible (A-Z)</label>
                    <select name="to_currency">
                        {% for code, name in currencies.items()|sort(attribute='1') %}
                        <option value="{{ code }}" {% if to_currency == code %}selected{% endif %}>
                            {{ name }} ({{ code }})
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit" class="btn">CALCULER LE CHANGE</button>
            </form>

            {% if result %}
            <div class="result-box">
                <div style="color: #9a3412; margin-bottom: 0.5rem;">Valeur Conversion :</div>
                <div class="result-val">{{ result }} {{ to_currency }}</div>
            </div>
            {% endif %}
        </div>
    </div>

    <footer>
        
        <p>Développé par <span class="adam">Adam - Moknine</span> 🇹🇳</p>
        <p>Ville de La Chebba - 2026</p>
    </footer>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result, amount, to_currency = None, "1.000", "EUR"
    if request.method == 'POST':
        try:
            amount_input = float(request.form.get('amount', 1))
            to_currency = request.form.get('to_currency', 'EUR')
            # جلب البيانات الحية لضمان الدقة
            resp = requests.get(API_URL, timeout=5)
            data = resp.json()
            rate = data['rates'].get(to_currency, 1)
            result = "{:,.2f}".format(amount_input * rate)
            amount = amount_input
        except Exception:
            result = "Erreur de Connexion"
            
    return render_template_string(HTML_TEMPLATE, currencies=CURRENCIES, result=result, amount=amount, to_currency=to_currency)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

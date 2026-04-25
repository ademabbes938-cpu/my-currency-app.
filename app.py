from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# رابط جلب أسعار الصرف الحية (Base TND)
API_URL = "https://api.exchangerate-api.com/v4/latest/TND"

# القائمة الكاملة لـ 160 عملة بالفرنسية مرتبة أبجدياً (A-Z)
CURRENCIES = {
    "AFN": "Afghani afghan", "ALL": "Lek albanais", "DZD": "Dinar algérien", "EUR": "Euro",
    "AMD": "Dram arménien", "AWG": "Florin d'Aruba", "AUD": "Dollar australien", "AZN": "Manat azerbaïdjanais",
    "BSD": "Dollar bahaméen", "BHD": "Dinar bahreïni", "BDT": "Taka bangladais", "BBD": "Dollar barbadien",
    "BYN": "Rouble biélorusse", "BZD": "Dollar bélizien", "BMD": "Dollar bermudien", "BTN": "Ngultrum bhoutanais",
    "BOB": "Boliviano bolivien", "BAM": "Mark convertible bosniaque", "BWP": "Pula botswanais", "BRL": "Réal brésilien",
    "BND": "Dollar de Brunei", "BGN": "Lev bulgare", "BIF": "Franc burundais", "KHR": "Riel cambodgien",
    "CAD": "Dollar canadien", "CVE": "Escudo cap-verdien", "KYD": "Dollar des îles Caïmans", "XAF": "Franc CFA (BEAC)",
    "XOF": "Franc CFA (BCEAO)", "XPF": "Franc CFP", "CLP": "Peso chilien", "CNY": "Yuan chinois",
    "COP": "Peso colombien", "KMF": "Franc comorien", "CDF": "Franc congolais", "CRC": "Colón costaricain",
    "HRK": "Kuna croate", "CUP": "Peso cubain", "DKK": "Couronne danoise", "DJF": "Franc djiboutien",
    "DOP": "Peso dominicain", "XCD": "Dollar des Caraïbes orientales", "EGP": "Livre égyptienne", "ERN": "Nakfa érythréen",
    "ETB": "Birr éthiopien", "FKP": "Livre des îles Malouines", "FOK": "Couronne féroïenne", "FJD": "Dollar fidjien",
    "GMD": "Dalasi gambien", "GEL": "Lari géorgien", "GHS": "Cedi ghanéen", "GIP": "Livre de Gibraltar",
    "GTQ": "Quetzal guatémaltèque", "GGP": "Livre de Guernesey", "GNF": "Franc guinéen", "GYD": "Dollar guyanien",
    "HTG": "Gourde haïtienne", "HNL": "Lempira hondurien", "HKD": "Dollar de Hong Kong", "HUF": "Forint hongrois",
    "ISK": "Couronne islandaise", "INR": "Roupie indienne", "IDR": "Roupie indonésienne", "IRR": "Rial iranien",
    "IQD": "Dinar irakien", "ILS": "Shekel israélien", "JMD": "Dollar jamaïcain", "JPY": "Yen japonais",
    "JEP": "Livre de Jersey", "JOD": "Dinar jordanien", "KZT": "Tenge kazakh", "KES": "Shilling kényan",
    "KGS": "Som kirghize", "KWD": "Dinar koweïtien", "LAK": "Kip laotien", "LBP": "Livre libanaise",
    "LSL": "Loti lesothan", "LRD": "Dollar libérien", "LYD": "Dinar libyen", "MOP": "Pataca macanaise",
    "MKD": "Denar macédonien", "MGA": "Ariary malgache", "MWK": "Kwacha malawien", "MYR": "Ringgit malais",
    "MVR": "Rufiyaa maldivienne", "IMP": "Livre mannoise", "MRU": "Ouguiya mauritanienne", "MUR": "Roupie mauricienne",
    "MXN": "Peso mexicain", "MDL": "Leu moldave", "MNT": "Tugrik mongol", "MAD": "Dirham marocain",
    "MZN": "Metical mozambicain", "MMK": "Kyat birman", "NAD": "Dollar namibien", "NPR": "Roupie népalaise",
    "ANG": "Florin des Antilles néerlandaises", "TWD": "Nouveau dollar taïwanais", "NZD": "Dollar néo-zélandais", "NIO": "Córdoba nicaraguayen",
    "NGN": "Naira nigérian", "NOK": "Couronne norvégienne", "OMR": "Rial omanais", "PKR": "Roupie pakistanaise",
    "PAB": "Balboa panaméen", "PGK": "Kina papouan-guinéen", "PYG": "Guaraní paraguayen", "PEN": "Sol péruvien",
    "PHP": "Peso philippin", "PLN": "Zloty polonais", "GBP": "Livre sterling", "QAR": "Riyal qatari",
    "RON": "Leu roumain", "RUB": "Rouble russe", "RWF": "Franc rwandais", "SHP": "Livre de Sainte-Hélène",
    "WST": "Tala samoan", "STN": "Dobra santoméen", "SAR": "Riyal saoudien", "RSD": "Dinar serbe",
    "SCR": "Roupie seychelloise", "SLL": "Leone sierra-léonais", "SGD": "Dollar de Singapour", "SBD": "Dollar des îles Salomon",
    "SOS": "Shilling somalien", "ZAR": "Rand sud-africain", "KRW": "Won sud-coréen", "SSP": "Livre sud-soudanaise",
    "LKR": "Roupie srilankaise", "SDG": "Livre soudanaise", "SRD": "Dollar surinamais", "SZL": "Lilangeni swazi",
    "SEK": "Couronne suédoise", "CHF": "Franc suisse", "SYP": "Livre syrienne", "TJS": "Somoni tadjik",
    "TZS": "Shilling tanzanien", "THB": "Baht thaïlandais", "TOP": "Pa'anga tongan", "TTD": "Dollar de Trinité-et-Tobago",
    "TND": "Dinar tunisien", "TRY": "Lire turque", "TMT": "Manat turkmène", "TVD": "Dollar tuvaluan",
    "UGX": "Shilling ougandais", "UAH": "Hryvnia ukrainienne", "AED": "Dirham des Émirats arabes unis", "USD": "Dollar américain",
    "UYU": "Peso uruguayen", "UZS": "Som ouzbek", "VUV": "Vatu vanuatais", "VES": "Bolivar vénézuélien",
    "VND": "Dong vietnamien", "YER": "Rial yéménite", "ZMW": "Kwacha zambien", "ZWL": "Dollar zimbabwéen"
}

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="fr" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echange Dinar Tunisien</title>
    <!-- الأيقونة تظهر بجانب الرابط (حرف E مع خط واحد بني) -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 fill=%22white%22/><text y=%22.9em%22 font-size=%2280%22 font-family=%22serif%22 fill=%22%23d38b5d%22 font-weight=%22bold%22 x=%2220%22>E</text><rect x=%2242%22 y=%2210%22 width=%228%22 height=%2280%22 fill=%22%23d38b5d%22/></svg>">
    
    <style>
        :root { --primary: #d38b5d; --dark: #1a202c; --bg: #f8fafc; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); margin: 0; color: #333; }
        
        header { 
            background: var(--dark); color: white; padding: 2.5rem 1rem; text-align: center;
            border-bottom: 6px solid var(--primary);
        }

        /* الشعار في الهيدر */
        .logo-box {
            width: 85px; height: 85px; background: white; margin: 0 auto 15px;
            border-radius: 15px; display: flex; align-items: center; justify-content: center;
            position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .logo-e { color: var(--primary); font-size: 60px; font-weight: bold; font-family: serif; position: relative; z-index: 1; }
        .central-line { position: absolute; width: 8px; height: 60px; background: var(--primary); left: 38px; top: 12px; z-index: 2; border-radius: 4px; }

        .container { max-width: 550px; margin: -40px auto 40px; padding: 20px; }
        
        .card { 
            background: white; padding: 35px; border-radius: 25px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center;
        }

        h1 { margin: 0; font-size: 1.8rem; color: white; }
        h2 { color: var(--primary); margin-top: 10px; margin-bottom: 30px; font-size: 1.3rem; }

        .form-group { text-align: left; margin-bottom: 20px; }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #64748b; font-size: 0.85rem; }
        input, select { 
            width: 100%; padding: 14px; border: 2px solid #f1f5f9; border-radius: 15px; 
            box-sizing: border-box; font-size: 1.1rem; outline: none; transition: 0.2s;
        }
        input:focus { border-color: var(--primary); }

        .btn { 
            background: var(--primary); color: white; padding: 16px; border: none; 
            border-radius: 15px; width: 100%; font-weight: bold; cursor: pointer; font-size: 1.1rem;
            transition: 0.3s; box-shadow: 0 4px 12px rgba(211, 139, 93, 0.3);
        }
        .btn:hover { background: #b57248; transform: translateY(-2px); }

        .result-box { 
            margin-top: 30px; padding: 25px; background: #fffcf9; 
            border: 2px dashed var(--primary); border-radius: 20px; 
        }
        .result-val { font-size: 2.6rem; font-weight: 800; color: var(--primary); }

        footer { text-align: center; padding: 40px; color: #94a3b8; font-size: 0.85rem; }
        .signature { font-weight: bold; color: var(--dark); font-size: 1rem; display: block; margin-top: 10px; }
    </style>
</head>
<body>

<header>
    <div class="logo-box">
        <span class="logo-e">E</span>
        <div class="central-line"></div>
    </div>
    <h1>Echange Dinar Tunisien</h1>
</header>

<div class="container">
    <div class="card">
        <h2>Convertisseur (A à Z)</h2>
        <form method="POST">
            <div class="form-group">
                <label>Montant en (TND)</label>
                <input type="number" step="0.001" name="amount" value="{{ amount }}" required>
            </div>
            <div class="form-group">
                <label>Vers la devise (160+ Devises)</label>
                <select name="to_currency">
                    {% for code, name in currencies.items()|sort(attribute='1') %}
                    <option value="{{ code }}" {% if to_currency == code %}selected{% endif %}>
                        {{ name }} ({{ code }})
                    </option>
                    {% endfor %}
                </select>
            </div>
            <button type="submit" class="btn">CALCULER MAINTENANT</button>
        </form>

        {% if result %}
        <div class="result-box">
            <p style="color: #c2410c; font-weight: 600;">Résultat estimé :</p>
            <div class="result-val">{{ result }} {{ to_currency }}</div>
        </div>
        {% endif %}
    </div>
</div>

<footer>
    
    <span class="signature">Développé par Adam - Moknine 🇹🇳</span>
    <p>© 2026 Echange Dinar Tunisien</p>
</footer>

</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    result, amount, to_currency = None, "1.000", "EUR"
    if request.method == 'POST':
        try:
            amount_val = float(request.form.get('amount', 1))
            to_currency = request.form.get('to_currency', 'EUR')
            # جلب البيانات الحية
            data = requests.get(API_URL, timeout=5).json()
            rate = data['rates'].get(to_currency, 1)
            result = "{:,.2f}".format(amount_val * rate)
            amount = amount_val
        except Exception:
            result = "Erreur Service"
            
    return render_template_string(HTML_PAGE, currencies=CURRENCIES, result=result, amount=amount, to_currency=to_currency)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

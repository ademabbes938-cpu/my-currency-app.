from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

# رابط جلب أسعار الصرف الحية
API_URL = "https://api.exchangerate-api.com/v4/latest/TND"

# القائمة الكاملة لجميع العملات العالمية بالفرنسية
CURRENCY_NAMES = {
    "AED": "Dirham des Émirats arabes unis", "AFN": "Afghani afghan", "ALL": "Lek albanais", "AMD": "Dram arménien",
    "ANG": "Florin des Antilles néerlandaises", "AOA": "Kwanza angolais", "ARS": "Peso argentin", "AUD": "Dollar australien",
    "AWG": "Florin d'Aruba", "AZN": "Manat azerbaïdjanais", "BAM": "Mark convertible bosniaque", "BBD": "Dollar barbadien",
    "BDT": "Taka bangladais", "BGN": "Lev bulgare", "BHD": "Dinar bahreïni", "BIF": "Franc burundais",
    "BMD": "Dollar bermudien", "BND": "Dollar de Brunei", "BOB": "Boliviano bolivien", "BRL": "Réal brésilien",
    "BSD": "Dollar bahaméen", "BTN": "Ngultrum bhoutanais", "BWP": "Pula botswanais", "BYN": "Rouble biélorusse",
    "BZD": "Dollar bélizien", "CAD": "Dollar canadien", "CDF": "Franc congolais", "CHF": "Franc suisse",
    "CLP": "Peso chilien", "CNY": "Yuan chinois", "COP": "Peso colombien", "CRC": "Colón costaricain",
    "CUP": "Peso cubain", "CVE": "Escudo cap-verdien", "CZK": "Couronne tchèque", "DJF": "Franc djiboutien",
    "DKK": "Couronne danoise", "DOP": "Peso dominicain", "DZD": "Dinar algérien", "EGP": "Livre égyptienne",
    "ERN": "Nakfa érythréen", "ETB": "Birr éthiopien", "EUR": "Euro", "FJD": "Dollar fidjien",
    "FKP": "Livre des îles Malouines", "FOK": "Couronne féroïenne", "GBP": "Livre sterling", "GEL": "Lari géorgien",
    "GGP": "Livre de Guernesey", "GHS": "Cedi ghanéen", "GIP": "Livre de Gibraltar", "GMD": "Dalasi gambien",
    "GNF": "Franc guinéen", "GTQ": "Quetzal guatémaltèque", "GYD": "Dollar guyanien", "HKD": "Dollar de Hong Kong",
    "HNL": "Lempira hondurien", "HRK": "Kuna croate", "HTG": "Gourde haïtienne", "HUF": "Forint hongrois",
    "IDR": "Roupie indonésienne", "ILS": "Shekel israélien", "IMP": "Livre mannoise", "INR": "Roupie indienne",
    "IQD": "Dinar irakien", "IRR": "Rial iranien", "ISK": "Couronne islandaise", "JEP": "Livre de Jersey",
    "JMD": "Dollar jamaïcain", "JOD": "Dinar jordanien", "JPY": "Yen japonais", "KES": "Shilling kényan",
    "KGS": "Som kirghize", "KHR": "Riel cambodgien", "KID": "Dollar des Kiribati", "KMF": "Franc comorien",
    "KRW": "Won sud-coréen", "KWD": "Dinar koweïtien", "KYD": "Dollar des îles Caïmans", "KZT": "Tenge kazakh",
    "LAK": "Kip laotien", "LBP": "Livre libanaise", "LKR": "Roupie srilankaise", "LRD": "Dollar libérien",
    "LSL": "Loti lesothan", "LYD": "Dinar libyen", "MAD": "Dirham marocain", "MDL": "Leu moldave",
    "MGA": "Ariary malgache", "MKD": "Denar macédonien", "MMK": "Kyat birman", "MNT": "Tugrik mongol",
    "MOP": "Pataca macanaise", "MRU": "Ouguiya mauritanienne", "MUR": "Roupie mauricienne", "MVR": "Rufiyaa maldivienne",
    "MWK": "Kwacha malawien", "MXN": "Peso mexicain", "MYR": "Ringgit malais", "MZN": "Metical mozambicain",
    "NAD": "Dollar namibien", "NGN": "Naira nigérian", "NIO": "Córdoba nicaraguayen", "NOK": "Couronne norvégienne",
    "NPR": "Roupie népalaise", "NZD": "Dollar néo-zélandais", "OMR": "Rial omanais", "PAB": "Balboa panaméen",
    "PEN": "Sol péruvien", "PGK": "Kina papouan-guinéen", "PHP": "Peso philippin", "PKR": "Roupie pakistanaise",
    "PLN": "Zloty polonais", "PYG": "Guaraní paraguayen", "QAR": "Riyal qatari", "RON": "Leu roumain",
    "RSD": "Dinar serbe", "RUB": "Rouble russe", "RWF": "Franc rwandais", "SAR": "Riyal saoudien",
    "SBD": "Dollar des îles Salomon", "SCR": "Roupie seychelloise", "SDG": "Livre soudanaise", "SEK": "Couronne suédoise",
    "SGD": "Dollar de Singapour", "SHP": "Livre de Sainte-Hélène", "SLL": "Leone sierra-léonais", "SOS": "Shilling somalien",
    "SRD": "Dollar surinamais", "SSP": "Livre sud-soudanaise", "STN": "Dobra santoméen", "SYP": "Livre syrienne",
    "SZL": "Lilangeni swazi", "THB": "Baht thaïlandais", "TJS": "Somoni tadjik", "TMT": "Manat turkmène",
    "TND": "Dinar tunisien", "TOP": "Pa'anga tongan", "TRY": "Lire turque", "TTD": "Dollar de Trinité-et-Tobago",
    "TVD": "Dollar tuvaluan", "TWD": "Nouveau dollar taïwanais", "TZS": "Shilling tanzanien", "UAH": "Hryvnia ukrainienne",
    "UGX": "Shilling ougandais", "USD": "Dollar américain", "UYU": "Peso uruguayen", "UZS": "Som ouzbek",
    "VES": "Bolivar vénézuélien", "VND": "Dong vietnamien", "VUV": "Vatu vanuatais", "WST": "Tala samoan",
    "XAF": "Franc CFA (BEAC)", "XCD": "Dollar des Caraïbes orientales", "XDR": "Droits de tirage spéciaux",
    "XOF": "Franc CFA (BCEAO)", "XPF": "Franc CFP", "YER": "Rial yéménite", "ZAR": "Rand sud-africain",
    "ZMW": "Kwacha zambien", "ZWL": "Dollar zimbabwéen"
}

def get_live_rates():
    try:
        response = requests.get(API_URL, timeout=5)
        return response.json().get('rates', {})
    except:
        return {"USD": 0.32, "EUR": 0.30, "TND": 1.0}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convertisseur Adam - 160+ Devises</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23E70013'/><path d='M35 30 H65 M35 50 H60 M35 70 H65 M35 30 V70' stroke='white' stroke-width='8' stroke-linecap='round' fill='none'/></svg>">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 100%; max-width: 500px; text-align: center; border-top: 6px solid #E70013; }
        h1 { color: #333; font-size: 1.5rem; margin-bottom: 25px; }
        .input-group { text-align: left; margin-bottom: 20px; }
        label { font-weight: bold; color: #666; font-size: 0.9rem; }
        input, select { width: 100%; padding: 12px; margin-top: 8px; border-radius: 10px; border: 1px solid #ddd; box-sizing: border-box; font-size: 1rem; }
        .btn { width: 100%; padding: 15px; background: #E70013; color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        .btn:hover { background: #c60011; transform: translateY(-2px); }
        .result { margin-top: 25px; padding: 20px; background: #fff5f5; border-radius: 15px; border: 1px solid #ffe5e5; }
        .val { font-size: 2rem; font-weight: 800; color: #E70013; }
        footer { margin-top: 30px; font-size: 0.8rem; color: #bbb; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Convertisseur Global Adam</h1>
        <form method="POST">
            <div class="input-group">
                <label>Montant en Dinars Tunisiens (TND)</label>
                <input type="number" step="0.001" name="amount" value="{{ amount }}" required>
            </div>
            <div class="input-group">
                <label>Convertir vers</label>
                <select name="currency">
                    {% for code in rates.keys()|sort %}
                    <option value="{{ code }}" {% if currency == code %}selected{% endif %}>
                        {{ names.get(code, code) }} ({{ code }})
                    </option>
                    {% endfor %}
                </select>
            </div>
            <button type="submit" class="btn">CALCULER</button>
        </form>
        {% if result %}
        <div class="result">
            <div class="val">{{ result }} {{ currency }}</div>
        </div>
        {% endif %}
        <footer>Réalisé par Adam - Moknine 🇹🇳</footer>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    rates = get_live_rates()
    result, amount, currency = None, '1.000', 'USD'
    if request.method == 'POST':
        try:
            amount_val = float(request.form['amount'])
            currency = request.form['currency']
            result = "{:,.2f}".format(amount_val * rates.get(currency, 1))
            amount = amount_val
        except: result = "Erreur"
    return render_template_string(HTML_TEMPLATE, rates=rates, result=result, amount=amount, currency=currency, names=CURRENCY_NAMES)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

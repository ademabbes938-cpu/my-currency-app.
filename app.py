from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# رابط جلب أسعار الصرف الحية
API_URL = "https://api.exchangerate-api.com/v4/latest/TND"

# قاموس لترجمة الرموز إلى الأسماء الفرنسية الكاملة
CURRENCY_NAMES = {
    'USD': 'Dollar Américain',
    'EUR': 'Euro',
    'TND': 'Dinar Tunisien',
    'SAR': 'Riyal Saoudien',
    'AED': 'Dirham des Émirats',
    'TRY': 'Lire Turque',
    'GBP': 'Livre Sterling',
    'CAD': 'Dollar Canadien',
    'JPY': 'Yen Japonais',
    'CHF': 'Franc Suisse',
    'QAR': 'Riyal Qatari',
    'MAD': 'Dirham Marocain',
    'DZD': 'Dinar Algérien',
    'LYD': 'Dinar Libyen',
    'EGP': 'Livre Égyptienne',
    'KWD': 'Dinar Koweïtien',
    'CNY': 'Yuan Chinois',
    'RUB': 'Rouble Russe',
    'AUD': 'Dollar Australien',
    'BRL': 'Réal Brésilien',
    'INR': 'Roupie Indienne'
}

def get_live_rates():
    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()
        return data.get('rates', {})
    except Exception:
        return {'USD': 0.32, 'EUR': 0.30, 'TND': 1.0}

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echange Global - Adam</title>
    
    <!-- الأيقونة التي تظهر بجانب الرابط في جوجل -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='20' fill='%23E70013'/><path d='M35 30 H65 M35 50 H60 M35 70 H65 M35 30 V70' stroke='white' stroke-width='8' stroke-linecap='round' fill='none'/><line x1='25' y1='42' x2='45' y2='42' stroke='white' stroke-width='4' stroke-linecap='round'/><line x1='25' y1='58' x2='45' y2='58' stroke='white' stroke-width='4' stroke-linecap='round'/></svg>">

    <style>
        :root { --red: #E70013; --white: #ffffff; }
        body { font-family: sans-serif; background: #f4f6f8; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .card { background: var(--white); width: 100%; max-width: 480px; border-radius: 35px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.1); text-align: center; }
        .header-bg { width: 100%; height: 160px; background: url('https://images.unsplash.com/photo-1590059391056-0e7828003666?w=800') center/cover; position: relative; }
        .logo-badge { width: 110px; height: 110px; background: var(--red); border-radius: 22px; margin: -55px auto 10px; position: relative; display: flex; align-items: center; justify-content: center; border: 5px solid white; box-shadow: 0 8px 20px rgba(231,0,19,0.3); z-index: 2; }
        .content { padding: 10px 30px 40px; }
        h1 { font-size: 1.4rem; color: #222; margin-bottom: 25px; font-weight: 800; }
        .field { text-align: left; margin-bottom: 15px; }
        label { font-size: 0.85rem; font-weight: 700; color: #666; display: block; margin-bottom: 5px; }
        input, select { width: 100%; padding: 12px; border-radius: 12px; border: 1px solid #ddd; font-size: 1rem; box-sizing: border-box; }
        .btn { width: 100%; padding: 15px; background: var(--red); color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; font-size: 1.1rem; margin-top: 10px; }
        .result { margin-top: 20px; padding: 20px; background: #fff5f5; border-radius: 15px; border: 1px solid #ffe5e5; }
        .val { font-size: 2rem; font-weight: 900; color: var(--red); }
        .footer { margin-top: 30px; font-size: 0.8rem; color: #ccc; }
    </style>
</head>
<body>
    <div class="card">
        <div class="header-bg"></div>
        <div class="logo-badge">
            <svg width="65" height="65" viewBox="0 0 100 100">
                <path d="M35 32 H65 M35 50 H60 M35 68 H65 M35 32 V68" stroke="white" stroke-width="8" stroke-linecap="round" fill="none" />
                <line x1="25" y1="43" x2="45" y2="43" stroke="white" stroke-width="4" stroke-linecap="round" />
                <line x1="25" y1="57" x2="45" y2="57" stroke="white" stroke-width="4" stroke-linecap="round" />
            </svg>
        </div>
        <div class="content">
            <h1>Echange de Devises Global</h1>
            <form method="POST">
                <div class="field">
                    <label>Montant en (TND)</label>
                    <input type="number" step="0.001" name="amount" placeholder="Ex: 10.500" required value="{{ amount }}">
                </div>
                <div class="field">
                    <label>Vers la devise</label>
                    <select name="currency">
                        {% for code in rates.keys()|sort %}
                        <option value="{{ code }}" {% if currency == code %}selected{% endif %}>
                            {{ currency_names.get(code, code) }} ({{ code }})
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit" class="btn">CONVERTIR</button>
            </form>
            {% if result %}
            <div class="result">
                <div class="val">{{ result }} {{ currency }}</div>
            </div>
            {% endif %}
            <div class="footer">Adam | Moknine, Tunisie 🇹🇳</div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    rates = get_live_rates()
    result, amount, currency = None, '', 'USD'
    if request.method == 'POST':
        try:
            amount_val = float(request.form['amount'])
            currency = request.form['currency']
            result = "{:,.2f}".format(amount_val * rates.get(currency, 1))
            amount = amount_val
        except: result = "Erreur"
    return render_template_string(HTML_PAGE, rates=rates, result=result, amount=amount, currency=currency, currency_names=CURRENCY_NAMES)

if __name__ == '__main__':
    app.run()

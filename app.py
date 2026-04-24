from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# رابط جلب أسعار الصرف الحية (تلقائي لكل عملات العالم)
API_URL = "https://api.exchangerate-api.com/v4/latest/TND"

def get_live_rates():
    try:
        # جلب البيانات من الإنترنت
        response = requests.get(API_URL, timeout=5)
        data = response.json()
        return data.get('rates', {})
    except Exception:
        # قائمة احتياطية في حال تعطل الإنترنت مؤقتاً
        return {'USD': 0.32, 'EUR': 0.30, 'TRY': 10.5, 'SAR': 1.2, 'TND': 1.0, 'GBP': 0.25}

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echange Global - Dinar Tunisien</title>
    <style>
        :root { --tunisian-red: #E70013; --white: #ffffff; --soft-gray: #f8f9fa; }
        body { font-family: 'Segoe UI', sans-serif; background-color: var(--soft-gray); margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .main-card { background: var(--white); width: 100%; max-width: 450px; padding: 40px; border-radius: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.07); text-align: center; border: 1px solid #f0f0f0; }
        .brand-logo { width: 140px; height: 140px; margin: 0 auto 30px; display: block; }
        h1 { color: #1a1a1a; font-size: 1.5rem; margin-bottom: 30px; font-weight: 800; }
        .input-box { text-align: left; margin-bottom: 20px; }
        label { display: block; font-size: 0.9rem; font-weight: 700; color: #555; margin-bottom: 8px; }
        input, select { width: 100%; padding: 15px; border: 2px solid #eee; border-radius: 15px; font-size: 1.1rem; box-sizing: border-box; }
        input:focus { border-color: var(--tunisian-red); outline: none; }
        .btn-action { width: 100%; padding: 18px; background: var(--tunisian-red); color: white; border: none; border-radius: 15px; font-size: 1.2rem; font-weight: bold; cursor: pointer; transition: 0.3s; box-shadow: 0 10px 20px rgba(231, 0, 19, 0.2); }
        .btn-action:hover { background: #c60011; transform: translateY(-2px); }
        .result-panel { margin-top: 30px; padding: 20px; background: #fffafa; border-radius: 20px; border: 2px solid #ffebeb; }
        .res-value { font-size: 2.2rem; font-weight: 900; color: var(--tunisian-red); }
        .dev-credit { margin-top: 35px; font-size: 0.8rem; color: #ccc; border-top: 1px solid #f9f9f9; padding-top: 15px; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="brand-logo">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <rect x="5" y="5" width="90" height="90" rx="22" fill="#E70013" />
                <path d="M35 32 H65 M35 50 H60 M35 68 H65 M35 32 V68" stroke="white" stroke-width="8" stroke-linecap="round" fill="none" />
                <line x1="25" y1="43" x2="48" y2="43" stroke="white" stroke-width="4" stroke-linecap="round" />
                <line x1="25" y1="57" x2="48" y2="57" stroke="white" stroke-width="4" stroke-linecap="round" />
            </svg>
        </div>
        <h1>Echange avec le Dinar</h1>
        <form method="POST">
            <div class="input-box">
                <label>Montant en (TND)</label>
                <input type="number" step="0.001" name="amount" placeholder="0.000" required value="{{ amount }}">
            </div>
            <div class="input-box">
                <label>Vers la devise (Toutes les monnaies)</label>
                <select name="currency">
                    {% for code in rates.keys()|sort %}
                    <option value="{{ code }}" {% if currency == code %}selected{% endif %}>{{ code }}</option>
                    {% endfor %}
                </select>
            </div>
            <button type="submit" class="btn-action">CALCULER</button>
        </form>
        {% if result %}
        <div class="result-panel">
            <div style="color: #999;">Valeur convertية :</div>
            <div class="res-value">{{ result }} {{ currency }}</div>
        </div>
        {% endif %}
        <div class="dev-credit">Développé par Adam | Moknine, Tunisie 🇹🇳</div>
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
            rate = rates.get(currency, 1)
            # النتيجة = المبلغ مضروب في سعر الصرف مقابل 1 دينار
            result = "{:,.2f}".format(amount_val * rate)
            amount = amount_val
        except: result = "Erreur"
    return render_template_string(HTML_PAGE, rates=rates, result=result, amount=amount, currency=currency)

if __name__ == '__main__':
    app.run(debug=True)

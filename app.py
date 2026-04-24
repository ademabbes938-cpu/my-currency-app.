from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# رابط جلب أسعار الصرف الحية (تلقائي لكل عملات العالم)
API_URL = "https://api.exchangerate-api.com/v4/latest/TND"

def get_live_rates():
    try:
        response = requests.get(API_URL, timeout=5)
        data = response.json()
        return data.get('rates', {})
    except Exception:
        return {'USD': 0.32, 'EUR': 0.30, 'TRY': 10.5, 'SAR': 1.2, 'TND': 1.0}

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echange Global - Adam</title>
    <style>
        :root { --red: #E70013; --white: #ffffff; }
        body { font-family: sans-serif; background: #f4f4f4; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .card { background: var(--white); width: 100%; max-width: 450px; border-radius: 30px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; }
        .img-header { width: 100%; height: 150px; background: url('https://images.unsplash.com/photo-1590059391056-0e7828003666?w=500') center/cover; }
        .logo { width: 100px; height: 100px; background: var(--red); border-radius: 20px; margin: -50px auto 10px; display: flex; align-items: center; justify-content: center; border: 5px solid white; box-shadow: 0 5px 15px rgba(231,0,19,0.3); }
        .content { padding: 20px 30px 40px; }
        input, select { width: 100%; padding: 12px; margin: 10px 0; border-radius: 10px; border: 1px solid #ddd; box-sizing: border-box; }
        .btn { width: 100%; padding: 15px; background: var(--red); color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 1.1rem; }
        .res { margin-top: 20px; font-size: 2rem; font-weight: 900; color: var(--red); background: #fff5f5; padding: 15px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <div class="img-header"></div>
        <div class="logo">
            <svg width="60" height="60" viewBox="0 0 100 100">
                <path d="M35 32 H65 M35 50 H60 M35 68 H65 M35 32 V68" stroke="white" stroke-width="8" stroke-linecap="round" fill="none" />
                <line x1="25" y1="43" x2="45" y2="43" stroke="white" stroke-width="4" stroke-linecap="round" />
                <line x1="25" y1="57" x2="45" y2="57" stroke="white" stroke-width="4" stroke-linecap="round" />
            </svg>
        </div>
        <div class="content">
            <h1>Echange de Devises</h1>
            <form method="POST">
                <input type="number" step="0.001" name="amount" placeholder="Montant en TND" required value="{{ amount }}">
                <select name="currency">
                    {% for code in rates.keys()|sort %}
                    <option value="{{ code }}" {% if currency == code %}selected{% endif %}>{{ code }}</option>
                    {% endfor %}
                </select>
                <button type="submit" class="btn">CONVERTIR</button>
            </form>
            {% if result %}<div class="res">{{ result }} {{ currency }}</div>{% endif %}
            <p style="color:#ccc; font-size: 0.8rem; margin-top: 20px;">Adam | Moknine 🇹🇳</p>
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
    return render_template_string(HTML_PAGE, rates=rates, result=result, amount=amount, currency=currency)

if __name__ == '__main__':
    app.run()

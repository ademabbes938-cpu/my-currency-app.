from flask import Flask, render_template_string, request

app = Flask(__name__)

# أسعار الصرف المحدثة (مقابل 1 دينار تونسي)
EXCHANGE_RATES = {
    'USD': 3.12, 'EUR': 3.35, 'TRY': 0.096, 'JPY': 0.020,
    'SAR': 0.83, 'AED': 0.85, 'GBP': 3.90, 'CAD': 2.28, 'QAR': 0.86
}

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="fr" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Echange avec le Dinar Tunisien</title>
    <style>
        :root { --tunisian-red: #E70013; --white: #ffffff; }
        body { font-family: sans-serif; background: #fdfdfd; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: var(--white); width: 100%; max-width: 400px; padding: 30px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align: center; border: 1px solid #eee; border-top: 10px solid var(--tunisian-red); }
        .logo-box { width: 80px; height: 80px; background: var(--tunisian-red); margin: 0 auto 20px; border-radius: 15px; display: flex; align-items: center; justify-content: center; position: relative; color: white; font-size: 50px; font-weight: 900; }
        .logo-box::after { content: ""; position: absolute; left: 15px; top: 40%; width: 50px; height: 4px; background: white; box-shadow: 0 12px 0 white; }
        h1 { color: var(--tunisian-red); font-size: 1.4rem; }
        input, select { width: 100%; padding: 12px; margin: 10px 0; border-radius: 10px; border: 1px solid #ddd; box-sizing: border-box; }
        .btn { width: 100%; padding: 15px; background: var(--tunisian-red); color: white; border: none; border-radius: 10px; font-size: 1.1rem; cursor: pointer; font-weight: bold; }
        .result { margin-top: 20px; padding: 15px; background: #fff5f5; border-radius: 10px; color: var(--tunisian-red); font-weight: bold; font-size: 1.5rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo-box">E</div>
        <h1>Echange avec le Dinar Tunisien</h1>
        <form method="POST">
            <input type="number" step="0.01" name="amount" placeholder="Montant en TND" required value="{{ amount }}">
            <select name="currency">
                <option value="USD">🇺🇸 Dollar US</option>
                <option value="EUR">🇪🇺 Euro</option>
                <option value="TRY">🇹🇷 Lire Turque</option>
                <option value="JPY">🇯🇵 Yen Japonais</option>
                <option value="SAR">🇸🇦 Riyal Saoudien</option>
            </select>
            <button type="submit" class="btn">Calculer</button>
        </form>
        {% if result %}<div class="result">{{ result }} {{ currency }}</div>{% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result, amount, currency = None, '', 'USD'
    if request.method == 'POST':
        try:
            amount_val = float(request.form['amount'])
            currency = request.form['currency']
            converted = amount_val / EXCHANGE_RATES.get(currency, 1)
            result = "{:,.2f}".format(converted)
            amount = amount_val
        except: result = "Erreur"
    return render_template_string(HTML_PAGE, result=result, amount=amount, currency=currency)

if __name__ == '__main__':
    app.run(debug=True)

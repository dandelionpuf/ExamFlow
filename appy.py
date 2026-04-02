from flask import Flask, render_template

app= Flask(__name__)


dersler = {
    "Tarih":{
        "biten": 5,
        "toplam": 25,
        "yanlis": 14,
        "renk": "#e74c3c"
    },
    "Turkce": {
        "biten": 12,
        "toplam": 30,
        "yanlis": 8,
        "renk": "#f1c40f"

    }
}

@app.route('/')
def index():
    return render_template('index.html', veriler=dersler)

if __name__ == '__main__':
    app.run(debug=True)
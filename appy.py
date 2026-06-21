from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
app = Flask(__name__)
def db_connection():
    conn = sqlite3.connect('sinav.db')
    conn.row_factory = sqlite3.Row
    return conn
def veritabani_olustur():
    conn = db_connection()
    conn.execute('''
            CREATE TABLE IF NOT EXISTS dersler (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ders_adi TEXT UNIQUE,
                 biten INTEGER DEFAULT 0,
                 toplam INTEGER DEFAULT 100,
                 yanlis INTEGER DEFAULT 0,
                 dogru INTEGER DEFAULT 0,
                 puan INTEGER DEFAULT 0,
                 renk TEXT
            )
        ''')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM dersler")
    if cursor.fetchone()[0] == 0:
        varsayilanlar = [
            ('Tarih', 8, 25, 0, 8, 16, '#e74c3c'),
            ('Turkce', 12, 30, 8, 22, 36, '#f1c40f')
        ]
        cursor.executemany("INSERT INTO dersler (ders_adi, biten, toplam, yanlis, dogru, puan, renk) VALUES (?, ?, ?, ?, ?, ?, ?)", varsayilanlar)
        conn.commit()      
                           
    conn.close()
@app.route('/')
def index():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dersler') 
    veriler = cursor.fetchall()


    toplam_biten = 0
    toplam_konu = 0


    for ders in veriler:
        toplam_biten += ders[2]
        toplam_konu += ders[3]

    genel_yuzde = 0
    if toplam_konu > 0:
        genel_yuzde = round(toplam_biten / toplam_konu * 100, 1)
    
    conn.close()
    return render_template('index.html', veriler=veriler, toplam_biten=toplam_biten, toplam_konu=toplam_konu, genel_yuzde=genel_yuzde)
@app.route('/guncelle', methods=['GET', 'POST'])
def guncelle():
    conn = db_connection()
    if request.method == 'POST':
        ders_adi = request.form.get('ders_adi')
        yeni_biten = request.form.get('biten', type=int, default=0)
        yeni_yanlis = request.form.get('yanlis', type=int, default=0)
        yeni_dogru = request.form.get('dogru', type=int, default=0)
        yeni_puan = (yeni_dogru * 2) - (yeni_yanlis * 0.5)
        yeni_renk = request.form.get('renk')

        conn.execute('''
                     UPDATE dersler
                     SET biten = ?, yanlis = ?, dogru = ?, puan = ?, renk = ?
                     WHERE ders_adi = ?
        ''', (yeni_biten, yeni_yanlis, yeni_dogru, yeni_puan, yeni_renk, ders_adi))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    dersler_listesi = conn.execute('SELECT * FROM dersler').fetchall()
    conn.close()
    return render_template('guncelle.html', dersler=dersler_listesi)

veritabani_olustur()
@app.route('/ekle', methods=['GET', 'POST'])
def ders_ekle():
    if request.method == 'POST':
        ders_adi = request.form['ders_adi']
        toplam = request.form['toplam']
        renk = request.form['renk']

        conn = db_connection()
        conn.execute('INSERT INTO dersler (ders_adi, biten, toplam, yanlis, renk) VALUES (?, ?, ?, ?, ?)',
                     (ders_adi, 0, toplam, 0, renk))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('ekle.html')
@app.route('/sil/<int:id>')
def sil(id):
        conn = db_connection()
        conn.execute('DELETE FROM dersler WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return redirect('/')
        
if __name__ == '__main__':
    app.run(debug=True)
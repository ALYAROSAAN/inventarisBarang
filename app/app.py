# app/app.py (Versi Inventaris Barang)
import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # UBAH DI SINI: Membuat tabel 'barang' dengan kolom nama_barang dan jumlah
    cur.execute('''
        CREATE TABLE IF NOT EXISTS barang (
            id SERIAL PRIMARY KEY,
            nama_barang TEXT NOT NULL,
            jumlah INTEGER NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# UBAH DI SINI: Halaman utama untuk menampilkan daftar barang (Read)
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM barang ORDER BY id;')
    items = cur.fetchall() # Mengganti nama variabel dari 'tasks' menjadi 'items'
    cur.close()
    conn.close()
    return render_template('index.html', items=items) # Mengirim 'items' ke template

# UBAH DI SINI: Menambah barang baru (Create)
@app.route('/add', methods=('POST',))
def add():
    nama_barang = request.form['nama_barang']
    jumlah = request.form['jumlah']
    
    # Memastikan kedua input tidak kosong
    if nama_barang and jumlah:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO barang (nama_barang, jumlah) VALUES (%s, %s)',
                    (nama_barang, int(jumlah)))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))

# UBAH DI SINI: Menghapus barang (Delete)
@app.route('/delete/<int:item_id>', methods=('POST',))
def delete(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM barang WHERE id = %s;', (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing database: {e}")
        import time
        time.sleep(5)
        init_db()

    app.run(host='0.0.0.0', port=5000, debug=True)
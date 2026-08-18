import os
import random
import sqlite3
import requests
import pandas as pd
import streamlit as st
import yt_dlp

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Personal Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIALISASI DATABASE KEUANGAN (SQLITE) ---
def init_db():
    conn = sqlite3.connect("database_app.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS keuangan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT,
            jumlah REAL,
            jenis TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- INITIALIZE SESSION STATE FOR TO-DO ---
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# --- CUSTOM STYLING (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
    }
    .header-box {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("🚀 Personal Dashboard")
st.sidebar.caption("All-in-One Productivity Hub")

pilihan_menu = st.sidebar.radio(
    "Navigasi Fitur",
    [
        "🌤️ Cek Cuaca",
        "📝 To-Do List",
        "💰 Pelacak Keuangan",
        "💬 Quotes Inspiratif",
        "📥 Media Downloader"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Status:** Dashboard Aktif & Siap Digunakan")


# ==========================================
# 🌤️ FITUR 1: CEK CUACA
# ==========================================
if pilihan_menu == "🌤️ Cek Cuaca":
    st.markdown("""
        <div class="header-box">
            <h2>🌤️ Cek Cuaca Real-Time</h2>
            <p style="color: #9ca3af; margin: 0;">Prakiraan cuaca langsung via Open-Meteo API.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, _ = st.columns([2, 1])
    kota = col1.text_input("📍 Masukkan Nama Kota:", placeholder="Contoh: Jakarta, Surabaya, Bali, Tokyo")
    
    if st.button("🔍 Cek Cuaca", type="primary"):
        if not kota.strip():
            st.warning("⚠️ Masukkan nama kota terlebih dahulu!")
        else:
            with st.spinner("Mengambil data cuaca..."):
                try:
                    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={kota}&count=1"
                    geo_res = requests.get(geo_url).json()
                    
                    if "results" in geo_res and len(geo_res["results"]) > 0:
                        lat = geo_res["results"][0]["latitude"]
                        lon = geo_res["results"][0]["longitude"]
                        nama_res = geo_res["results"][0]["name"]
                        negara = geo_res["results"][0].get("country", "")
                        
                        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                        w_res = requests.get(w_url).json()
                        curr = w_res["current_weather"]
                        
                        st.success(f"Lokasi: **{nama_res}, {negara}**")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("🌡️ Suhu Udara", f"{curr['temperature']} °C")
                        c2.metric("💨 Kecepatan Angin", f"{curr['windspeed']} km/h")
                        c3.metric("🧭 Arah Angin", f"{curr['winddirection']}°")
                    else:
                        st.error("❌ Kota tidak ditemukan.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")


# ==========================================
# 📝 FITUR 2: TO-DO LIST
# ==========================================
elif pilihan_menu == "📝 To-Do List":
    st.markdown("""
        <div class="header-box">
            <h2>📝 To-Do List Harian</h2>
            <p style="color: #9ca3af; margin: 0;">Kelola tugas dan target harianmu.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_in, col_bt = st.columns([4, 1])
    tugas_baru = col_in.text_input("Tugas Baru:", placeholder="Tuliskan tugas...", label_visibility="collapsed")
    
    if col_bt.button("➕ Tambah", type="primary", use_container_width=True):
        if tugas_baru.strip():
            st.session_state.todo_list.append({"tugas": tugas_baru.strip(), "selesai": False})
            st.rerun()
            
    st.divider()
    
    if not st.session_state.todo_list:
        st.info("📌 Belum ada tugas ditambahkan.")
    else:
        for idx, item in enumerate(st.session_state.todo_list):
            c_chk, c_txt, c_del = st.columns([0.5, 8, 0.5])
            is_done = c_chk.checkbox("", value=item["selesai"], key=f"todo_{idx}")
            st.session_state.todo_list[idx]["selesai"] = is_done
            
            if is_done:
                c_txt.markdown(f"~~{item['tugas']}~~ ✅")
            else:
                c_txt.write(item["tugas"])
                
            if c_del.button("🗑️", key=f"del_todo_{idx}"):
                st.session_state.todo_list.pop(idx)
                st.rerun()


# ==========================================
# 💰 FITUR 3: PELACAK KEUANGAN (SQLITE)
# ==========================================
elif pilihan_menu == "💰 Pelacak Keuangan":
    st.markdown("""
        <div class="header-box">
            <h2>💰 Pelacak Keuangan Permanen</h2>
            <p style="color: #9ca3af; margin: 0;">Catatan keuangan tersimpan aman di Database SQLite.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_keuangan", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        ket = c1.text_input("Keterangan", placeholder="Contoh: Gaji, Kopi")
        nom = c2.number_input("Nominal (Rp)", min_value=0, step=5000)
        jns = c3.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
        
        if st.form_submit_button("💳 Simpan Transaksi", type="primary", use_container_width=True):
            if ket.strip() and nom > 0:
                conn = sqlite3.connect("database_app.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO keuangan (keterangan, jumlah, jenis) VALUES (?, ?, ?)", (ket, nom, jns))
                conn.commit()
                conn.close()
                st.success("Data berhasil disimpan!")
                st.rerun()
            else:
                st.warning("⚠️ Lengkapi data transaksi dengan benar!")

    st.divider()

    # Load Data dari SQLite
    conn = sqlite3.connect("database_app.db")
    df = pd.read_sql_query("SELECT id, keterangan as Keterangan, jumlah as Jumlah, jenis as Jenis FROM keuangan", conn)
    conn.close()

    if not df.empty:
        total_masuk = df[df["Jenis"] == "Pemasukan"]["Jumlah"].sum()
        total_keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
        saldo = total_masuk - total_keluar

        m1, m2, m3 = st.columns(3)
        m1.metric("🟢 Total Pemasukan", f"Rp {total_masuk:,.0f}")
        m2.metric("🔴 Total Pengeluaran", f"Rp {total_keluar:,.0f}")
        m3.metric("🔵 Sisa Saldo", f"Rp {saldo:,.0f}")

        st.subheader("📊 Riwayat Transaksi")
        st.dataframe(df[["Keterangan", "Jumlah", "Jenis"]], use_container_width=True)
        
        if st.button("🗑️ Hapus Semua Data Keuangan"):
            conn = sqlite3.connect("database_app.db")
            conn.execute("DELETE FROM keuangan")
            conn.commit()
            conn.close()
            st.rerun()
    else:
        st.info("💡 Belum ada catatan transaksi keuangan.")


# ==========================================
# 💬 FITUR 4: QUOTES INSPIRATIF
# ==========================================
elif pilihan_menu == "💬 Quotes Inspiratif":
    st.markdown("""
        <div class="header-box">
            <h2>💬 Quotes Inspiratif</h2>
            <p style="color: #9ca3af; margin: 0;">Suntikan semangat untuk produktivitas harimu.</p>
        </div>
    """, unsafe_allow_html=True)
    
    quotes = [
        {"q": "Cara terbaik memprediksi masa depan adalah dengan menciptakannya.", "a": "Peter Drucker"},
        {"q": "Satu-satunya cara melakukan pekerjaan hebat adalah mencintai apa yang dilakukan.", "a": "Steve Jobs"},
        {"q": "Kesuksesan adalah hasil dari persiapan, kerja keras, dan belajar dari kegagalan.", "a": "Colin Powell"},
        {"q": "Jangan menunggu kesempatan, ciptakanlah kesempatan itu sendiri.", "a": "Anonim"}
    ]
    
    if "qt" not in st.session_state:
        st.session_state.qt = random.choice(quotes)
        
    st.info(f"“{st.session_state.qt['q']}”\n\n— **{st.session_state.qt['a']}**")
    if st.button("🎲 Quote Lain", type="primary"):
        st.session_state.qt = random.choice(quotes)
        st.rerun()


# ==========================================
# 📥 FITUR 5: MEDIA DOWNLOADER (ANTI TIMEOUT)
# ==========================================
elif pilihan_menu == "📥 Media Downloader":
    st.markdown("""
        <div class="header-box">
            <h2>📥 Universal Media Downloader</h2>
            <p style="color: #9ca3af; margin: 0;">Unduh video/audio YouTube tanpa error.</p>
        </div>
    """, unsafe_allow_html=True)

    url_in = st.text_input("🔗 Tempel URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")
    fmt = st.radio("Format Output:", ["📹 Video (MP4)", "🎵 Audio Saja (MP3)"], horizontal=True)

    st.divider()

    if st.button("🚀 Unduh Media Sekarang", type="primary"):
        if not url_in.strip():
            st.warning("⚠️ Masukkan URL video terlebih dahulu!")
        else:
            with st.spinner("Mengunduh media... Mohon tunggu sebentar."):
                try:
                    out_dir = "downloads"
                    os.makedirs(out_dir, exist_ok=True)
                    
                    ydl_opts = {
            'format': 'best[ext=mp4][height<=720]/best[height<=720]/best' if "Video" in fmt else 'bestaudio/best',
            'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'socket_timeout': 15,
            'extractor_args': {'youtube': {'player_client': ['mweb', 'android']}},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
            }
        }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_in, download=True)
                        title = info.get('title', 'Downloaded_Media')
                        fpath = ydl.prepare_filename(info)

                    st.success(f"✅ Selesai: **{title}**")

                    if os.path.exists(fpath):
                        with open(fpath, "rb") as f:
                            st.download_button(
                                label="💾 Simpan File ke Laptop/HP",
                                data=f,
                                file_name=os.path.basename(fpath),
                                mime="application/octet-stream",
                                type="primary"
                            )
                except Exception as err:
                    st.error(f"❌ Terjadi kesalahan: {err}")import os
import random
import sqlite3
import requests
import pandas as pd
import streamlit as st
import yt_dlp

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Personal Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INIALISASI DATABASE KEUANGAN (SQLITE) ---
def init_db():
    conn = sqlite3.connect("database_app.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS keuangan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT,
            jumlah REAL,
            jenis TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- INITIALIZE SESSION STATE FOR TO-DO ---
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# --- CUSTOM STYLING (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
    }
    .header-box {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("🚀 Personal Dashboard")
st.sidebar.caption("All-in-One Productivity Hub")

pilihan_menu = st.sidebar.radio(
    "Navigasi Fitur",
    [
        "🌤️ Cek Cuaca",
        "📝 To-Do List",
        "💰 Pelacak Keuangan",
        "💬 Quotes Inspiratif",
        "📥 Media Downloader"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Status:** Dashboard Aktif & Siap Digunakan")


# ==========================================
# 🌤️ FITUR 1: CEK CUACA
# ==========================================
if pilihan_menu == "🌤️ Cek Cuaca":
    st.markdown("""
        <div class="header-box">
            <h2>🌤️ Cek Cuaca Real-Time</h2>
            <p style="color: #9ca3af; margin: 0;">Prakiraan cuaca langsung via Open-Meteo API.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, _ = st.columns([2, 1])
    kota = col1.text_input("📍 Masukkan Nama Kota:", placeholder="Contoh: Jakarta, Surabaya, Bali, Tokyo")
    
    if st.button("🔍 Cek Cuaca", type="primary"):
        if not kota.strip():
            st.warning("⚠️ Masukkan nama kota terlebih dahulu!")
        else:
            with st.spinner("Mengambil data cuaca..."):
                try:
                    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={kota}&count=1"
                    geo_res = requests.get(geo_url).json()
                    
                    if "results" in geo_res and len(geo_res["results"]) > 0:
                        lat = geo_res["results"][0]["latitude"]
                        lon = geo_res["results"][0]["longitude"]
                        nama_res = geo_res["results"][0]["name"]
                        negara = geo_res["results"][0].get("country", "")
                        
                        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                        w_res = requests.get(w_url).json()
                        curr = w_res["current_weather"]
                        
                        st.success(f"Lokasi: **{nama_res}, {negara}**")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("🌡️ Suhu Udara", f"{curr['temperature']} °C")
                        c2.metric("💨 Kecepatan Angin", f"{curr['windspeed']} km/h")
                        c3.metric("🧭 Arah Angin", f"{curr['winddirection']}°")
                    else:
                        st.error("❌ Kota tidak ditemukan.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")


# ==========================================
# 📝 FITUR 2: TO-DO LIST
# ==========================================
elif pilihan_menu == "📝 To-Do List":
    st.markdown("""
        <div class="header-box">
            <h2>📝 To-Do List Harian</h2>
            <p style="color: #9ca3af; margin: 0;">Kelola tugas dan target harianmu.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_in, col_bt = st.columns([4, 1])
    tugas_baru = col_in.text_input("Tugas Baru:", placeholder="Tuliskan tugas...", label_visibility="collapsed")
    
    if col_bt.button("➕ Tambah", type="primary", use_container_width=True):
        if tugas_baru.strip():
            st.session_state.todo_list.append({"tugas": tugas_baru.strip(), "selesai": False})
            st.rerun()
            
    st.divider()
    
    if not st.session_state.todo_list:
        st.info("📌 Belum ada tugas ditambahkan.")
    else:
        for idx, item in enumerate(st.session_state.todo_list):
            c_chk, c_txt, c_del = st.columns([0.5, 8, 0.5])
            is_done = c_chk.checkbox("", value=item["selesai"], key=f"todo_{idx}")
            st.session_state.todo_list[idx]["selesai"] = is_done
            
            if is_done:
                c_txt.markdown(f"~~{item['tugas']}~~ ✅")
            else:
                c_txt.write(item["tugas"])
                
            if c_del.button("🗑️", key=f"del_todo_{idx}"):
                st.session_state.todo_list.pop(idx)
                st.rerun()


# ==========================================
# 💰 FITUR 3: PELACAK KEUANGAN (SQLITE)
# ==========================================
elif pilihan_menu == "💰 Pelacak Keuangan":
    st.markdown("""
        <div class="header-box">
            <h2>💰 Pelacak Keuangan Permanen</h2>
            <p style="color: #9ca3af; margin: 0;">Catatan keuangan tersimpan aman di Database SQLite.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_keuangan", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        ket = c1.text_input("Keterangan", placeholder="Contoh: Gaji, Kopi")
        nom = c2.number_input("Nominal (Rp)", min_value=0, step=5000)
        jns = c3.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
        
        if st.form_submit_button("💳 Simpan Transaksi", type="primary", use_container_width=True):
            if ket.strip() and nom > 0:
                conn = sqlite3.connect("database_app.db")
                cur = conn.cursor()
                cur.execute("INSERT INTO keuangan (keterangan, jumlah, jenis) VALUES (?, ?, ?)", (ket, nom, jns))
                conn.commit()
                conn.close()
                st.success("Data berhasil disimpan!")
                st.rerun()
            else:
                st.warning("⚠️ Lengkapi data transaksi dengan benar!")

    st.divider()

    # Load Data dari SQLite
    conn = sqlite3.connect("database_app.db")
    df = pd.read_sql_query("SELECT id, keterangan as Keterangan, jumlah as Jumlah, jenis as Jenis FROM keuangan", conn)
    conn.close()

    if not df.empty:
        total_masuk = df[df["Jenis"] == "Pemasukan"]["Jumlah"].sum()
        total_keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
        saldo = total_masuk - total_keluar

        m1, m2, m3 = st.columns(3)
        m1.metric("🟢 Total Pemasukan", f"Rp {total_masuk:,.0f}")
        m2.metric("🔴 Total Pengeluaran", f"Rp {total_keluar:,.0f}")
        m3.metric("🔵 Sisa Saldo", f"Rp {saldo:,.0f}")

        st.subheader("📊 Riwayat Transaksi")
        st.dataframe(df[["Keterangan", "Jumlah", "Jenis"]], use_container_width=True)
        
        if st.button("🗑️ Hapus Semua Data Keuangan"):
            conn = sqlite3.connect("database_app.db")
            conn.execute("DELETE FROM keuangan")
            conn.commit()
            conn.close()
            st.rerun()
    else:
        st.info("💡 Belum ada catatan transaksi keuangan.")


# ==========================================
# 💬 FITUR 4: QUOTES INSPIRATIF
# ==========================================
elif pilihan_menu == "💬 Quotes Inspiratif":
    st.markdown("""
        <div class="header-box">
            <h2>💬 Quotes Inspiratif</h2>
            <p style="color: #9ca3af; margin: 0;">Suntikan semangat untuk produktivitas harimu.</p>
        </div>
    """, unsafe_allow_html=True)
    
    quotes = [
        {"q": "Cara terbaik memprediksi masa depan adalah dengan menciptakannya.", "a": "Peter Drucker"},
        {"q": "Satu-satunya cara melakukan pekerjaan hebat adalah mencintai apa yang dilakukan.", "a": "Steve Jobs"},
        {"q": "Kesuksesan adalah hasil dari persiapan, kerja keras, dan belajar dari kegagalan.", "a": "Colin Powell"},
        {"q": "Jangan menunggu kesempatan, ciptakanlah kesempatan itu sendiri.", "a": "Anonim"}
    ]
    
    if "qt" not in st.session_state:
        st.session_state.qt = random.choice(quotes)
        
    st.info(f"“{st.session_state.qt['q']}”\n\n— **{st.session_state.qt['a']}**")
    if st.button("🎲 Quote Lain", type="primary"):
        st.session_state.qt = random.choice(quotes)
        st.rerun()


# ==========================================
# 📥 FITUR 5: MEDIA DOWNLOADER (ANTI TIMEOUT)
# ==========================================
elif pilihan_menu == "📥 Media Downloader":
    st.markdown("""
        <div class="header-box">
            <h2>📥 Universal Media Downloader</h2>
            <p style="color: #9ca3af; margin: 0;">Unduh video/audio YouTube tanpa error.</p>
        </div>
    """, unsafe_allow_html=True)

    url_in = st.text_input("🔗 Tempel URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")
    fmt = st.radio("Format Output:", ["📹 Video (MP4)", "🎵 Audio Saja (MP3)"], horizontal=True)

    st.divider()

    if st.button("🚀 Unduh Media Sekarang", type="primary"):
        if not url_in.strip():
            st.warning("⚠️ Masukkan URL video terlebih dahulu!")
        else:
            with st.spinner("Mengunduh media... Mohon tunggu sebentar."):
                try:
                    out_dir = "downloads"
                    os.makedirs(out_dir, exist_ok=True)
                    
                    ydl_opts = {
            'format': 'best[ext=mp4][height<=720]/best[height<=720]/best' if "Video" in fmt else 'bestaudio/best',
            'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'socket_timeout': 15,
            'extractor_args': {'youtube': {'player_client': ['mweb', 'android']}},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
            }
        }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_in, download=True)
                        title = info.get('title', 'Downloaded_Media')
                        fpath = ydl.prepare_filename(info)

                    st.success(f"✅ Selesai: **{title}**")

                    if os.path.exists(fpath):
                        with open(fpath, "rb") as f:
                            st.download_button(
                                label="💾 Simpan File ke Laptop/HP",
                                data=f,
                                file_name=os.path.basename(fpath),
                                mime="application/octet-stream",
                                type="primary"
                            )
                except Exception as err:
                    st.error(f"❌ Terjadi kesalahan: {err}")

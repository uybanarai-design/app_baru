import os
import random
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

# --- CUSTOM CSS UNTUK TAMPILAN MODERN ---
st.markdown("""
    <style>
    /* Styling Container Utama */
    .main {
        background-color: #0e1117;
    }
    
    /* Styling Card / Box Metrik */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
    }
    
    /* Custom Header Box */
    .header-box {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    
    /* Styling Tombol Utama */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

if "keuangan" not in st.session_state:
    st.session_state.keuangan = []

# --- SIDEBAR / MENU UTAMA ---
st.sidebar.image("https://em-content.zobj.net/source/apple/354/rocket_1f680.png", width=60)
st.sidebar.title("Personal Dashboard")
st.sidebar.caption("Workspace Produktivitas All-in-One")

pilihan_menu = st.sidebar.radio(
    "Navigasi Feature",
    [
        "🌤️ Cek Cuaca",
        "📝 To-Do List",
        "💰 Pelacak Keuangan",
        "💬 Quotes Inspiratif",
        "📥 Media Downloader"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("✨ **Tips:** Pilih menu di atas untuk berganti antar fitur produktivitas.")


# --- FITUR 1: CEK CUACA ---
if pilihan_menu == "🌤️ Cek Cuaca":
    st.markdown("""
        <div class="header-box">
            <h2>🌤️ Cek Cuaca Real-Time</h2>
            <p style="color: #9ca3af; margin: 0;">Pantau prakiraan cuaca terkini di seluruh kota dunia.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, _ = st.columns([2, 1])
    with col1:
        kota = st.text_input("📍 Masukkan Nama Kota:", placeholder="Contoh: Jakarta, Surabaya, Bali, Tokyo")
    
    if st.button("🔍 Cari Informasi Cuaca", type="primary"):
        if not kota.strip():
            st.warning("⚠️ Harap masukkan nama kota terlebih dahulu!")
        else:
            with st.spinner("Mengambil data dari stasiun cuaca..."):
                try:
                    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={kota}&count=1"
                    geo_res = requests.get(geo_url).json()
                    
                    if "results" in geo_res and len(geo_res["results"]) > 0:
                        lat = geo_res["results"][0]["latitude"]
                        lon = geo_res["results"][0]["longitude"]
                        nama_res = geo_res["results"][0]["name"]
                        negara = geo_res["results"][0].get("country", "")
                        
                        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                        weather_res = requests.get(weather_url).json()
                        curr = weather_res["current_weather"]
                        
                        st.success(f"Lokasi Ditemukan: **{nama_res}, {negara}**")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("🌡️ Suhu Udara", f"{curr['temperature']} °C")
                        c2.metric("💨 Kecepatan Angin", f"{curr['windspeed']} km/h")
                        c3.metric("🧭 Arah Angin", f"{curr['winddirection']}°")
                    else:
                        st.error("❌ Nama kota tidak ditemukan. Coba periksa kembali ejaannya.")
                except Exception as e:
                    st.error(f"❌ Gagal mengambil data cuaca: {e}")


# --- FITUR 2: TO-DO LIST ---
elif pilihan_menu == "📝 To-Do List":
    st.markdown("""
        <div class="header-box">
            <h2>📝 To-Do List Harian</h2>
            <p style="color: #9ca3af; margin: 0;">Atur dan selesaikan target tugas harianmu.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_input, col_btn = st.columns([4, 1])
    tugas_baru = col_input.text_input("Tugas Baru:", placeholder="Contoh: Review Laporan Bulanan", label_visibility="collapsed")
    
    if col_btn.button("➕ Tambah Task", type="primary", use_container_width=True):
        if tugas_baru.strip():
            st.session_state.todo_list.append({"tugas": tugas_baru.strip(), "selesai": False})
            st.rerun()
        else:
            st.warning("⚠️ Tuliskan rencana tugasmu!")
            
    st.divider()
    
    if not st.session_state.todo_list:
        st.info("📌 Belum ada daftar tugas. Yuk mulai dengan menambah tugas baru di atas!")
    else:
        for idx, item in enumerate(st.session_state.todo_list):
            c_check, c_text, c_del = st.columns([0.5, 8, 0.5])
            is_done = c_check.checkbox("", value=item["selesai"], key=f"check_{idx}")
            st.session_state.todo_list[idx]["selesai"] = is_done
            
            if is_done:
                c_text.markdown(f"~~{item['tugas']}~~ ✅", unsafe_allow_html=True)
            else:
                c_text.write(item["tugas"])
                
            if c_del.button("🗑️", key=f"del_{idx}"):
                st.session_state.todo_list.pop(idx)
                st.rerun()


# --- FITUR 3: PELACAK KEUANGAN ---
elif pilihan_menu == "💰 Pelacak Keuangan":
    st.markdown("""
        <div class="header-box">
            <h2>💰 Pelacak Keuangan</h2>
            <p style="color: #9ca3af; margin: 0;">Catat dan kontrol arus kas pemasukan serta pengeluaran harian.</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_keuangan", clear_on_submit=True):
        col1, col2, col3 = st.columns([3, 2, 2])
        keterangan = col1.text_input("Keterangan Transaksi", placeholder="Gaji, Kopi, Transportasi")
        jumlah = col2.number_input("Nominal (Rp)", min_value=0, step=5000)
        jenis = col3.selectbox("Kategori", ["Pemasukan", "Pengeluaran"])
        
        if st.form_submit_button("💳 Simpan Catatan", type="primary", use_container_width=True):
            if keterangan.strip() and jumlah > 0:
                st.session_state.keuangan.append({
                    "Keterangan": keterangan,
                    "Jumlah": jumlah,
                    "Jenis": jenis
                })
                st.success("Catatan transaksi berhasil disimpan!")
                st.rerun()
            else:
                st.warning("⚠️ Isikan keterangan dan nominal angka secara valid!")
                
    st.divider()
    
    if st.session_state.keuangan:
        df = pd.DataFrame(st.session_state.keuangan)
        
        total_masuk = df[df["Jenis"] == "Pemasukan"]["Jumlah"].sum()
        total_keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
        saldo = total_masuk - total_keluar
        
        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 Total Pemasukan", f"Rp {total_masuk:,.0f}")
        c2.metric("🔴 Total Pengeluaran", f"Rp {total_keluar:,.0f}")
        c3.metric("🔵 Sisa Saldo", f"Rp {saldo:,.0f}")
        
        st.subheader("📋 Riwayat Transaksi")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("💡 Belum ada riwayat keuangan yang dicatat.")


# --- FITUR 4: QUOTES INSPIRATIF ---
elif pilihan_menu == "💬 Quotes Inspiratif":
    st.markdown("""
        <div class="header-box">
            <h2>💬 Quotes Inspiratif</h2>
            <p style="color: #9ca3af; margin: 0;">Dapatkan suntikan semangat harian untuk menunjang harimu.</p>
        </div>
    """, unsafe_allow_html=True)
    
    daftar_quotes = [
        {"quote": "Cara terbaik untuk memprediksi masa depan adalah dengan menciptakannya.", "author": "Peter Drucker"},
        {"quote": "Satu-satunya cara untuk melakukan pekerjaan hebat adalah dengan mencintai apa yang Anda lakukan.", "author": "Steve Jobs"},
        {"quote": "Kesuksesan adalah hasil dari persiapan, kerja keras, dan belajar dari kegagalan.", "author": "Colin Powell"},
        {"quote": "Jangan menunggu kesempatan, ciptakanlah kesempatan itu sendiri.", "author": "Anonim"},
        {"quote": "Perjalanan ribuan mil dimulai dengan satu langkah kecil.", "author": "Lao Tzu"}
    ]
    
    if "current_quote" not in st.session_state:
        st.session_state.current_quote = random.choice(daftar_quotes)
        
    st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); padding: 30px; border-radius: 12px; text-align: center; margin: 20px 0;">
            <p style="font-size: 20px; font-style: italic; color: #e5e7eb;">“{st.session_state.current_quote['quote']}”</p>
            <h4 style="color: #60a5fa; margin-top: 15px;">— {st.session_state.current_quote['author']}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎲 Ambil Quote Baru", type="primary"):
        st.session_state.current_quote = random.choice(daftar_quotes)
        st.rerun()


# ---------------------------------------------------------
# MENU 5: MEDIA DOWNLOADER (API BYPASS)
# ---------------------------------------------------------
elif "Media Downloader" in pilihan_menu:
    import requests

    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">📺 Universal Media Downloader</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Unduh video atau audio YouTube secara instan & bebas blokir bot.</p>
        </div>
    """, unsafe_allow_html=True)

    url_in = st.text_input("🔗 Tempel URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")
    fmt = st.radio("Format Output:", ["📹 Video (MP4)", "🎵 Audio Saja (MP3)"], horizontal=True)

    st.divider()

    if st.button("🚀 Unduh Media Sekarang", type="primary"):
        if not url_in.strip():
            st.warning("⚠️ Masukkan URL video terlebih dahulu!")
        else:
            with st.spinner("Sedang memproses tautan unduhan... Mohon tunggu sebentar."):
                try:
                    # Menghubungi API Cobalt untuk bypass proteksi YouTube
                    api_url = "https://api.cobalt.tools/api/json"
                    payload = {
                        "url": url_in.strip(),
                        "downloadMode": "audio" if "Audio" in fmt else "auto",
                        "audioFormat": "mp3",
                        "videoQuality": "max"
                    }
                    headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    }

                    res = requests.post(api_url, json=payload, headers=headers, timeout=15)
                    data = res.json()

                    if res.status_code == 200 and data.get("status") in ["tunnel", "redirect"]:
                        download_link = data.get("url")
                        st.success("✅ Tautan unduhan berhasil dibuat!")
                        st.link_button("💾 Klik di Sini untuk Unduh File", download_link, type="primary")
                    else:
                        error_detail = data.get("text", "Gagal memproses URL media.")
                        st.error(f"❌ Terjadi kesalahan: {error_detail}")

                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan jaringan: {e}")

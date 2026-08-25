import os
import random
import requests
import io
import pandas as pd
import streamlit as st
import yt_dlp

st.set_page_config(page_title="Personal Dashboard", page_icon="🚀", layout="wide")

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
st.sidebar.title("🚀 Personal Dashboard")
st.sidebar.caption("All-in-One Productivity Hub")

pilihan_menu = st.sidebar.radio(
    "Navigasi Fitur",
    [
        "🌤️ Cek Cuaca",
        "📝 To-Do List",
        "💰 Pelacak Keuangan",
        "🎵 Pemutar Musik",
        "💬 Quotes Inspiratif",
        "📥 Media Downloader"
    ]
)

st.sidebar.divider()
st.sidebar.info("💡 Status: Dashboard Aktif & Siap Digunakan")

# =========================================================
# MENU 1: CEK CUACA (OPEN-METEO API)
# =========================================================
if pilihan_menu == "🌤️ Cek Cuaca" or "Cek Cuaca" in pilihan_menu:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">🌤️ Cek Cuaca Real-Time</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Prakiraan cuaca langsung via Open-Meteo API.</p>
        </div>
    """, unsafe_allow_html=True)

    kota = st.text_input("📍 Masukkan Nama Kota:", placeholder="Contoh: Jakarta, Surabaya, Bali, Tokyo")

    if st.button("🔍 Cek Cuaca", type="primary"):
        if not kota.strip():
            st.warning("⚠️ Masukkan nama kota terlebih dahulu!")
        else:
            with st.spinner(f"Mengambil data cuaca untuk {kota}..."):
                try:
                    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={kota.strip()}&count=1&language=id&format=json"
                    geo_res = requests.get(geo_url, timeout=10).json()

                    if "results" in geo_res and len(geo_res["results"]) > 0:
                        lat = geo_res["results"][0]["latitude"]
                        lon = geo_res["results"][0]["longitude"]
                        nama_res = geo_res["results"][0]["name"]
                        negara = geo_res["results"][0].get("country", "")

                        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                        w_res = requests.get(weather_url, timeout=10).json()

                        curr = w_res.get("current_weather", {})
                        temp = curr.get("temperature", "-")
                        wind = curr.get("windspeed", "-")
                        code = curr.get("weathercode", 0)

                        status_cuaca = "☀️ Cerah" if code == 0 else "⛅ Berawan" if code in [1, 2, 3] else "🌧️ Hujan" if code in [51, 61, 63, 80] else "🌩️ Badai"

                        st.success(f"📍 Hasil Cuaca untuk **{nama_res}, {negara}**")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("🌡️ Suhu", f"{temp} °C")
                        col2.metric("🌤️ Kondisi", status_cuaca)
                        col3.metric("💨 Angin", f"{wind} km/h")
                    else:
                        st.error("❌ Kota tidak ditemukan. Coba ejaan nama kota lain.")

                except Exception as e:
                    st.error(f"❌ Gagal mengambil data cuaca: {e}")

# =========================================================
# MENU 2: TO-DO LIST (SESSION STATE)
# =========================================================
elif pilihan_menu == "📝 To-Do List" or "To-Do List" in pilihan_menu:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">📝 To-Do List & Productivity Planner</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Kelola daftar tugas harian Anda secara fleksibel.</p>
        </div>
    """, unsafe_allow_html=True)

    if "todos" not in st.session_state:
        st.session_state.todos = []

    col_in, col_btn = st.columns([4, 1])
    with col_in:
        new_task = st.text_input("Tugas Baru:", placeholder="Tuliskan tugas harianmu di sini...", label_visibility="collapsed")
    with col_btn:
        if st.button("➕ Tambah", type="primary", use_container_width=True):
            if new_task.strip():
                st.session_state.todos.append({"task": new_task.strip(), "done": False})
                st.rerun()

    st.divider()

    if not st.session_state.todos:
        st.info("📌 Belum ada tugas. Tambahkan tugas pertama Anda di atas!")
    else:
        for idx, item in enumerate(st.session_state.todos):
            c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
            is_done = c1.checkbox("", value=item["done"], key=f"check_{idx}")
            st.session_state.todos[idx]["done"] = is_done
            
            if is_done:
                c2.write(f"~~{item['task']}~~")
            else:
                c2.write(item["task"])
                
            if c3.button("🗑️", key=f"del_{idx}"):
                st.session_state.todos.pop(idx)
                st.rerun()

# =========================================================
# MENU 3: PELACAK KEUANGAN (FITUR EKSPOR CSV & EXCEL)
# =========================================================
elif pilihan_menu == "💰 Pelacak Keuangan" or "Pelacak Keuangan" in pilihan_menu:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #f59e0b; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">💰 Pelacak Keuangan Ringkas</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Catat, monitor, dan ekspor arus kas harian Anda.</p>
        </div>
    """, unsafe_allow_html=True)

    if "transaksi" not in st.session_state:
        st.session_state.transaksi = []

    with st.form("form_keuangan", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        ket = col1.text_input("Keterangan", placeholder="Misal: Gaji, Belanja, Makan")
        tipe = col2.selectbox("Jenis", ["Pemasukan", "Pengeluaran"])
        jumlah = col3.number_input("Jumlah (Rp)", min_value=0, step=1000)
        submitted = st.form_submit_button("💾 Simpan Transaksi", type="primary")

        if submitted and ket and jumlah > 0:
            st.session_state.transaksi.append({
                "Keterangan": ket,
                "Jenis": tipe,
                "Jumlah (Rp)": jumlah if tipe == "Pemasukan" else -jumlah
            })
            st.success("Transaksi berhasil dicatat!")

    if st.session_state.transaksi:
        df = pd.DataFrame(st.session_state.transaksi)
        masuk = df[df["Jumlah (Rp)"] > 0]["Jumlah (Rp)"].sum()
        keluar = abs(df[df["Jumlah (Rp)"] < 0]["Jumlah (Rp)"].sum())
        saldo = masuk - keluar

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Pemasukan", f"Rp {masuk:,.0f}")
        m2.metric("Total Pengeluaran", f"Rp {keluar:,.0f}")
        m3.metric("Saldo Akhir", f"Rp {saldo:,.0f}")

        st.subheader("📋 Riwayat Transaksi")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.subheader("📥 Ekspor Laporan Keuangan")
        col_csv, col_excel = st.columns(2)

        # 1. Ekspor CSV
        csv_data = df.to_csv(index=False).encode('utf-8')
        col_csv.download_button(
            label="📄 Unduh Laporan (CSV)",
            data=csv_data,
            file_name="laporan_keuangan.csv",
            mime="text/csv",
            use_container_width=True
        )

        # 2. Ekspor Excel (.xlsx)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Keuangan')
        excel_data = buffer.getvalue()

        col_excel.download_button(
            label="📊 Unduh Laporan (Excel)",
            data=excel_data,
            file_name="laporan_keuangan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )

# =========================================================
# MENU 4: PEMUTAR MUSIK (LO-FI & RELAXING AUDIO)
# =========================================================
elif pilihan_menu == "🎵 Pemutar Musik" or "Pemutar Musik" in pilihan_menu:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #ec4899; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">🎵 Pemutar Musik & Suara Santai</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Dengarkan musik Lo-Fi dan ambient sound untuk menemani belajar atau bekerja.</p>
        </div>
    """, unsafe_allow_html=True)

    tracks = {
        "☕ Chill Lo-Fi Beats": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🌧️ Suara Hujan & Alam": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "🌌 Deep Focus Ambient": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "🎸 Smooth Acoustic Vibes": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
    }

    selected_track = st.selectbox("🎧 Pilih Audio / Musik:", list(tracks.keys()))
    
    st.markdown(f"**Sedang Memutar:** `{selected_track}`")
    st.audio(tracks[selected_track], format="audio/mp3")

    st.divider()
    st.caption("💡 *Tips: Kamu juga bisa mengganti link MP3 di atas dengan file MP3 milikmu sendiri atau link radio stream favorit.*")

# =========================================================
# MENU 5: QUOTES INSPIRATIF
# =========================================================
elif pilihan_menu == "💬 Quotes Inspiratif" or "Quotes Inspiratif" in pilihan_menu:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #8b5cf6; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">💬 Quotes Inspiratif</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Pengingat dan motivasi harian untuk semangat berkarya.</p>
        </div>
    """, unsafe_allow_html=True)

    quotes_list = [
        ("Cara terbaik untuk memulai adalah dengan berhenti berbicara dan mulai melakukan.", "Walt Disney"),
        ("Jangan menunggu kesempatan, ciptakan kesempatan itu sendiri.", "George Bernard Shaw"),
        ("Kesuksesan adalah hasil dari persiapan, kerja keras, dan belajar dari kegagalan.", "Colin Powell"),
        ("Fokus pada prosesnya, hasil terbaik akan mengikuti dengan sendirinya.", "Anonim"),
        ("Satu-satunya cara untuk melakukan pekerjaan besar adalah dengan mencintai apa yang Anda lakukan.", "Steve Jobs")
    ]

    if "current_quote" not in st.session_state:
        st.session_state.current_quote = random.choice(quotes_list)

    if st.button("🎲 Ambil Quote Acak", type="primary"):
        st.session_state.current_quote = random.choice(quotes_list)

    q, a = st.session_state.current_quote
    st.markdown(f"""
        <div style="background-color: #0f172a; padding: 30px; border-radius: 10px; margin-top: 20px; text-align: center;">
            <h3 style="color: #f1f5f9; font-style: italic;">"{q}"</h3>
            <p style="color: #94a3b8; font-weight: bold;">— {a}</p>
        </div>
    """, unsafe_allow_html=True)

# =========================================================
# MENU 6: MEDIA DOWNLOADER (HYBRID NATIVE & FALLBACK)
# =========================================================
elif "Media Downloader" in pilihan_menu:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #ef4444; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">📺 Universal Media Downloader</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Unduh video atau audio YouTube secara langsung.</p>
        </div>
    """, unsafe_allow_html=True)

    url_in = st.text_input("🔗 Tempel URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")
    fmt = st.radio("Format Output:", ["📹 Video (MP4)", "🎵 Audio Saja (MP3)"], horizontal=True)

    st.divider()

    if st.button("🚀 Unduh Media Sekarang", type="primary"):
        if not url_in.strip():
            st.warning("⚠️ Masukkan URL video terlebih dahulu!")
        else:
            with st.spinner("Sedang memproses dan mengunduh file... Mohon tunggu sebentar."):
                try:
                    out_dir = "downloads"
                    os.makedirs(out_dir, exist_ok=True)

                    ydl_opts = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if "Video" in fmt else 'bestaudio/best',
                        'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'socket_timeout': 15,
                        'extractor_args': {
                            'youtube': {
                                'player_client': ['android', 'ios', 'mweb']
                            }
                        },
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
                        }
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url_in.strip(), download=True)
                        file_path = ydl.prepare_filename(info)

                    if os.path.exists(file_path):
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="💾 Klik di Sini untuk Mengunduh File",
                                data=file,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4" if "Video" in fmt else "audio/mp3",
                                type="primary"
                            )
                        st.success("✅ File berhasil diunduh secara langsung!")

                except Exception:
                    st.warning("⚠️ Server Cloud terdeteksi bot oleh YouTube. Gunakan tautan unduh langsung via Cobalt Web di bawah ini:")
                    st.link_button("🌐 Unduh Langsung via Cobalt Web", f"https://cobalt.tools/#url={url_in.strip()}", type="primary", use_container_width=True)

    if url_in.strip():
        st.divider()
        st.subheader("🎬 Pratinjau Video")
        st.video(url_in.strip())

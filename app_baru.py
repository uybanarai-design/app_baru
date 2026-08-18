import streamlit as st
import requests

st.set_page_config(page_title="Personal Dashboard", page_icon="🚀", layout="wide")

# Navigation Sidebar
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

st.sidebar.divider()
st.sidebar.info("💡 Status: Dashboard Aktif & Siap Digunakan")

# ---------------------------------------------------------
# MENU 1: CEK CUACA
# ---------------------------------------------------------
if pilihan_menu == "🌤️ Cek Cuaca":
    st.header("🌤️ Cek Cuaca Real-Time")
    st.write("Fitur cek cuaca siap digunakan.")

# ---------------------------------------------------------
# MENU 2: TO-DO LIST
# ---------------------------------------------------------
elif pilihan_menu == "📝 To-Do List":
    st.header("📝 To-Do List")
    st.write("Fitur daftar tugas siap digunakan.")

# ---------------------------------------------------------
# MENU 3: PELACAK KEUANGAN
# ---------------------------------------------------------
elif pilihan_menu == "💰 Pelacak Keuangan":
    st.header("💰 Pelacak Keuangan")
    st.write("Fitur keuangan siap digunakan.")

# ---------------------------------------------------------
# MENU 4: QUOTES INSPIRATIF
# ---------------------------------------------------------
elif pilihan_menu == "💬 Quotes Inspiratif":
    st.header("💬 Quotes Inspiratif")
    st.write("Fitur quotes siap digunakan.")

# ---------------------------------------------------------
# MENU 5: MEDIA DOWNLOADER (YT-DLP NATIVE)
# ---------------------------------------------------------
elif pilihan_menu == "📥 Media Downloader" or "Media Downloader" in pilihan_menu:
    import os
    import yt_dlp

    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">📺 Universal Media Downloader</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Unduh video atau audio YouTube secara langsung via yt-dlp.</p>
        </div>
    """, unsafe_allow_html=True)

    url_in = st.text_input("🔗 Tempel URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")
    fmt = st.radio("Format Output:", ["📹 Video (MP4)", "🎵 Audio Saja (MP3)"], horizontal=True)

    st.divider()

    if st.button("🚀 Unduh Media Sekarang", type="primary"):
        if not url_in.strip():
            st.warning("⚠️ Masukkan URL video terlebih dahulu!")
        else:
            with st.spinner("Sedang mengunduh file ke server... Mohon tunggu sebentar."):
                try:
                    out_dir = "downloads"
                    os.makedirs(out_dir, exist_ok=True)

                    # Opsi yt-dlp dengan penyamaran Client Android agar lolos blokir IP Cloud
                    ydl_opts = {
                        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if "Video" in fmt else 'bestaudio/best',
                        'outtmpl': os.path.join(out_dir, '%(title)s.%(ext)s'),
                        'quiet': True,
                        'no_warnings': True,
                        'nocheckcertificate': True,
                        'socket_timeout': 30,
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

                    # Jika file berhasil diunduh, tampilkan tombol download bawaan Streamlit
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as file:
                            btn = st.download_button(
                                label="💾 Klik di Sini untuk Mengunduh File",
                                data=file,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4" if "Video" in fmt else "audio/mp3",
                                type="primary"
                            )
                        st.success("✅ File berhasil diproses!")

                except Exception as e:
                    st.error(f"❌ Gagal mengunduh media: {e}")

    if url_in.strip():
        st.divider()
        st.subheader("🎬 Pratinjau Video")
        st.video(url_in.strip())

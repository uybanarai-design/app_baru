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
# MENU 5: MEDIA DOWNLOADER (COBALT API)
# ---------------------------------------------------------
elif pilihan_menu == "📥 Media Downloader" or "Media Downloader" in pilihan_menu:
    st.markdown("""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 20px;">
            <h2 style="color: white; margin: 0;">📺 Universal Media Downloader</h2>
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Unduh video atau audio YouTube secara instan.</p>
        </div>
    """, unsafe_allow_html=True)

    url_in = st.text_input("🔗 Tempel URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")
    fmt = st.radio("Format Output:", ["📹 Video (MP4)", "🎵 Audio Saja (MP3)"], horizontal=True)

    st.divider()

    if st.button("🚀 Unduh Media Sekarang", type="primary"):
        if not url_in.strip():
            st.warning("⚠️ Masukkan URL video terlebih dahulu!")
        else:
            with st.spinner("Sedang memproses permintaan via Cobalt API v10..."):
                try:
                    # Menggunakan API Cobalt v10 Official
                    api_url = "https://api.cobalt.tools/"
                    payload = {
                        "url": url_in.strip(),
                        "downloadMode": "audio" if "Audio" in fmt else "auto",
                        "audioFormat": "mp3",
                        "videoQuality": "720"
                    }
                    headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    }

                    res = requests.post(api_url, json=payload, headers=headers, timeout=10)
                    data = res.json()

                    if res.status_code == 200 and (data.get("status") in ["tunnel", "redirect", "picker"] or data.get("url")):
                        download_link = data.get("url")
                        st.success("✅ Tautan unduhan berhasil dibuat!")
                        st.link_button("💾 Klik di Sini untuk Unduh File", download_link, type="primary")
                    else:
                        # Jika API menolak (karena bot protection / JWT), berikan link akses langsung ke Cobalt Web
                        st.warning("⚠️ API Cobalt memblokir permintaan otomatis dari server Cloud. Gunakan tautan langsung di bawah:")
                        st.link_button("🌐 Buka & Unduh Langsung via Cobalt Web", f"https://cobalt.tools/#url={url_in.strip()}", type="primary", use_container_width=True)

                except Exception as e:
                    # Cadangan jika terjadi kendala koneksi API
                    st.warning("⚠️ Gagal terhubung ke API Cobalt. Silakan unduh langsung via web Cobalt:")
                    st.link_button("🌐 Buka & Unduh Langsung via Cobalt Web", f"https://cobalt.tools/#url={url_in.strip()}", type="primary", use_container_width=True)

    if url_in.strip():
        st.divider()
        st.subheader("🎬 Pratinjau Video")
        st.video(url_in.strip())

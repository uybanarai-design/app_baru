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
elif pilihan_menu == "📥 Media Downloader":
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
                    # Memanggil API Cobalt
                    # Memanggil API Cobalt v10 Terbaru
                    api_url = "https://cobalt.qewertyy.dev/"
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

                    res = requests.post(api_url, json=payload, headers=headers, timeout=15)
                    data = res.json()

                    if res.status_code == 200 and data.get("status") in ["tunnel", "redirect", "picker"]:
                        download_link = data.get("url")
                        st.success("✅ Tautan unduhan berhasil dibuat!")
                        st.link_button("💾 Klik di Sini untuk Unduh File", download_link, type="primary")
                    else:
                        error_detail = data.get("text") or data.get("error", {}).get("code", "Gagal memproses URL media.")
                        st.error(f"❌ Terjadi kesalahan: {error_detail}")

                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan jaringan: {e}")

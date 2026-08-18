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
            <p style="color: #9ca3af; margin: 5px 0 0 0;">Putar video langsung di Streamlit atau unduh secara instan.</p>
        </div>
    """, unsafe_allow_html=True)

    url_in = st.text_input("🔗 Tempel URL Video YouTube:", placeholder="https://www.youtube.com/watch?v=...")

    st.divider()

    if url_in.strip():
        st.subheader("🎬 Pratinjau Video")
        st.video(url_in.strip())

        st.subheader("📥 Pilihan Layanan Unduh")
        st.info("Pilih salah satu tombol di bawah untuk mengunduh media tanpa error server:")

        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📹 Unduh via Cobalt Web", f"https://cobalt.tools/#url={url_in.strip()}", type="primary", use_container_width=True)
        with col2:
            st.link_button("🎵 Unduh MP3/MP4 via SaveFrom", f"https://en.savefrom.net/1-youtube-video-downloader-3v1/?url={url_in.strip()}", use_container_width=True)

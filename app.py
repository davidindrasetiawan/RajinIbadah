import streamlit as st
import pandas as pd

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Dashboard Harga Pangan Banten",
    layout="wide"
)

# ======================================================
# JUDUL UTAMA
# ======================================================
st.title("Dashboard Harga Komoditas Pangan Utama di Banten")

st.markdown("""
Dashboard ini menggambarkan dinamika harga tujuh komoditas pangan strategis di Provinsi Banten 
selama periode 2019 hingga 2024, yaitu beras, daging ayam, daging sapi, bawang merah, cabai rawit, 
minyak goreng, dan gula pasir. Visualisasi data menunjukkan bahwa meskipun setiap komoditas 
memiliki karakteristik pergerakan harga yang berbeda, secara umum terdapat kecenderungan 
kenaikan harga dalam jangka panjang.
""")

# ======================================================
# FOTO DI ATAS NAMA ANGGOTA
# ======================================================
st.image(
    "foto/foto.jpg",   # pastikan file ada
    caption="Ilustrasi",
    use_container_width=True
)

# ======================================================
# NAMA ANGGOTA
# ======================================================
st.subheader("Anggota Kelompok")

anggota = [
    "Jibral Yusuf Nazar (021002301001)",
    "David Indra Setiawan (021002305021)",
    "Dimas Wahyu Saputra (021002302003)"
]

for a in anggota:
    st.write(f"- {a}")

# ======================================================
# LOAD DATA CSV
# ======================================================
file_path = "data_bengkulu.csv"

try:
    df = pd.read_csv(file_path)

    # Membersihkan nama kolom
    df.columns = df.columns.str.strip()

    # Konversi kolom tahun menjadi datetime
    df["tahun_date"] = pd.to_datetime(
        df["tahun"].astype(str).str.replace(" ", ""),
        errors="coerce"
    )

    # ==================================================
    # SIDEBAR FILTER
    # ==================================================
    st.sidebar.header("Filter Tampilan")
    show_table = st.sidebar.checkbox(
        "Tampilkan Tabel Data",
        value=True
    )

    if show_table:
        st.subheader("Data Lengkap")
        st.dataframe(df)
        st.caption(f"Menampilkan total {len(df)} baris data.")

    # ==================================================
    # BAGIAN ANALISIS GRAFIK
    # ==================================================
    st.divider()
    st.header("Analisis Harga Pangan Tahun 2019–2024 di Provinsi Banten")
    st.markdown("Grafik berikut menunjukkan pergerakan harga komoditas pangan dari waktu ke waktu.")

    target_komoditas = [
        "Beras",
        "Daging Ayam",
        "Daging Sapi",
        "Bawang Merah",
        "Cabai Rawit",
        "Minyak Goreng",
        "Gula Pasir"
    ]

    komoditas_plot = [
        col for col in target_komoditas
        if col in df.columns
    ]

    if komoditas_plot:
        selected_commodities = st.multiselect(
            "Pilih Komoditas untuk Ditampilkan:",
            options=komoditas_plot,
            default=komoditas_plot
        )

        if selected_commodities:
            chart_data = df.set_index("tahun_date")[selected_commodities]

            st.subheader("Dinamika Harga Komoditas Pangan")
            st.line_chart(chart_data)

            # ==================================================
            # PENJELASAN (VERSI BARU – LENGKAP)
            # ==================================================
            
            st.markdown("""
### 📊 Analisis Perkembangan Harga Komoditas Pangan Utama di Provinsi Banten (2019–2024)

**Beras** menunjukkan kondisi harga yang relatif stabil pada periode 2019 hingga 2022. 
Stabilitas ini mencerminkan peran pemerintah dalam menjaga ketersediaan stok dan stabilisasi 
harga. Namun, pada periode 2023 hingga 2024 terlihat tren kenaikan harga yang cukup signifikan, 
yang mengindikasikan adanya tekanan inflasi, peningkatan biaya produksi, serta gangguan iklim 
yang memengaruhi hasil panen.

**Cabai Rawit** merupakan komoditas dengan tingkat volatilitas harga yang tinggi. Fluktuasi 
harga yang tajam dari waktu ke waktu dipengaruhi oleh faktor cuaca, musim panen, serta 
keterbatasan pasokan. Kondisi ini menyebabkan harga cabai rawit dapat berubah secara cepat, 
baik dalam skala bulanan maupun harian.

**Daging Ayam** menunjukkan pergerakan harga yang relatif moderat. Meskipun terjadi fluktuasi 
kenaikan dan penurunan harga, perubahannya tidak terlalu ekstrem. Hal ini disebabkan oleh 
siklus produksi yang relatif cepat serta kemampuan pasokan untuk menyesuaikan dengan permintaan.

**Minyak Goreng** cenderung memiliki harga yang stabil dalam jangka panjang. Namun, pada tahun 
2022 terjadi lonjakan harga yang cukup tajam. Kenaikan tersebut berkaitan dengan dampak pasca 
pandemi COVID-19, gangguan rantai pasok global, serta meningkatnya harga bahan baku.

**Bawang Merah** memiliki pola pergerakan harga yang hampir serupa dengan cabai rawit. Harga 
bawang merah sangat dipengaruhi oleh musim tanam, kondisi cuaca, dan hasil panen. Ketika 
pasokan terganggu, harga cenderung meningkat, dan sebaliknya akan menurun saat produksi melimpah.

**Gula Pasir** menunjukkan tren kenaikan harga yang bersifat gradual dan relatif konsisten dari 
tahun ke tahun. Pola ini mencerminkan tekanan biaya produksi, ketergantungan terhadap impor, 
serta peningkatan permintaan masyarakat.

**Daging Sapi** merupakan komoditas dengan tingkat harga yang tinggi dan relatif sulit mengalami 
penurunan. Pada tahun 2022 terjadi lonjakan harga yang cukup drastis akibat meningkatnya permintaan 
pasca pandemi serta keterbatasan pasokan. Meskipun sempat menurun, harga daging sapi tetap berada 
pada level yang lebih tinggi dibandingkan periode sebelum pandemi.

**Kesimpulan**  
Secara keseluruhan, harga komoditas pangan utama di Provinsi Banten cenderung mengalami peningkatan 
dari tahun ke tahun. Meskipun tingkat fluktuasi berbeda antar komoditas, tren kenaikan ini 
menunjukkan pentingnya kebijakan stabilisasi harga dan penguatan ketahanan pangan daerah guna 
menjaga daya beli masyarakat.
""")


        else:
            st.warning("Silakan pilih setidaknya satu komoditas untuk menampilkan grafik.")
    else:
        st.error("Komoditas yang dicari tidak ditemukan dalam data.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.text("Pastikan file 'data_bengkulu.csv' berada di folder yang sama dengan app.py.")

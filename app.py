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
            st.subheader("Penjelasan Analisis Harga Komoditas")

st.markdown("""
**Beras**  
Selama periode 2019 hingga 2022, harga beras di Provinsi Banten relatif stabil dan berada pada 
kisaran yang aman. Namun, memasuki tahun 2023 hingga 2024 terlihat adanya tren kenaikan harga 
yang cukup konsisten. Kondisi ini mengindikasikan meningkatnya tekanan inflasi serta kemungkinan 
adanya gangguan pada sisi produksi dan distribusi, sehingga harga beras menjadi lebih mahal 
dibandingkan tahun-tahun sebelumnya.

**Cabai Rawit**  
Cabai rawit merupakan komoditas dengan tingkat volatilitas harga yang paling tinggi. Pergerakan 
harga cabai rawit sangat dipengaruhi oleh faktor cuaca, musim tanam, dan masa panen. Akibatnya, 
harga cabai rawit dapat mengalami kenaikan maupun penurunan yang tajam dalam waktu yang relatif 
singkat, bahkan dalam hitungan minggu atau hari.

**Daging Ayam**  
Harga daging ayam cenderung menunjukkan kondisi yang relatif stabil sepanjang periode pengamatan. 
Meskipun terjadi fluktuasi naik dan turun, perubahan harga tersebut tidak terlalu ekstrem. Hal ini 
menunjukkan bahwa pasokan daging ayam relatif mampu menyesuaikan dengan tingkat permintaan pasar.

**Minyak Goreng**  
Secara umum, harga minyak goreng terlihat stabil dari tahun ke tahun. Namun, pada tahun 2022 
terjadi lonjakan harga yang cukup signifikan. Kenaikan ini berkaitan dengan dampak pasca pandemi 
COVID-19, gangguan rantai pasok global, serta meningkatnya harga bahan baku di pasar internasional.

**Bawang Merah**  
Pergerakan harga bawang merah memiliki pola yang hampir serupa dengan cabai rawit. Harga sangat 
dipengaruhi oleh kondisi cuaca, musim tanam, dan hasil panen. Ketika produksi menurun, harga 
cenderung meningkat, sedangkan saat pasokan melimpah, harga kembali menurun.

**Gula Pasir**  
Harga gula pasir menunjukkan kecenderungan meningkat secara perlahan dan relatif konsisten setiap 
tahunnya. Pola ini mencerminkan adanya tekanan biaya produksi, ketergantungan terhadap impor, 
serta peningkatan permintaan masyarakat dari waktu ke waktu.

**Daging Sapi**  
Daging sapi merupakan komoditas dengan tingkat harga yang relatif tinggi dan cenderung sulit 
mengalami penurunan. Pada tahun 2022 terjadi kenaikan harga yang cukup tajam, yang diduga 
disebabkan oleh tingginya permintaan serta keterbatasan pasokan. Meskipun sempat mengalami 
penyesuaian, harga daging sapi tetap berada pada level yang lebih tinggi dibandingkan sebelum 
pandemi.

**Kesimpulan**  
Secara keseluruhan, harga komoditas pangan utama di Provinsi Banten menunjukkan tren kenaikan 
dalam jangka panjang dengan tingkat fluktuasi yang berbeda-beda. Kondisi ini menegaskan pentingnya 
peran pemerintah dalam menjaga stabilitas harga dan memperkuat ketahanan pangan daerah guna 
melindungi daya beli masyarakat.
""")

        else:
            st.warning("Silakan pilih setidaknya satu komoditas untuk menampilkan grafik.")
    else:
        st.error("Komoditas yang dicari tidak ditemukan dalam data.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.text("Pastikan file 'data_bengkulu.csv' berada di folder yang sama dengan app.py.")

import streamlit as st
import pandas as pd
from pathlib import Path

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Dashboard Harga Pangan Banten",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# JUDUL UTAMA
# ======================================================
st.title("📈 Dashboard Harga Komoditas Pangan Utama di Banten")

st.markdown("""
Dashboard ini menggambarkan dinamika harga tujuh komoditas pangan strategis di Provinsi Banten 
selama periode 2019 hingga 2024, yaitu **beras, daging ayam, daging sapi, bawang merah, cabai rawit, 
minyak goreng, dan gula pasir**. Visualisasi data menunjukkan bahwa meskipun setiap komoditas 
memiliki karakteristik pergerakan harga yang berbeda, secara umum terdapat kecenderungan 
kenaikan harga dalam jangka panjang.
""")

# ======================================================
# FOTO DI ATAS NAMA ANGGOTA
# ======================================================
foto_path = Path("foto/foto.jpg")
if foto_path.exists():
    st.image(
        str(foto_path),
        caption="Ilustrasi Komoditas Pangan",
        use_container_width=True
    )
else:
    st.info("📷 Gambar ilustrasi tidak ditemukan. Pastikan file 'foto/foto.jpg' ada.")

# ======================================================
# NAMA ANGGOTA
# ======================================================
st.subheader("👥 Anggota Kelompok")

anggota = [
    "Jibral Yusuf Nazar (021002301001)",
    "David Indra Setiawan (021002305021)",
    "Dimas Wahyu Saputra (021002302003)"
]

col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

for idx, a in enumerate(anggota):
    with columns[idx]:
        st.markdown(f"**{a}**")

st.divider()

# ======================================================
# LOAD DATA CSV
# ======================================================
file_path = "data_bengkulu.csv"

try:
    # Cek apakah file ada
    if not Path(file_path).exists():
        st.error(f"❌ File '{file_path}' tidak ditemukan!")
        st.info("💡 Pastikan file CSV berada di folder yang sama dengan script ini.")
        st.stop()
    
    df = pd.read_csv(file_path)
    
    # Validasi data tidak kosong
    if df.empty:
        st.error("❌ File CSV kosong!")
        st.stop()

    # Membersihkan nama kolom
    df.columns = df.columns.str.strip()

    # Konversi kolom tahun menjadi datetime
    if "tahun" in df.columns:
        df["tahun_date"] = pd.to_datetime(
            df["tahun"].astype(str).str.strip(),
            errors="coerce"
        )
        
        # Hapus baris dengan tahun invalid
        df = df.dropna(subset=["tahun_date"])
        
        # Sort berdasarkan tanggal
        df = df.sort_values("tahun_date")
    else:
        st.error("❌ Kolom 'tahun' tidak ditemukan dalam data!")
        st.stop()

    # ==================================================
    # SIDEBAR FILTER
    # ==================================================
    st.sidebar.header("⚙️ Pengaturan Dashboard")
    
    # Filter tahun
    if not df["tahun_date"].empty:
        min_year = df["tahun_date"].min().year
        max_year = df["tahun_date"].max().year
        
        year_range = st.sidebar.slider(
            "Pilih Rentang Tahun:",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        # Filter dataframe berdasarkan tahun
        df_filtered = df[
            (df["tahun_date"].dt.year >= year_range[0]) & 
            (df["tahun_date"].dt.year <= year_range[1])
        ]
    else:
        df_filtered = df
    
    show_table = st.sidebar.checkbox(
        "📊 Tampilkan Tabel Data",
        value=False
    )

    if show_table:
        st.subheader("📋 Data Lengkap")
        st.dataframe(
            df_filtered.style.format(precision=0, thousands=".", decimal=","),
            use_container_width=True,
            height=400
        )
        st.caption(f"Menampilkan **{len(df_filtered)}** baris data dari total **{len(df)}** baris.")

    # ==================================================
    # BAGIAN ANALISIS GRAFIK
    # ==================================================
    st.divider()
    st.header("📊 Analisis Harga Pangan Tahun 2019–2024 di Provinsi Banten")
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

    # Cari komoditas yang ada di data
    komoditas_plot = [
        col for col in target_komoditas
        if col in df_filtered.columns
    ]

    if not komoditas_plot:
        st.error("❌ Tidak ada komoditas yang ditemukan dalam data!")
        st.info(f"Kolom yang tersedia: {', '.join(df_filtered.columns.tolist())}")
        st.stop()

    # Multiselect dengan semua komoditas terpilih secara default
    selected_commodities = st.multiselect(
        "🔍 Pilih Komoditas untuk Ditampilkan:",
        options=komoditas_plot,
        default=komoditas_plot,
        help="Pilih satu atau lebih komoditas untuk membandingkan harganya"
    )

    if selected_commodities:
        # Buat chart data
        chart_data = df_filtered.set_index("tahun_date")[selected_commodities]
        
        # Hapus nilai NaN
        chart_data = chart_data.dropna(how='all')

        # Tampilkan grafik
        st.subheader("📈 Dinamika Harga Komoditas Pangan")
        st.line_chart(chart_data, height=500)

        # Tampilkan statistik ringkas
        st.subheader("📊 Statistik Harga (Periode Terpilih)")
        
        stats_data = []
        for commodity in selected_commodities:
            data = df_filtered[commodity].dropna()
            if not data.empty:
                stats_data.append({
                    "Komoditas": commodity,
                    "Harga Rata-rata": f"Rp {data.mean():,.0f}",
                    "Harga Tertinggi": f"Rp {data.max():,.0f}",
                    "Harga Terendah": f"Rp {data.min():,.0f}",
                    "Perubahan (%)": f"{((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100):.1f}%"
                })
        
        if stats_data:
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)

        # ==================================================
        # PENJELASAN ANALISIS
        # ==================================================
        st.divider()
        st.markdown("""
### 📊 Analisis Perkembangan Harga Komoditas Pangan Utama di Provinsi Banten (2019–2024)

#### 🌾 Beras
Menunjukkan kondisi harga yang relatif stabil pada periode 2019 hingga 2022. 
Stabilitas ini mencerminkan peran pemerintah dalam menjaga ketersediaan stok dan stabilisasi 
harga. Namun, pada periode 2023 hingga 2024 terlihat tren kenaikan harga yang cukup signifikan, 
yang mengindikasikan adanya tekanan inflasi, peningkatan biaya produksi, serta gangguan iklim 
yang memengaruhi hasil panen.

#### 🌶️ Cabai Rawit
Merupakan komoditas dengan tingkat volatilitas harga yang tinggi. Fluktuasi 
harga yang tajam dari waktu ke waktu dipengaruhi oleh faktor cuaca, musim panen, serta 
keterbatasan pasokan. Kondisi ini menyebabkan harga cabai rawit dapat berubah secara cepat, 
baik dalam skala bulanan maupun harian.

#### 🍗 Daging Ayam
Menunjukkan pergerakan harga yang relatif moderat. Meskipun terjadi fluktuasi 
kenaikan dan penurunan harga, perubahannya tidak terlalu ekstrem. Hal ini disebabkan oleh 
siklus produksi yang relatif cepat serta kemampuan pasokan untuk menyesuaikan dengan permintaan.

#### 🛢️ Minyak Goreng
Cenderung memiliki harga yang stabil dalam jangka panjang. Namun, pada tahun 
2022 terjadi lonjakan harga yang cukup tajam. Kenaikan tersebut berkaitan dengan dampak pasca 
pandemi COVID-19, gangguan rantai pasok global, serta meningkatnya harga bahan baku.

#### 🧅 Bawang Merah
Memiliki pola pergerakan harga yang hampir serupa dengan cabai rawit. Harga 
bawang merah sangat dipengaruhi oleh musim tanam, kondisi cuaca, dan hasil panen. Ketika 
pasokan terganggu, harga cenderung meningkat, dan sebaliknya akan menurun saat produksi melimpah.

#### 🍚 Gula Pasir
Menunjukkan tren kenaikan harga yang bersifat gradual dan relatif konsisten dari 
tahun ke tahun. Pola ini mencerminkan tekanan biaya produksi, ketergantungan terhadap impor, 
serta peningkatan permintaan masyarakat.

#### 🥩 Daging Sapi
Merupakan komoditas dengan tingkat harga yang tinggi dan relatif sulit mengalami 
penurunan. Pada tahun 2022 terjadi lonjakan harga yang cukup drastis akibat meningkatnya permintaan 
pasca pandemi serta keterbatasan pasokan. Meskipun sempat menurun, harga daging sapi tetap berada 
pada level yang lebih tinggi dibandingkan periode sebelum pandemi.

---

### 🎯 Kesimpulan
Secara keseluruhan, harga komoditas pangan utama di Provinsi Banten cenderung mengalami peningkatan 
dari tahun ke tahun. Meskipun tingkat fluktuasi berbeda antar komoditas, tren kenaikan ini 
menunjukkan pentingnya kebijakan stabilisasi harga dan penguatan ketahanan pangan daerah guna 
menjaga daya beli masyarakat.
""")

    else:
        st.warning("⚠️ Silakan pilih setidaknya satu komoditas untuk menampilkan grafik.")

except FileNotFoundError:
    st.error(f"❌ File '{file_path}' tidak ditemukan!")
    st.info("💡 Pastikan file 'data_bengkulu.csv' berada di folder yang sama dengan script ini.")
except pd.errors.EmptyDataError:
    st.error("❌ File CSV kosong atau tidak valid!")
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat memuat data:")
    st.exception(e)
    st.info("💡 Periksa format data CSV Anda dan pastikan kolom yang diperlukan tersedia.")

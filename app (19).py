
import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Harga Pangan Banten", layout="wide")

# Judul Utama
st.title(' Dashboard Harga Komoditas Pangan Utama di Banten')
st.markdown("""
Dashboard ini menyajikan analisis perkembangan harga pangan strategis di wilayah Banten.
Data ini diambil dari laporan bulanan dan divisualisasikan untuk membantu memantau tren kenaikan atau penurunan harga.
""")

# Load data CSV (Bukan Excel lagi)
file_path = 'data_bengkulu.csv'

try:
    # Membaca CSV (Tidak butuh openpyxl)
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Process 'tahun' column
    # Pastikan format tanggal sesuai. CSV kadang mengubah format string, jadi kita parse ulang dengan hati-hati
    df['tahun_date'] = pd.to_datetime(df['tahun'].astype(str).str.replace(' ', ''), format='%m/%Y', errors='coerce')

    # Sidebar untuk filter
    st.sidebar.header("Filter Tampilan")
    show_table = st.sidebar.checkbox("Tampilkan Tabel Data", value=True)

    if show_table:
        st.subheader(" Data Lengkap")
        st.dataframe(df)
        st.caption(f"Menampilkan total {len(df)} baris data.")

    # Plotting Section
    st.divider()
    st.header(" Analisis Harga pangan dari tahun 2019- 2024 di wilayah banten")
    st.markdown("Grafik ini menunjukkan pergerakan harga komoditas pangan dari waktu ke waktu.")

    target_komoditas = ['Beras', 'Daging Ayam', 'Daging Sapi', 'Bawang Merah',
                        'Cabai Rawit', 'Minyak Goreng', 'Gula Pasir']

    # Filter columns that exist in the dataframe
    komoditas_plot = [col for col in target_komoditas if col in df.columns]

    if komoditas_plot:
        selected_commodities = st.multiselect(
            "Pilih Komoditas untuk Ditampilkan:",
            options=komoditas_plot,
            default=komoditas_plot
        )

        if selected_commodities:
            # Native Streamlit Chart
            chart_data = df.set_index('tahun_date')[selected_commodities]
            
            st.subheader("Dinamika Harga Komoditas Pangan")
            st.line_chart(chart_data)

            st.info("""
            ** penjelasan:**
            *   **Beras**: dari tahun 2019 samapai 2022 harganya stabil dan aman aman aja tapi ketika memasuki  tahun 2023 sampai 2024 harganya naik bisa di liaht dari garisnya yang naik tandanya harga udah makin mahal entah kenapa dah  .
            *   **Cabai Rawit**: Sering mengalami volatilitas tinggi, biasanya dipengaruhi oleh faktor cuaca dan musim panen karena itu harganya bisa mahal murah dan kadang bisa naik dalam waktu seminggu hingga bulan bahkan hari tergantung cuaca aja .
            *   **Daging Ayam**: garisnya tetep di tengah kadang naik kadang turun tapi masih bisa di bilang cukup stabil.
            *   **Minyak Goreng**:harganya cenderung setabil di dari tahun ke tahun tapi ada garis yang naiik di tahun 2022 penyebabnya paska covid 19.
            *   **bawang merah**: sama kayak cabe kadang harga naik dan kadang turun tergantung cuaca dan musim aja
            *   **gula pasir **: hampir sama seperti beras yang naik dikit dikit setiap tahun
            *   ** daging sapi**: dari grafik dan harganya yang tinggi daging sapi jadi komonditas yang sulit turun mungkin karena permintaan yang makin tinggi dan di 2022 pasca covid harganya naik dersatis dan turun di tahun selanjutnya tapi tetep naik
            *   ** kesimpulan**: dari hasil pengamatan data di atas harga komonditas di indonesia makin tahun makin naik walaupun sedikit demi sedikit.            """)
        else:
            st.warning("Silakan pilih setidaknya satu komoditas untuk menampilkan grafik.")

    else:
        st.error("Komoditas yang dicari tidak ditemukan dalam data.")

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.text("Pastikan file 'data_bengkulu.csv' berada di folder yang sama dengan app.py di GitHub.")

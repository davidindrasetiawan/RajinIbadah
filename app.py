import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Dashboard Harga Pangan Banten",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

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
    
    # Tab mode di sidebar
    analysis_mode = st.sidebar.radio(
        "🎯 Mode Analisis:",
        ["Overview", "Perbandingan Detail", "Analisis Volatilitas", "Prediksi Trend"]
    )
    
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
    
    st.sidebar.divider()
    st.sidebar.markdown("### 📥 Export Data")
    
    # Download button untuk filtered data
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="⬇️ Download Data (CSV)",
        data=csv,
        file_name=f'data_pangan_{year_range[0]}_{year_range[1]}.csv',
        mime='text/csv',
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
    # DEFINISI KOMODITAS
    # ==================================================
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

    # ==================================================
    # MODE 1: OVERVIEW
    # ==================================================
    if analysis_mode == "Overview":
        st.header("📊 Overview Harga Pangan")
        
        # Metrics Cards
        st.subheader("📈 Ringkasan Perubahan Harga")
        
        cols = st.columns(len(komoditas_plot))
        for idx, commodity in enumerate(komoditas_plot):
            data = df_filtered[commodity].dropna()
            if len(data) >= 2:
                first_price = data.iloc[0]
                last_price = data.iloc[-1]
                change = ((last_price - first_price) / first_price) * 100
                
                with cols[idx]:
                    st.metric(
                        label=commodity,
                        value=f"Rp {last_price:,.0f}",
                        delta=f"{change:+.1f}%"
                    )
        
        st.divider()
        
        # Multi-select untuk grafik
        selected_commodities = st.multiselect(
            "🔍 Pilih Komoditas untuk Ditampilkan:",
            options=komoditas_plot,
            default=komoditas_plot[:3],
            help="Pilih satu atau lebih komoditas untuk membandingkan harganya"
        )

        if selected_commodities:
            # Grafik Interaktif dengan Plotly
            fig = go.Figure()
            
            for commodity in selected_commodities:
                fig.add_trace(go.Scatter(
                    x=df_filtered["tahun_date"],
                    y=df_filtered[commodity],
                    mode='lines+markers',
                    name=commodity,
                    line=dict(width=2),
                    marker=dict(size=6)
                ))
            
            fig.update_layout(
                title="Dinamika Harga Komoditas Pangan",
                xaxis_title="Tahun",
                yaxis_title="Harga (Rp)",
                hovermode='x unified',
                height=500,
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistik Ringkas
            st.subheader("📊 Statistik Harga (Periode Terpilih)")
            
            stats_data = []
            for commodity in selected_commodities:
                data = df_filtered[commodity].dropna()
                if not data.empty:
                    stats_data.append({
                        "Komoditas": commodity,
                        "Rata-rata": f"Rp {data.mean():,.0f}",
                        "Tertinggi": f"Rp {data.max():,.0f}",
                        "Terendah": f"Rp {data.min():,.0f}",
                        "Perubahan": f"{((data.iloc[-1] - data.iloc[0]) / data.iloc[0] * 100):.1f}%",
                        "Std Dev": f"Rp {data.std():,.0f}"
                    })
            
            if stats_data:
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df, use_container_width=True, hide_index=True)

    # ==================================================
    # MODE 2: PERBANDINGAN DETAIL
    # ==================================================
    elif analysis_mode == "Perbandingan Detail":
        st.header("🔄 Perbandingan Detail Komoditas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            commodity1 = st.selectbox(
                "Pilih Komoditas 1:",
                options=komoditas_plot,
                index=0
            )
        
        with col2:
            commodity2 = st.selectbox(
                "Pilih Komoditas 2:",
                options=komoditas_plot,
                index=min(1, len(komoditas_plot)-1)
            )
        
        # Grafik Perbandingan Side by Side
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader(f"📊 {commodity1}")
            data1 = df_filtered[["tahun_date", commodity1]].dropna()
            
            fig1 = px.area(
                data1,
                x="tahun_date",
                y=commodity1,
                title=f"Trend Harga {commodity1}",
                labels={"tahun_date": "Tahun", commodity1: "Harga (Rp)"}
            )
            st.plotly_chart(fig1, use_container_width=True)
            
            # Stats commodity 1
            if not data1.empty:
                avg1 = data1[commodity1].mean()
                max1 = data1[commodity1].max()
                min1 = data1[commodity1].min()
                
                st.metric("Rata-rata", f"Rp {avg1:,.0f}")
                st.metric("Tertinggi", f"Rp {max1:,.0f}")
                st.metric("Terendah", f"Rp {min1:,.0f}")
        
        with col_b:
            st.subheader(f"📊 {commodity2}")
            data2 = df_filtered[["tahun_date", commodity2]].dropna()
            
            fig2 = px.area(
                data2,
                x="tahun_date",
                y=commodity2,
                title=f"Trend Harga {commodity2}",
                labels={"tahun_date": "Tahun", commodity2: "Harga (Rp)"}
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Stats commodity 2
            if not data2.empty:
                avg2 = data2[commodity2].mean()
                max2 = data2[commodity2].max()
                min2 = data2[commodity2].min()
                
                st.metric("Rata-rata", f"Rp {avg2:,.0f}")
                st.metric("Tertinggi", f"Rp {max2:,.0f}")
                st.metric("Terendah", f"Rp {min2:,.0f}")
        
        # Korelasi
        st.divider()
        st.subheader("🔗 Analisis Korelasi")
        
        if not data1.empty and not data2.empty:
            # Merge data untuk korelasi
            merged = pd.merge(data1, data2, on="tahun_date")
            
            if len(merged) > 1:
                correlation = merged[commodity1].corr(merged[commodity2])
                
                col_x, col_y, col_z = st.columns(3)
                with col_y:
                    st.metric(
                        "Korelasi Harga",
                        f"{correlation:.3f}",
                        help="Nilai mendekati 1: korelasi positif kuat, -1: korelasi negatif kuat, 0: tidak ada korelasi"
                    )
                
                # Scatter plot
                fig_scatter = px.scatter(
                    merged,
                    x=commodity1,
                    y=commodity2,
                    trendline="ols",
                    title=f"Hubungan Harga {commodity1} vs {commodity2}",
                    labels={commodity1: f"Harga {commodity1}", commodity2: f"Harga {commodity2}"}
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

    # ==================================================
    # MODE 3: ANALISIS VOLATILITAS
    # ==================================================
    elif analysis_mode == "Analisis Volatilitas":
        st.header("📉 Analisis Volatilitas Harga")
        
        st.markdown("""
        Volatilitas mengukur seberapa besar fluktuasi harga suatu komoditas. 
        Volatilitas tinggi menunjukkan harga yang tidak stabil.
        """)
        
        # Hitung volatilitas (standar deviasi)
        volatility_data = []
        
        for commodity in komoditas_plot:
            data = df_filtered[commodity].dropna()
            if len(data) > 1:
                volatility = data.std()
                mean_price = data.mean()
                cv = (volatility / mean_price) * 100  # Coefficient of Variation
                
                volatility_data.append({
                    "Komoditas": commodity,
                    "Volatilitas (Std Dev)": volatility,
                    "Harga Rata-rata": mean_price,
                    "Koefisien Variasi (%)": cv
                })
        
        vol_df = pd.DataFrame(volatility_data)
        vol_df = vol_df.sort_values("Koefisien Variasi (%)", ascending=False)
        
        # Bar chart volatilitas
        fig_vol = px.bar(
            vol_df,
            x="Komoditas",
            y="Koefisien Variasi (%)",
            title="Tingkat Volatilitas Komoditas (Koefisien Variasi)",
            color="Koefisien Variasi (%)",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_vol, use_container_width=True)
        
        # Tabel volatilitas
        st.subheader("📊 Detail Volatilitas")
        
        display_vol = vol_df.copy()
        display_vol["Volatilitas (Std Dev)"] = display_vol["Volatilitas (Std Dev)"].apply(lambda x: f"Rp {x:,.0f}")
        display_vol["Harga Rata-rata"] = display_vol["Harga Rata-rata"].apply(lambda x: f"Rp {x:,.0f}")
        display_vol["Koefisien Variasi (%)"] = display_vol["Koefisien Variasi (%)"].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(display_vol, use_container_width=True, hide_index=True)
        
        # Interpretasi
        st.info("""
        **💡 Interpretasi:**
        - **Koefisien Variasi < 15%**: Volatilitas Rendah (Harga Stabil)
        - **Koefisien Variasi 15-30%**: Volatilitas Sedang
        - **Koefisien Variasi > 30%**: Volatilitas Tinggi (Harga Tidak Stabil)
        """)
        
        # Grafik pergerakan harian/perubahan
        st.divider()
        st.subheader("📈 Perubahan Harga dari Waktu ke Waktu")
        
        commodity_vol = st.selectbox(
            "Pilih komoditas untuk melihat perubahan harga:",
            options=komoditas_plot
        )
        
        data_vol = df_filtered[["tahun_date", commodity_vol]].dropna()
        data_vol["Perubahan (%)"] = data_vol[commodity_vol].pct_change() * 100
        
        fig_change = go.Figure()
        
        fig_change.add_trace(go.Bar(
            x=data_vol["tahun_date"],
            y=data_vol["Perubahan (%)"],
            name="Perubahan Harga",
            marker_color=np.where(data_vol["Perubahan (%)"] >= 0, 'green', 'red')
        ))
        
        fig_change.update_layout(
            title=f"Persentase Perubahan Harga {commodity_vol}",
            xaxis_title="Tahun",
            yaxis_title="Perubahan (%)",
            height=400
        )
        
        st.plotly_chart(fig_change, use_container_width=True)

    # ==================================================
    # MODE 4: PREDIKSI TREND
    # ==================================================
    elif analysis_mode == "Prediksi Trend":
        st.header("🔮 Analisis dan Prediksi Trend")
        
        st.warning("⚠️ Prediksi ini menggunakan metode sederhana (moving average) dan hanya untuk ilustrasi. Bukan rekomendasi investasi.")
        
        commodity_pred = st.selectbox(
            "Pilih komoditas untuk analisis trend:",
            options=komoditas_plot
        )
        
        data_pred = df_filtered[["tahun_date", commodity_pred]].dropna()
        
        if len(data_pred) >= 3:
            # Hitung moving averages
            data_pred["MA_3"] = data_pred[commodity_pred].rolling(window=3).mean()
            data_pred["MA_6"] = data_pred[commodity_pred].rolling(window=min(6, len(data_pred))).mean()
            
            # Grafik dengan moving averages
            fig_pred = go.Figure()
            
            fig_pred.add_trace(go.Scatter(
                x=data_pred["tahun_date"],
                y=data_pred[commodity_pred],
                mode='lines+markers',
                name='Harga Aktual',
                line=dict(color='blue', width=2)
            ))
            
            fig_pred.add_trace(go.Scatter(
                x=data_pred["tahun_date"],
                y=data_pred["MA_3"],
                mode='lines',
                name='Moving Average 3',
                line=dict(color='orange', width=2, dash='dash')
            ))
            
            fig_pred.add_trace(go.Scatter(
                x=data_pred["tahun_date"],
                y=data_pred["MA_6"],
                mode='lines',
                name='Moving Average 6',
                line=dict(color='red', width=2, dash='dot')
            ))
            
            fig_pred.update_layout(
                title=f"Trend Harga {commodity_pred} dengan Moving Average",
                xaxis_title="Tahun",
                yaxis_title="Harga (Rp)",
                height=500,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_pred, use_container_width=True)
            
            # Analisis trend
            st.subheader("📊 Analisis Trend")
            
            col1, col2, col3 = st.columns(3)
            
            # Trend direction
            recent_data = data_pred[commodity_pred].tail(6)
            if len(recent_data) >= 2:
                trend_direction = "Naik" if recent_data.iloc[-1] > recent_data.iloc[0] else "Turun"
                trend_pct = ((recent_data.iloc[-1] - recent_data.iloc[0]) / recent_data.iloc[0]) * 100
                
                with col1:
                    st.metric(
                        "Trend 6 Periode Terakhir",
                        trend_direction,
                        f"{trend_pct:+.1f}%"
                    )
                
                with col2:
                    current_price = data_pred[commodity_pred].iloc[-1]
                    ma3_current = data_pred["MA_3"].iloc[-1]
                    
                    signal = "Bullish" if current_price > ma3_current else "Bearish"
                    st.metric("Sinyal Pasar", signal)
                
                with col3:
                    volatility = recent_data.std()
                    st.metric("Volatilitas 6 Periode", f"Rp {volatility:,.0f}")
            
            # Insight otomatis
            st.divider()
            st.subheader("💡 Insight Otomatis")
            
            avg_price = data_pred[commodity_pred].mean()
            current_price = data_pred[commodity_pred].iloc[-1]
            
            if current_price > avg_price * 1.1:
                st.error(f"🔴 Harga {commodity_pred} saat ini **{((current_price/avg_price - 1) * 100):.1f}% lebih tinggi** dari rata-rata historis. Harga sedang tinggi.")
            elif current_price < avg_price * 0.9:
                st.success(f"🟢 Harga {commodity_pred} saat ini **{((1 - current_price/avg_price) * 100):.1f}% lebih rendah** dari rata-rata historis. Harga sedang rendah.")
            else:
                st.info(f"🟡 Harga {commodity_pred} saat ini berada pada level **normal** sekitar rata-rata historis.")

    # ==================================================
    # PENJELASAN ANALISIS (Di bawah semua mode)
    # ==================================================
    st.divider()
    with st.expander("📖 Lihat Analisis Lengkap Perkembangan Harga", expanded=False):
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

except FileNotFoundError:
    st.error(f"❌ File '{file_path}' tidak ditemukan!")
    st.info("💡 Pastikan file 'data_bengkulu.csv' berada di folder yang sama dengan script ini.")
except pd.errors.EmptyDataError:
    st.error("❌ File CSV kosong atau tidak valid!")
except Exception as e:
    st.error(f"❌ Terjadi kesalahan saat memuat data:")
    st.exception(e)
    st.info("💡 Periksa format data CSV Anda dan pastikan kolom yang diperlukan tersedia.")

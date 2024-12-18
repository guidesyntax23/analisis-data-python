import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat data dari day_data.csv
day_data = pd.read_csv('data/day.csv')
hour_data = pd.read_csv('data/hour.csv')

# Mengubah kolom 'dteday' menjadi datetime
day_data['dteday'] = pd.to_datetime(day_data['dteday'])

# Mapping season ke kategori yang lebih mudah dipahami
season_map = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
day_data['season'] = day_data['season'].map(season_map)

# Mapping weather conditions ke kategori yang lebih mudah dipahami
weather_map = {1: 'Cuaca Cerah', 2: 'Cuaca Berawan', 3: 'Cuaca Buruk'}
day_data['weathersit'] = day_data['weathersit'].map(weather_map)

# Menambahkan kolom 'month' untuk analisis bulanan
day_data['month'] = day_data['dteday'].dt.month

# Title of the dashboard
st.title('Dashboard Peminjaman Sepeda')

# Filter berdasarkan rentang tanggal
st.subheader('Filter Berdasarkan Tanggal')

# Meminta pengguna untuk memilih tanggal mulai dan tanggal selesai
start_date = st.date_input("Pilih Tanggal Mulai", min_value=day_data['dteday'].min(), max_value=day_data['dteday'].max(), value=day_data['dteday'].min())
end_date = st.date_input("Pilih Tanggal Selesai", min_value=day_data['dteday'].min(), max_value=day_data['dteday'].max(), value=day_data['dteday'].max())

# Cek apakah tanggal selesai lebih besar dari tanggal mulai
if end_date < start_date:
    st.warning("Tanggal selesai tidak boleh lebih kecil dari tanggal mulai. Silakan pilih tanggal yang valid.")

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = day_data[(day_data['dteday'] >= pd.to_datetime(start_date)) & (day_data['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan data yang sudah difilter
st.write(filtered_data)

# Filter berdasarkan musim menggunakan multiselect untuk memungkinkan pilihan lebih dari satu musim
seasons = st.multiselect(
    'Pilih Musim',
    options=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'],
    default=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'], 
    help="Pilih musim-musim yang ingin ditampilkan."
)
# Filter berdasarkan cuaca menggunakan multiselect untuk memungkinkan pilihan lebih dari satu cuaca
weather_conditions = st.multiselect(
    'Pilih Cuaca',
    options=['Cuaca Cerah', 'Cuaca Berawan', 'Cuaca Buruk'],
    default=['Cuaca Cerah', 'Cuaca Berawan', 'Cuaca Buruk'],
    help="Pilih kondisi cuaca yang ingin ditampilkan."
)

# Filter data berdasarkan musim yang dipilih
filtered_by_season = filtered_data[filtered_data['season'].isin(seasons)]
# Filter data berdasarkan cuaca yang dipilih
filtered_by_weather = filtered_by_season[filtered_by_season['weathersit'].isin(weather_conditions)]

# Menambahkan kolom 'hour' dari 'dteday' untuk jam
filtered_by_weather['hour'] = filtered_by_weather['dteday'].dt.hour  # Ekstrak jam dari kolom 'dteday'

# Menampilkan perbedaan data berdasarkan filter musim dan cuaca
st.write(f"Data yang sesuai dengan musim: {', '.join(seasons)} dan cuaca: {', '.join(weather_conditions)}")

# Visualisasi Jumlah Peminjaman Sepeda per Bulan dengan pemisahan berdasarkan musim dan cuaca
st.subheader('Jumlah Peminjaman Sepeda per Bulan')
if not filtered_by_weather.empty:
    # Mengelompokkan berdasarkan bulan, musim, dan cuaca
    monthly_data = filtered_by_weather.groupby([filtered_by_weather['dteday'].dt.to_period('M'), 'season', 'weathersit'])['cnt'].sum().reset_index()
    monthly_data.columns = ['Month', 'Season', 'Weather', 'Total Peminjaman']
    
    # Mengubah 'Month' menjadi string agar seaborn bisa memprosesnya dengan baik
    monthly_data['Month'] = monthly_data['Month'].astype(str)

    # Membuat grafik dengan warna berdasarkan musim dan cuaca
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=monthly_data, x='Month', y='Total Peminjaman', hue='Season', style='Weather', markers=True, ax=ax)
    ax.set_title('Jumlah Peminjaman Sepeda per Bulan Berdasarkan Musim dan Cuaca')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Peminjaman Sepeda')
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")


# Visualisasi Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman dengan pemisahan berdasarkan cuaca
st.subheader('Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman Sepeda')
if not filtered_by_weather.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_by_weather, x='temp', y='hum', hue='weathersit', style='season', size='cnt', ax=ax, palette='Set1')
    ax.set_title('Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Kelembaban (%)')
    st.pyplot(fig)
else:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")

# Visualisasi Jumlah Peminjaman per Jam Berdasarkan Hari Libur
st.subheader('Jumlah Peminjaman per Jam Berdasarkan Hari Libur')

# Mengelompokkan data dari hour_data berdasarkan jam dan hari libur
hourly_data_holiday = hour_data.groupby(['hr', 'holiday']).agg({'cnt': 'sum'}).reset_index()

# Memisahkan data untuk hari kerja dan hari libur
data_working_day = hourly_data_holiday[hourly_data_holiday['holiday'] == 0]
data_holiday = hourly_data_holiday[hourly_data_holiday['holiday'] == 1]

# Cek apakah ada data untuk hari kerja dan hari libur
if data_working_day.empty and data_holiday.empty:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih untuk jumlah peminjaman per jam berdasarkan hari libur.")
else:
    # Plotting
    fig2, ax2 = plt.subplots(figsize=(10, 6))

    # Menggunakan log scale untuk sumbu Y untuk perbedaan besar
    ax2.set_yscale('log')

    # Plot untuk hari kerja dan hari libur terpisah
    sns.lineplot(data=data_working_day, x='hr', y='cnt', label='Hari Kerja', ax=ax2)
    sns.lineplot(data=data_holiday, x='hr', y='cnt', label='Hari Libur', ax=ax2)

    ax2.set_title('Jumlah Peminjaman per Jam Berdasarkan Hari Libur')
    ax2.set_xlabel('Jam')
    ax2.set_ylabel('Jumlah Peminjaman Sepeda (Log Scale)')
    ax2.legend(title='Hari', loc='upper left')

    st.pyplot(fig2)

# Jumlah Peminjaman Sepeda per Jam Berdasarkan Cuaca
st.subheader('Jumlah Peminjaman Sepeda per Jam Berdasarkan Cuaca')

# Mengelompokkan data dari hour_data berdasarkan jam dan kondisi cuaca
hourly_weather_data = hour_data.groupby(['hr', 'weathersit']).agg({'cnt': 'sum'}).reset_index()

# Cek apakah ada data untuk kondisi cuaca
if hourly_weather_data.empty:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih untuk jumlah peminjaman per jam berdasarkan cuaca.")
else:
    # Plotting grafik untuk visualisasi kedua
    fig3, ax3 = plt.subplots(figsize=(10, 6))

    # Plot dengan menggunakan seaborn
    sns.lineplot(data=hourly_weather_data, x='hr', y='cnt', hue='weathersit', ax=ax3)

    ax3.set_title('Jumlah Peminjaman Sepeda per Jam Berdasarkan Cuaca')
    ax3.set_xlabel('Jam')
    ax3.set_ylabel('Jumlah Peminjaman Sepeda')

    # Mengubah keterangan legend menjadi deskriptif
    weather_labels = {
        1: 'Cuaca Cerah',
        2: 'Cuaca Berawan',
        3: 'Cuaca Buruk',
        # Tambahkan label untuk nilai lain jika ada
        4: 'Cuaca Sangat Buruk'  # Misalnya, jika ada kondisi cuaca lain
    }

    # Mendapatkan handles dan labels dari legend
    handles, labels = ax3.get_legend_handles_labels()
    
    # Mengganti label dengan yang deskriptif
    new_labels = []
    for label in labels:
        try:
            new_labels.append(weather_labels[int(label)])
        except KeyError:
            new_labels.append(f'Unknown ({label})')  # Menangani label yang tidak dikenal

    ax3.legend(handles, new_labels, title='Kondisi Cuaca')

    st.pyplot(fig3)

# RFM Analysis
st.subheader('RFM Analysis')

# Recency: calculate days since last rental
if not filtered_by_weather.empty:
    last_date = filtered_by_weather['dteday'].max()
    filtered_by_weather['Recency'] = (last_date - filtered_by_weather['dteday']).dt.days

    # Frequency: total rentals per day
    filtered_by_weather['Frequency'] = filtered_by_weather['cnt']

    # Monetary: using 'cnt' as monetary
    filtered_by_weather['Monetary'] = filtered_by_weather['cnt']

    # Displaying RFM distributions
    fig3, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Recency
    axes[0].hist(filtered_by_weather['Recency'], bins=30, color='skyblue')
    axes[0].set_title('Distribusi Recency')

    # Frequency
    axes[1].hist(filtered_by_weather['Frequency'], bins=30, color='orange')
    axes[1].set_title('Distribusi Frequency')

    # Monetary
    axes[2].hist(filtered_by_weather['Monetary'], bins=30, color='green')
    axes[2].set_title('Distribusi Monetary')

    st.pyplot(fig3)

    # Adding RFM scores
    filtered_by_weather['Recency_Score'] = pd.qcut(filtered_by_weather['Recency'], 3, labels=['High', 'Medium', 'Low'])
    filtered_by_weather['Frequency_Score'] = pd.qcut(filtered_by_weather['Frequency'], 3, labels=['Low', 'Medium', 'High'])
    filtered_by_weather['Monetary_Score'] = pd.qcut(filtered_by_weather['Monetary'], 3, labels=['Low', 'Medium', 'High'])

    # Display RFM Scores
    st.write(filtered_by_weather[['dteday', 'Recency', 'Frequency', 'Monetary', 'Recency_Score', 'Frequency_Score', 'Monetary_Score']].head())
else:
    st.warning("Tidak ada data yang cocok dengan filter yang dipilih untuk analisis RFM.")
    
# Conclusion and Recommendations
st.subheader('Conclusion and Recommendations')

st.write("""
### Insight 1: Pengaruh Suhu dan Kelembaban
- Suhu yang lebih tinggi cenderung meningkatkan peminjaman sepeda, sementara kelembaban tinggi mengurangi peminjaman.

### Insight 2: Pengaruh Hari Libur dan Cuaca
- Hari libur meningkatkan peminjaman sepeda, dengan puncaknya pada jam tertentu.

### RFM Analysis Insights:
- Pengguna dengan **Recency tinggi** lebih aktif dan berpotensi lebih mudah dijadikan target promosi.
- Pengguna dengan **Frequency tinggi** adalah pelanggan setia yang dapat diberikan program loyalitas.
- Pengguna dengan **Monetary tinggi** berkontribusi besar pada pendapatan dan dapat diberi penawaran eksklusif.

### Rekomendasi:
- **Recency**: Targetkan pengguna dengan Recency rendah untuk meningkatkan retensi.
- **Frequency**: Berikan program loyalitas untuk pengguna dengan Frequency tinggi.
- **Monetary**: Berikan promosi untuk pengguna dengan Monetary rendah untuk meningkatkan peminjaman.
""")

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat data dari main_data.csv
main_data = pd.read_csv('dashboard/main_data.csv')

# Mengubah kolom 'dteday' menjadi datetime
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

# Menambahkan kolom 'month' untuk analisis bulanan
main_data['month'] = main_data['dteday'].dt.month

# Title of the dashboard
st.title('Dashboard Peminjaman Sepeda')

# Filter berdasarkan rentang tanggal
st.subheader('Filter Berdasarkan Tanggal')
start_date = st.date_input("Pilih Tanggal Mulai", min_value=main_data['dteday'].min(), max_value=main_data['dteday'].max(), value=main_data['dteday'].min())
end_date = st.date_input("Pilih Tanggal Selesai", min_value=main_data['dteday'].min(), max_value=main_data['dteday'].max(), value=main_data['dteday'].max())

filtered_data = main_data[(main_data['dteday'] >= pd.to_datetime(start_date)) & (main_data['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan data yang sudah difilter
st.write(filtered_data)

# Filter berdasarkan musim (season)
season = st.selectbox('Pilih Musim', options=[1, 2, 3, 4], help='Pilih musim: 1=Musim Semi, 2=Musim Panas, 3=Musim Gugur, 4=Musim Dingin')
filtered_by_season = filtered_data[filtered_data['season'] == season]

# Filter berdasarkan cuaca (weathersit)
weather = st.selectbox('Pilih Cuaca', options=[1, 2, 3], help='Pilih cuaca: 1=Cuaca Cerah, 2=Cuaca Berawan, 3=Cuaca Buruk')
filtered_by_weather = filtered_by_season[filtered_by_season['weathersit'] == weather]

# Visualisasi Jumlah Peminjaman Sepeda per Bulan
st.subheader('Jumlah Peminjaman Sepeda per Bulan')
monthly_data = filtered_by_weather.groupby(filtered_by_weather['dteday'].dt.to_period('M'))['cnt'].sum().reset_index()
monthly_data.columns = ['Month', 'Total Peminjaman']
st.line_chart(monthly_data.set_index('Month'))

# Visualisasi Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman
st.subheader('Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_by_weather, x='temp', y='hum', hue='cnt', ax=ax)
ax.set_title('Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman')
ax.set_xlabel('Suhu (°C)')
ax.set_ylabel('Kelembaban (%)')
st.pyplot(fig)

# Visualisasi Jumlah Peminjaman per Jam Berdasarkan Hari Libur
st.subheader('Jumlah Peminjaman per Jam Berdasarkan Hari Libur')

# Menggunakan data dari filtered_by_weather
hourly_data = filtered_by_weather[['dteday', 'hourly_cnt', 'holiday']]  # Mengambil kolom yang relevan
hourly_data['hour'] = hourly_data['dteday'].dt.hour  # Mengambil jam dari dteday
hourly_data = hourly_data.groupby(['hour', 'holiday']).agg({'hourly_cnt': 'sum'}).reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=hourly_data, x='hour', y='hourly_cnt', hue='holiday', ax=ax2)
ax2.set_title('Jumlah Peminjaman per Jam Berdasarkan Hari Libur')
ax2.set_xlabel('Jam')
ax2.set_ylabel('Jumlah Peminjaman Sepeda')
st.pyplot(fig2)

# RFM Analysis
st.subheader('RFM Analysis')

# Recency: calculate days since last rental
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

st.write("RFM Scores (Recency, Frequency, and Monetary)")
st.write(filtered_by_weather[['dteday', 'Recency', 'Frequency', 'Monetary', 'Recency_Score', 'Frequency_Score', 'Monetary_Score']].head())

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
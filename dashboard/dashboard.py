import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat data dari day.csv dan hour.csv
day_data = pd.read_csv('data/day.csv')  # Pastikan path ini sesuai dengan lokasi file Anda
hour_data = pd.read_csv('data/hour.csv')  # Pastikan path ini sesuai dengan lokasi file Anda

# Mengubah kolom 'dteday' di day_data menjadi datetime
day_data['dteday'] = pd.to_datetime(day_data['dteday'])

# Mengubah kolom 'dteday' di hour_data menjadi datetime
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])

# Menambahkan kolom 'date' dan 'hour' ke hour_data
hour_data['date'] = hour_data['dteday'].dt.date
hour_data['hour'] = hour_data['hr']

# Menggabungkan data per jam ke dalam data harian
hourly_grouped = hour_data.groupby(['date']).agg({'cnt': 'sum'}).reset_index()
hourly_grouped.rename(columns={'cnt': 'hourly_cnt'}, inplace=True)

# Mengonversi kolom 'date' menjadi datetime
hourly_grouped['date'] = pd.to_datetime(hourly_grouped['date'])

# Menggabungkan data harian dengan data yang sudah dikelompokkan
main_data = pd.merge(day_data, hourly_grouped, left_on='dteday', right_on='date', how='left')

# Menyimpan data gabungan ke dalam main_data.csv
main_data.to_csv('dashboard/main_data.csv', index=False)

# Title of the dashboard
st.title('Dashboard Peminjaman Sepeda')

# Display data
st.subheader('Data Peminjaman Sepeda')
st.write(main_data)

# Visualisasi Jumlah Peminjaman Sepeda per Bulan
st.subheader('Jumlah Peminjaman Sepeda per Bulan')
monthly_data = main_data.groupby(main_data['dteday'].dt.to_period('M'))['cnt'].sum().reset_index()
monthly_data.columns = ['Month', 'Total Peminjaman']
st.line_chart(monthly_data.set_index('Month'))

# Visualisasi Pengaruh Suhu dan Kelembaban
st.subheader('Pengaruh Suhu dan Kelembaban terhadap Jumlah Peminjaman')
fig, ax = plt.subplots()
sns.scatterplot(data=main_data, x='temp', y='hum', hue='cnt', ax=ax)
ax.set_title('Pengaruh Suhu dan Kelembaban')
st.pyplot(fig)

# Visualisasi Jumlah Peminjaman per Jam Berdasarkan Hari Libur
st.subheader('Jumlah Peminjaman per Jam Berdasarkan Hari Libur')

# Menggunakan data dari main_data
hourly_data = main_data[['dteday', 'hourly_cnt', 'holiday']]  # Mengambil kolom yang relevan
hourly_data['hour'] = hourly_data['dteday'].dt.hour  # Mengambil jam dari dteday
hourly_data = hourly_data.groupby(['hour', 'holiday']).agg({'hourly_cnt': 'sum'}).reset_index()

fig2, ax2 = plt.subplots()
sns.lineplot(data=hourly_data, x='hour', y='hourly_cnt', hue='holiday', ax=ax2)
ax2.set_title('Jumlah Peminjaman per Jam Berdasarkan Hari Libur')
st.pyplot(fig2)
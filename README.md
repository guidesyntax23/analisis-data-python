# Dashboard Peminjaman Sepeda

## Deskripsi
Dashboard ini menyajikan analisis peminjaman sepeda berdasarkan data suhu, kelembaban, dan hari libur. Data yang digunakan berasal dari dataset `day.csv` dan `hour.csv`.

## Cara Menjalankan
1. Pastikan Anda telah menginstal semua dependensi yang diperlukan. Anda dapat menggunakan `pip install -r requirements.txt`.
2. Jalankan aplikasi Streamlit dengan perintah:
`streamlit run dashboard/dashboard.py`

## Dataset
- `day.csv`: Data peminjaman sepeda harian.
- `hour.csv`: Data peminjaman sepeda per jam.

## Insight
- Suhu yang lebih tinggi cenderung meningkatkan jumlah peminjaman sepeda.
- Kelembaban yang tinggi dapat menurunkan jumlah peminjaman.
- Hari libur mempengaruhi jumlah peminjaman sepeda pada jam-jam tertentu.
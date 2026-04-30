# Setup env dengan terminal
```
mkdir proyek_andat 
cd proyek_andat
pipenv install
pipenv shell
pip install -r requirements.txt
```

# Menjalankan streamlit
```
streamlit run Dashboard/Dashboard_BFAD.py
# Hapus "Dashboard/" apabila sudah beraada di luar folder
```
# 📊 E-Commerce Data Analysis Dashboard

## Deskripsi Proyek

Proyek ini merupakan dashboard analisis data e-commerce yang dibangun menggunakan Python dan Streamlit. Dashboard ini bertujuan untuk membantu memahami perilaku pelanggan, performa penjualan, serta tren transaksi berdasarkan berbagai dimensi seperti waktu, kategori produk, dan metode pembayaran.

Data yang digunakan mencakup transaksi e-commerce dari tahun 2016 hingga 2018, yang dianalisis untuk menghasilkan insight bisnis yang relevan dan actionable.

---

## Tujuan

* Mengidentifikasi metode pembayaran yang paling sering digunakan dan paling menghasilkan revenue
* Menentukan kategori produk dengan performa terbaik setiap tahunnya
* Menganalisis segmentasi pelanggan menggunakan metode RFM (Recency, Frequency, Monetary)
* Menyajikan insight dalam bentuk dashboard interaktif

---

## Fitur Utama

### Interactive Filtering

Pengguna dapat memfilter data berdasarkan:

* Tahun
* Bulan
* Kategori Produk
* Metode Pembayaran

---

### Payment Analysis

* Distribusi metode pembayaran (Pie Chart)
* Total revenue per metode pembayaran (Bar Chart)

---

### Top Product Analysis

* Visualisasi Top 3 kategori produk dengan revenue tertinggi setiap tahun

---

### RFM Analysis

Segmentasi pelanggan berdasarkan:

* **Recency** (seberapa baru transaksi terakhir)
* **Frequency** (seberapa sering transaksi)
* **Monetary** (total nilai transaksi)

Segment yang dihasilkan:

* Best Customer
* Loyal Customer
* Big Spender
* Others

---

### Key Performance Indicators (KPI)

* Total Revenue
* Total Orders
* Average Order Value

---

## Teknologi yang Digunakan

* Python
* Pandas
* Matplotlib & Seaborn
* Streamlit

---

## Insight Utama

* Metode pembayaran **credit card** mendominasi baik dari sisi frekuensi maupun revenue
* Kategori **health & beauty** konsisten menjadi penyumbang revenue tertinggi
* Terjadi peningkatan signifikan aktivitas e-commerce dari tahun 2016 ke 2018
* Segmentasi RFM menunjukkan sebagian besar pelanggan berada pada kategori potensial untuk ditingkatkan menjadi loyal customer

---


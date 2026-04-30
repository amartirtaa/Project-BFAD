import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(page_title="Dashboard E-Commerce",
                   page_icon="📊",
                   layout="wide")

# --- Fungsi untuk Memuat Data (dengan caching agar cepat) ---
@st.cache_data
def load_data(path):
    data = pd.read_csv(path)

    # Pastikan kolom tanggal dalam format datetime
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    return data

# --- Memuat Data ---
df = load_data('BFAD_file.csv')


# SIDEBAR FILTER
st.sidebar.header("🔎 Filter Data")

# Filter Tahun
years = sorted(df['year'].unique())
selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options=years,
    default=years
)

# Filter Bulan
months = sorted(df['month'].unique())
selected_month = st.sidebar.multiselect(
    "Pilih Bulan",
    options=months,
    default=months
)

# Filter Kategori
categories = df['product_category_name_english'].dropna().unique()
selected_category = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=categories,
    default=categories
)

# Filter Payment
payments = df['payment_type'].unique()
selected_payment = st.sidebar.multiselect(
    "Pilih Metode Pembayaran",
    options=payments,
    default=payments
)

# APPLY FILTER
df_filtered = df[
    (df['year'].isin(selected_year)) &
    (df['month'].isin(selected_month)) &
    (df['product_category_name_english'].isin(selected_category)) &
    (df['payment_type'].isin(selected_payment))
]

# TITLE
st.title("📊 Dashboard Analisis E-Commerce")
st.markdown("Selamat datang di dashboard interaktif untuk menganalisis data performa penjualan e-commerce dari 2016 hingga 2018.")
st.divider()

total_revenue = df_filtered['payment_value'].sum()
total_orders = df_filtered['order_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders != 0 else 0
unique_customers = df_filtered['customer_id'].nunique()

st.markdown("### 📊 Key Performance Indicators")
st.caption("Ringkasan performa berdasarkan filter yang dipilih")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${total_revenue:,.2f}"
    )

with col2:
    st.metric(
        label="Total Orders",
        value=f"{total_orders:,}"
    )

with col3:
    st.metric(
        label="Average Order Value",
        value=f"${avg_order_value:,.2f}"
    )
st.markdown("---")

# PAYMENT ANALYSIS
st.markdown("### 💳 Metode Pembayaran")

payment_counts = df_filtered['payment_type'].value_counts()
payment_sum = df_filtered.groupby('payment_type')['payment_value'].sum()

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%')
    ax1.set_title('Distribusi Metode Pembayaran')
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    sns.barplot(x=payment_sum.index, y=payment_sum.values, ax=ax2)
    ax2.set_title('Revenue per Metode Pembayaran')
    ax2.set_ylabel('Revenue')
    st.pyplot(fig2)

# TOP 3 PRODUK
st.markdown("### 🛍️ Top 3 Kategori Produk dengan Revenue Tertinggi per Tahun")

revenue_yearly = (
    df_filtered
    .groupby(['year', 'product_category_name_english'])['payment_value']
    .sum()
    .reset_index()
)

top3_per_year = (
    revenue_yearly
    .groupby('year', group_keys=False)
    .apply(lambda x: x.nlargest(3, 'payment_value'))
)

fig3, ax3 = plt.subplots(figsize=(10,6))
sns.barplot(
    data=top3_per_year,
    x='year',
    y='payment_value',
    hue='product_category_name_english',
    ax=ax3
)

ax3.set_title('Top 3 Kategori Produk per Tahun')
st.pyplot(fig3)

# RFM ANALYSIS
st.markdown("### 👥 RFM Analysis")

# --- Validasi data ---
if df_filtered.empty:
    st.warning("Data kosong, silakan ubah filter")
    st.stop()

# HITUNG RFM
snapshot_date = df_filtered['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

rfm = df_filtered.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
    'customer_id': 'count',
    'payment_value': 'sum'
})

rfm.columns = ['Recency', 'Frequency', 'Monetary']
rfm = rfm.reset_index()

# SCORING (AMAN)
rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1], duplicates='drop')
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4], duplicates='drop')
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4], duplicates='drop')

rfm['RFM_score'] = (
    rfm['R_score'].astype(str) +
    rfm['F_score'].astype(str) +
    rfm['M_score'].astype(str)
)

# SEGMENTASI
def segment(row):
    if row['RFM_score'] == '444':
        return 'Best Customer'
    elif int(row['R_score']) >= 3 and int(row['F_score']) >= 3:
        return 'Loyal Customer'
    elif int(row['M_score']) == 4:
        return 'Big Spender'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(segment, axis=1)

# BEST CUSTOMER ANALYSIS
st.markdown("### 👑 Best Customer Based on RFM Parameters")

best_customer = rfm[rfm['Segment'] == 'Best Customer']

if best_customer.empty:
    st.warning("Tidak ada Best Customer pada filter ini")
else:
    # KPI
    avg_recency = best_customer['Recency'].mean()
    avg_frequency = best_customer['Frequency'].mean()
    avg_monetary = best_customer['Monetary'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Recency (days)", f"{avg_recency:.1f}")
    col2.metric("Average Frequency", f"{avg_frequency:.2f}")
    col3.metric("Average Monetary", f"${avg_monetary:,.2f}")

st.subheader("📊 RFM Segment Summary")

# AGGREGATION
rfm_summary = rfm.groupby('Segment').agg({
    'customer_id': 'count',
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'sum']
})

# RENAME KOLOM
rfm_summary.columns = [
    'Total Customer',
    'Avg Recency',
    'Avg Frequency',
    'Avg Monetary',
    'Total Revenue'
]

# HITUNG PERSENTASE CUSTOMER
rfm_summary['Percentage (%)'] = (
    rfm_summary['Total Customer'] /
    rfm_summary['Total Customer'].sum() * 100
)

# ROUNDING BIAR RAPI
rfm_summary = rfm_summary.round({
    'Avg Recency': 2,
    'Avg Frequency': 2,
    'Avg Monetary': 2,
    'Total Revenue': 2,
    'Percentage (%)': 2
})

# URUTKAN (OPTIONAL)
rfm_summary = rfm_summary.sort_values(by='Total Customer', ascending=False)

# TAMPILKAN
st.dataframe(rfm_summary)

# VISUAL DISTRIBUSI
fig4, ax4 = plt.subplots()
sns.countplot(
    data=rfm,
    x='Segment',
    order=rfm['Segment'].value_counts().index,
    ax=ax4
)
plt.xticks(rotation=45)
ax4.set_title('Distribusi Segment Customer')
st.pyplot(fig4)

# TABEL RFM
st.markdown("📋 RFM Summary")

rfm_summary = rfm.groupby('Segment').agg({
    'customer_id': 'count',
    'Monetary': 'sum'
}).rename(columns={
    'customer_id': 'Total Customer',
    'Monetary': 'Total Revenue'
})

st.dataframe(rfm_summary)



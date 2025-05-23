import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# setup halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")
st.title("📊 Dashboard Penyewaan Sepeda")

# load data
day_df = pd.read_csv('data/day.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['year_month'] = day_df['dteday'].dt.to_period('M')

# filter tanggal
st.sidebar.header("Filter Tanggal")
start_date = st.sidebar.date_input("Mulai Tanggal", day_df['dteday'].min())
end_date = st.sidebar.date_input("Akhir Tanggal", day_df['dteday'].max())
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                     (day_df['dteday'] <= pd.to_datetime(end_date))]

# metrik utama
total_cnt = filtered_df['cnt'].sum()
total_registered = filtered_df['registered'].sum()
total_casual = filtered_df['casual'].sum()

st.subheader("Statistik Umum")
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{total_cnt:,}")
col2.metric("Total Registered", f"{total_registered:,}")
col3.metric("Total Casual", f"{total_casual:,}")

# visualisasi baru: tren registered
st.subheader("Tren Distribusi Bulanan Pengguna Registered (2011–2012)")
monthly_registered = (
    filtered_df.groupby('year_month')['registered'].sum().reset_index()
)
monthly_registered['year_month'] = monthly_registered['year_month'].astype(str)

fig1 = plt.figure(figsize=(12, 6))
plt.plot(monthly_registered['year_month'], monthly_registered['registered'], marker='o')
plt.xticks(rotation=45)
plt.title('Tren Bulanan Pengguna Registered (2011–2012)')
plt.xlabel('Tahun dan Bulan')
plt.ylabel('Total Pengguna Registered')
plt.grid(True)
plt.tight_layout()
st.pyplot(fig1)

# visualisasi baru: workingday
st.subheader("Rata-rata Peminjaman berdasarkan Workingday (2012)")
workingday_avg = filtered_df.groupby('workingday')['cnt'].mean().reset_index()

fig2 = plt.figure(figsize=(6, 4))
sns.barplot(data=workingday_avg, x='workingday', y='cnt', palette='pastel')
plt.title('Rata-rata Peminjaman berdasarkan Workingday (2012)')
plt.xlabel('Workingday (0 = Libur, 1 = Hari Kerja)')
plt.ylabel('Rata-rata Jumlah Peminjaman')
plt.tight_layout()
st.pyplot(fig2)

# visualisasi baru: holiday
st.subheader("Rata-rata Peminjaman berdasarkan Holiday (2012)")
holiday_avg = filtered_df.groupby('holiday')['cnt'].mean().reset_index()

fig3 = plt.figure(figsize=(6, 4))
sns.barplot(data=holiday_avg, x='holiday', y='cnt', palette='muted')
plt.title('Rata-rata Peminjaman berdasarkan Holiday (2012)')
plt.xlabel('Holiday (0 = Bukan Libur Resmi, 1 = Libur Resmi)')
plt.ylabel('Rata-rata Jumlah Peminjaman')
plt.tight_layout()
st.pyplot(fig3)

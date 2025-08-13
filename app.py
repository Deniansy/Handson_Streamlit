import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ---- set konfigurasi halaman ----
st.set_page_config(
    page_title='Dashboard Analisis Penjualan',
    # page_icon='',
    layout='wide',
    initial_sidebar_state='expanded'
)

# -- fungsi untuk memuat data --
@st.cache_data
def load_data():
    return pd.read_csv("data/data_dummy_retail_store.csv")

# load data penjualan
df_sales = load_data()
df_sales.columns = df_sales.columns.str.lower().str.replace(' ', '_') # mengubah nama kolomnya agar snake case
df_sales['tanggal_pesanan'] = pd.to_datetime(df_sales['tanggal_pesanan'])

# load model -- nanti

# judul dashboard 
st.title("Dashboard Analisis Penjualan Toko Online 33B")
st.markdown("Dashboard interaktif ini menyediakan gambaran umum performa penjualan, trend, dan *prediksi penjualan*.")

st.markdown("---") # garis pembatas 

# ----sidebar untuk filter-filter ----
st.sidebar.header("Filter & Navigasi")

pilihan_halaman = st.sidebar.radio(
    "Pilih Halaman:",
    ("Overview Dashboard", "Prediksi Penjualan")
)

# filter global (muncul untuk halaman overview dashboard)
if pilihan_halaman == "Overview Dashboard":
    st.sidebar.markdown("### Filter Dashboard")
    min_date = df_sales['tanggal_pesanan'].min().date()
    max_date = df_sales['tanggal_pesanan'].max().date()

    date_range = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        value=(min_date,max_date),
        min_value=min_date,
        max_value=max_date
    )

if len(date_range) == 2:
        start_date_filter = pd.to_datetime(date_range[0])
        end_date_filter = pd.to_datetime(date_range[1])
        filtered_df = df_sales[(df_sales['tanggal_pesanan'] >= start_date_filter) &
                               (df_sales['tanggal_pesanan'] <= end_date_filter)]
else: 
        # kalau filter date-nya belum tuntas
        filtered_df = df_sales 
    
    # filter berdasarkan wilayah 
selected_regions = st.sidebar.multiselect(
        "Pilih Wilayah:",
        options=df_sales['wilayah'].unique().tolist(),
        default=df_sales['wilayah'].unique().tolist()
    )

filtered_df = filtered_df[filtered_df['wilayah'].isin(selected_regions)]

# filter kategori produk 
selected_categories = st.sidebar.multiselect(
        "Pilih Kategori Produk:",
        options=df_sales['kategori'].unique().tolist(),
        default=df_sales['kategori'].unique().tolist()
    )

col_vis1, col_vis2 = st.columns(2)

with col_vis1:
    st.write("#### Top 10 Produk Terlaris")

    top_product_sold = filtered_df.groupby('produk')['total_penjualan'].sum().nlargest(10).reset_index() # agregat total penjualan per produk


 # bar chart
fig_top_products = px.bar(
    top_product_sold,
    x='total_penjualan',
    y='produk',
    orientation='h'
    )

st.plotly_chart(fig_top_products, use_container_width=True)

with col_vis2:
    st.write("#### Distribusi Penjualan per Kategori")

    sales_by_category = filtered_df.groupby('kategori')['total_penjualan'].sum().reset_index()

    fig_category_pie = px.pie(
        sales_by_category,
        values='total_penjualan',
        names='kategori'
        )

    st.plotly_chart(fig_category_pie, use_container_width=True)

ol_vis1, col_vis2 = st.columns(2)

with col_vis1:
    st.write("#### Top 10 Produk Terlaris")

    top_product_sold = filtered_df.groupby('produk')['total_penjualan'].sum().nlargest(10).reset_index() # agregat total penjualan per produk

    # bar chart
    fig_top_products = px.bar(
        top_product_sold,
        x='total_penjualan',
        y='produk',
        orientation='h'
        )

    st.plotly_chart(fig_top_products, use_container_width=True)

    with col_vis2:
        st.write("#### Distribusi Penjualan per Kategori")

        sales_by_category = filtered_df.groupby('kategori')['total_penjualan'].sum().reset_index()

        fig_category_pie = px.pie(
            sales_by_category,
            values='total_penjualan',
            names='kategori'
        )

        st.plotly_chart(fig_category_pie, use_container_width=True)

# membuat 2 tabs
    tab1, tab2 = st.tabs(["Metode Pembayaran", "Penjualan per Wilayah"])

sales_by_payment = filtered_df.groupby('metode_pembayaran')['total_penjualan'].sum().reset_index()

    # membuat chart payment method
with tab1:
        # st.write("#### Penjualan Berdasarkan Metode Pembayaran")
        
        fig_payment = px.bar(
            sales_by_payment,
            x='metode_pembayaran',
            y='total_penjualan',
            title='Total Penjualan per Metode Pembayaran',
            color='metode_pembayaran'
        )

        st.plotly_chart(fig_payment, use_container_width=True)

    # membuat chart wilayah
sales_by_region = filtered_df.groupby('wilayah')['total_penjualan'].sum().reset_index()
with tab2:
        fig_region = px.bar(
            sales_by_region,
            x='wilayah',
            y='total_penjualan',
            title="Total Penjualan per Wilayah",
            color='wilayah'

        )
        st.plotly_chart(fig_region, use_container_width=True)














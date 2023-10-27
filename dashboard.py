import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import urllib
from func import DataAnalyzer
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
all_df = pd.read_csv("all_df.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    # Title
    st.title("Brazilian E-Commerce Public Dataset by Olist")

    # Date Range
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]

function = DataAnalyzer(main_df)

sum_orders_df = function.create_sum_orders_df()
review_score_df = function.create_review_score_df()
review_persentase_df = function.create_review_persentase_df()
order_status_counts_df = function.create_order_status_counts_df()
state_counts_df = function.create_state_counts_df()
city_counts_df = function.create_city_counts_df()

# Title
st.header("Brazilian E-Commerce Public Dataset by Olist")
    
# Produk apa yang paling banyak dipesan?
st.subheader("Produk apa yang paling banyak dipesan?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))
colors = ["#00CED1", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_count", y="product_category_name_english", data = sum_orders_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Produk paling banyak terjual", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)

sns.barplot(x="product_count", y="product_category_name_english", data=sum_orders_df.sort_values(by="product_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Bagaimana tingkat kepuasan pelanggan pada pesanannya?
st.subheader("Bagaimana tingkat kepuasan pelanggan pada pesanannya?")
tab1, tab2 = st.tabs(["Jumlah", "Persentase"])

with tab1:
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#00CED1"]
    sns.barplot(x = review_score_df.index, 
        y = review_score_df.values, 
        palette = colors
    )
    plt.title("Tingkat Kepuasan Pelanggan Berdasarkan Rating (Review Score)", fontsize=15)
    plt.xlabel("Rating")
    plt.ylabel("Jumlah")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(12, 6))
    labels = review_persentase_df.index
    counts = review_persentase_df.values
    colors = ["#00CED1"]
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140, wedgeprops = {'width': 0.4})
    plt.title("Tingkat Kepuasan Pelanggan Berdasarkan Rating (Review Score)",  fontsize=15)
    st.pyplot(fig)

# Bagaimana Distribusi Status Pesanan?
st.subheader("Bagaimana Distribusi Status Pesanan?")
fig, ax = plt.subplots(figsize=(12, 6))
colors = ["#00CED1"]
sns.barplot(x = order_status_counts_df.index, 
            y = order_status_counts_df.values, 
            order = order_status_counts_df.index,
            palette = colors
            )
plt.title("Distribusi Status Pesanan", fontsize=15)
plt.xlabel("Jumlah")
plt.ylabel("Status Pesanan")
plt.xticks(fontsize=12)
st.pyplot(fig)

# Bagaimana demografi pelanggan pada platform ecommerce?
st.subheader("Bagaimana demografi pelanggan pada platform ecommerce?")
tab1, tab2 = st.tabs(["Berdasarkan State", "Berdasarkan Kota"])

with tab1:
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#00CED1"]
    sns.barplot(x = state_counts_df.index, 
        y = state_counts_df.values,
        palette = colors
    )
    plt.title("Pelanggan Berdasarkan State/Negara Bagian", fontsize=15)
    plt.xlabel("State")
    plt.ylabel("Jumlah Pelanggan")
    plt.xticks(fontsize=12)
    st.pyplot(fig)

with tab2:
    fig, ay = plt.subplots(figsize=(12, 6))
    colors = ["#00CED1"]
    sns.barplot(x = city_counts_df.index, 
        y = city_counts_df.values,
        palette = colors
    )
    plt.title("Pelanggan Berdasarkan Kota", fontsize=15)
    plt.xlabel("Kota")
    plt.ylabel("Jumlah Pelanggan")
    plt.xticks(fontsize=12)
    st.pyplot(fig)
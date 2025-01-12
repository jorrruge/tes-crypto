import streamlit as st
import pandas as pd

def load_data():
    average_data = pd.read_csv("/mnt/data/AVERAGE Crypto.csv")
    saw_data = pd.read_csv("/mnt/data/SAW Crypto.csv")
    topsis_data = pd.read_csv("/mnt/data/TOPSIS Crypto.csv")
    return average_data, saw_data, topsis_data

def calculate_weighted_scores(average_data, weights):
    weighted_scores = average_data.copy()
    for column in weights.keys():
        if column in weighted_scores.columns:
            weighted_scores[column] = weighted_scores[column] * weights[column]
    weighted_scores["Total Score"] = weighted_scores.sum(axis=1)
    return weighted_scores

def display_dashboard(average_data, saw_data, topsis_data):
    st.title("Dashboard Pemilihan Platform Exchange Cryptocurrency")

    # Bobot variabel (AHP)
    weights = {
        'Kemudahan Penggunaan': 0.11,
        'Keamanan': 0.25,
        'Likuiditas': 0.06,
        'Biaya Transaksi': 0.39,
        'Reputasi Platform': 0.16,
        'Dukungan Pelanggan': 0.03
    }

    # Pilihan variabel untuk filter
    selected_variable = st.sidebar.selectbox("Pilih Variabel Penilaian:", list(weights.keys()))

    # Menampilkan tabel rata-rata
    st.subheader("Nilai Rata-rata Alternatif Berdasarkan Variabel")
    st.dataframe(average_data)

    # Menampilkan hasil perhitungan SAW
    st.subheader("Hasil Perhitungan (SAW)")
    st.dataframe(saw_data)
    st.write("Peringkat Platform berdasarkan SAW:")
    st.write("1. Indodax")
    st.write("2. Tokocrypto")
    st.write("3. Binance")

    # Menampilkan hasil perhitungan TOPSIS
    st.subheader("Hasil Perhitungan (TOPSIS)")
    st.dataframe(topsis_data)
    best_values = topsis_data.max()
    worst_values = topsis_data.min()
    st.write(f"Nilai terbaik pada variabel '{selected_variable}': {best_values[selected_variable]}")
    st.write(f"Nilai terburuk pada variabel '{selected_variable}': {worst_values[selected_variable]}")

    # Perhitungan skor berbobot dari average
    st.subheader("Peringkat Berdasarkan Bobot dan Average")
    weighted_scores = calculate_weighted_scores(average_data, weights)
    st.dataframe(weighted_scores)
    ranked_scores = weighted_scores.sort_values(by="Total Score", ascending=False)
    st.write("Peringkat berdasarkan skor total:")
    for i, row in ranked_scores.iterrows():
        st.write(f"{i + 1}. {row['Platform']} - Skor: {row['Total Score']:.2f}")

# Load data
average_data, saw_data, topsis_data = load_data()

# Display dashboard
display_dashboard(average_data, saw_data, topsis_data)

import streamlit as st
import pandas as pd
import warnings
from io import BytesIO

warnings.filterwarnings("ignore", category=RuntimeWarning)

st.title("🧹 Pembersih Komentar 'Pas' pada Data PCI")

# Upload file
uploaded_file = st.file_uploader("📤 Upload file CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Kolom yang digunakan
    kolom_no = 'No'
    kolom_komentar = 'Komentar'

    # Pastikan kolom ada
    if kolom_no in df.columns and kolom_komentar in df.columns:

        komentar_bersih = df[kolom_komentar].fillna('').str.strip().str.lower()

        # Buat mask untuk baris yang akan dihapus
        mask_hapus = df.duplicated(subset=[kolom_no], keep=False) & (komentar_bersih == 'pas')
        df_hapus = df[mask_hapus]
        df_bersih = df[~mask_hapus].reset_index(drop=True)

        st.subheader("📌 Baris yang Akan Dihapus (Komentar = 'pas' dan Duplikat No):")
        st.dataframe(df_hapus)

        st.subheader("✅ Data Setelah Dibersihkan:")
        st.dataframe(df_bersih)

        # Hitung info
        st.markdown(f"""
        - Jumlah baris awal: **{len(df)}**
        - Jumlah baris dihapus: **{mask_hapus.sum()}**
        - Jumlah baris akhir: **{len(df_bersih)}**
        """)

        # Simpan dan buat link download
        csv_buffer = BytesIO()
        df_bersih.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        st.download_button(
            label="📥 Download Hasil CSV",
            data=csv_buffer,
            file_name="hasil_bersih.csv",
            mime="text/csv"
        )
    else:
        st.error("Kolom 'No' dan 'Komentar' tidak ditemukan di file.")
else:
    st.info("Silakan upload file CSV terlebih dahulu.")

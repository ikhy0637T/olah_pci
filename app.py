import streamlit as st
import pandas as pd
import warnings
from io import BytesIO

warnings.filterwarnings("ignore", category=RuntimeWarning)

st.title("🧹 Pembersih Komentar 'Pas' pada Data PCI")

uploaded_file = st.file_uploader("📤 Upload file CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    kolom_no = 'No'
    kolom_komentar = 'Komentar'

    if kolom_no in df.columns and kolom_komentar in df.columns:

        df[kolom_komentar] = df[kolom_komentar].fillna('').str.strip().str.lower()

        rows_to_keep = []

        for no_val, group in df.groupby(kolom_no):
            komentar_values = group[kolom_komentar].tolist()

            if all(k == 'pas' for k in komentar_values):
                # Semua 'pas', maka simpan satu saja
                rows_to_keep.append(group.iloc[[0]])
            else:
                # Simpan semua yang bukan 'pas'
                rows_to_keep.append(group[group[kolom_komentar] != 'pas'])

        df_bersih = pd.concat(rows_to_keep).reset_index(drop=True)

        # Cari baris yang dihapus (untuk ditampilkan)
        index_bersih = set(df_bersih.index)
        index_asli = set(df.index)
        indeks_hapus = list(index_asli - index_bersih)
        df_hapus = df.iloc[indeks_hapus]

        st.subheader("📌 Baris yang Dihapus:")
        st.dataframe(df_hapus)

        st.subheader("✅ Data Setelah Dibersihkan:")
        st.dataframe(df_bersih)

        st.markdown(f"""
        - Jumlah baris awal: **{len(df)}**
        - Jumlah baris dihapus: **{len(indeks_hapus)}**
        - Jumlah baris akhir: **{len(df_bersih)}**
        """)

        # Buat file untuk diunduh
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

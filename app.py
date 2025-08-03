import streamlit as st
import pandas as pd

# Judul
st.title("Filter Komentar 'Pas'")

# Upload file
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Pastikan kolom 'No' dan 'Komentar' ada
    if 'No' not in df.columns or 'Komentar' not in df.columns:
        st.error("File harus memiliki kolom 'No' dan 'Komentar'")
    else:
        kolom_no = 'No'
        kolom_komentar = 'Komentar'

        rows_to_keep = []
        rows_to_delete = []

        for no, group in df.groupby(kolom_no):
            komentar_lower = group[kolom_komentar].fillna('').str.strip().str.lower()

            if all(komentar_lower == 'pas'):
                # Semua 'pas', simpan satu, hapus sisanya
                rows_to_keep.append(group.iloc[[0]])
                rows_to_delete.append(group.iloc[1:])
            elif any(komentar_lower != 'pas'):
                # Ada yang bukan pas, simpan semua yang bukan pas
                rows_to_keep.append(group[komentar_lower != 'pas'])
                rows_to_delete.append(group[komentar_lower == 'pas'])

        df_bersih = pd.concat(rows_to_keep, ignore_index=True)
        df_dihapus = pd.concat(rows_to_delete, ignore_index=True)

        # Tampilkan hasil dalam scroll container
        st.subheader("🔍 Baris yang akan DIHAPUS")
        with st.container():
            st.dataframe(df_dihapus, use_container_width=True, height=300)

        st.subheader("✅ Baris yang DISIMPAN (Hasil Akhir)")
        with st.container():
            st.dataframe(df_bersih, use_container_width=True, height=300)

        # Tombol download
        csv = df_bersih.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download hasil_bersih.csv", csv, "hasil_bersih.csv", "text/csv")

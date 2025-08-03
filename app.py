import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pembersihan Data Komentar 'pas'", layout="wide")

st.title("🧹 Pembersih Data Komentar 'pas'")

st.markdown("""
Unggah file CSV hasil survei PCI, lalu sistem akan:
- Menghapus baris dengan komentar **'pas'** jika seluruh baris dengan `No` yang sama hanya berisi 'pas'
- Jika ada komentar lain selain 'pas', hanya baris yang berisi 'pas' yang dihapus

""")

uploaded_file = st.file_uploader("📁 Upload file CSV kamu di sini", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df = df.dropna(how='all')

    if 'No' not in df.columns or 'Komentar' not in df.columns:
        st.error("❌ File harus memiliki kolom 'No' dan 'Komentar'.")
    else:
        kolom_no = 'No'
        kolom_komentar = 'Komentar'
        rows_to_keep_idx = []

        for no, group in df.groupby(kolom_no):
            komentar_lower = group[kolom_komentar].fillna('').str.strip().str.lower()
            if all(komentar_lower == 'pas'):
                rows_to_keep_idx.append(group.index[0])
            else:
                rows_to_keep_idx.extend(group[komentar_lower != 'pas'].index)

        df_bersih = df.loc[rows_to_keep_idx].reset_index(drop=True)
        df_dihapus = df.drop(index=rows_to_keep_idx).reset_index(drop=True)

        st.success("✅ Proses selesai!")
        st.write(f"📌 Jumlah baris awal: **{len(df)}**")
        st.write(f"✅ Jumlah baris tersisa: **{len(df_bersih)}**")
        st.write(f"🗑️ Jumlah baris dihapus: **{len(df_dihapus)}**")

        with st.expander("📊 Lihat hasil bersih"):
            st.dataframe(df_bersih.head(100))

        with st.expander("🗑️ Lihat baris yang dihapus"):
            st.dataframe(df_dihapus.head(100))

        # Fungsi bantu untuk ekspor CSV
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download hasil_bersih.csv",
                data=convert_df(df_bersih),
                file_name='hasil_bersih.csv',
                mime='text/csv'
            )
        with col2:
            st.download_button(
                label="📥 Download baris_dihapus.csv",
                data=convert_df(df_dihapus),
                file_name='baris_dihapus.csv',
                mime='text/csv'
            )

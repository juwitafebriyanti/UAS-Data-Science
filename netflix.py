import streamlit as st
import pandas as pd

st.title('Klasifikasi Popularitas Konten Netflix')

st.write("""
    Aplikasi ini mengklasifikasikan konten Netflix berdasarkan IMDB Score menjadi 'Populer' atau 'Tidak Populer'.
""")

# Fungsi untuk klasifikasi
def classify_popularity(imdb_score):
    if imdb_score >= 6.1:
        return "Populer"
    else:
        return "Tidak Populer"

# Path ke file dataset bawaan
file_path = 'Dataset/NetflixOriginals.xlsx'  

try:
    df = pd.read_excel(file_path)

    if 'IMDB Score' in df.columns:
        df['Popularitas'] = df['IMDB Score'].apply(classify_popularity)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("10 Konten Populer")
            populer = df[df['Popularitas'] == "Populer"].head(10)[['Title', 'IMDB Score', 'Popularitas']]
            populer = populer.reset_index(drop=True)  
            populer.index = populer.index + 1 
            st.dataframe(populer)

        with col2:
            st.subheader("10 Konten Tidak Populer")
            tidak_populer = df[df['Popularitas'] == "Tidak Populer"].head(10)[['Title', 'IMDB Score', 'Popularitas']]
            tidak_populer = tidak_populer.reset_index(drop=True)  
            tidak_populer.index = tidak_populer.index + 1  
            st.dataframe(tidak_populer)

        # Inisialisasi DataFrame untuk data baru
        if "data_baru" not in st.session_state:
            st.session_state.data_baru = pd.DataFrame(columns=["Title", "IMDB Score", "Popularitas"])

        # Form untuk input data baru
        with st.form("input_form"):
            title = st.text_input("Masukkan Judul Konten Baru:")
            imdb_score = st.number_input("Masukkan IMDB Score Baru:", min_value=0.0, max_value=10.0, step=0.1)
            submitted = st.form_submit_button("Tambahkan")

            if submitted:
                if title.strip() and 0.0 <= imdb_score <= 10.0:
                    popularitas = classify_popularity(imdb_score)

                    new_data = pd.DataFrame({"Title": [title], "IMDB Score": [imdb_score], "Popularitas": [popularitas]})
                    st.session_state.data_baru = pd.concat([st.session_state.data_baru, new_data], ignore_index=True)
                    st.success(f"Konten '{title}' berhasil ditambahkan!")
                else:
                    st.error("Judul tidak boleh kosong dan IMDB Score harus berada dalam rentang 0-10.")

        # Reset index dan mulai dari 1 untuk data baru
        st.session_state.data_baru = st.session_state.data_baru.reset_index(drop=True)
        st.session_state.data_baru.index = st.session_state.data_baru.index + 1

        # Tampilkan data baru yang telah ditambahkan
        st.write("Data Baru yang Ditambahkan:")
        st.write(st.session_state.data_baru)

        # Gabungkan data lama dan data baru untuk diunduh
        gabungan_data = pd.concat([df[['Title', 'IMDB Score', 'Popularitas']], st.session_state.data_baru], ignore_index=True)

        # Reset index mulai dari 1
        gabungan_data.index = gabungan_data.index + 1

        # Tombol download data gabungan
        csv = gabungan_data.to_csv(index=False)
        st.download_button(
            label="Download Data Gabungan",
            data=csv,
            file_name='netflix_popularity_combined.csv',
            mime='text/csv'
        )
    else:
        st.error("Kolom 'IMDB Score' tidak ditemukan di dataset.")
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file: {e}")

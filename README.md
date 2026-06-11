# AI Student Impact BI Dashboard — Modul 6

Dashboard interaktif ini dibuat untuk studi kasus **Analisis Dampak Penggunaan AI Generatif terhadap Performa Akademik dan Kesejahteraan Mahasiswa** pada Skema Sertifikasi Data Analyst.

## Isi paket

- `app.py` — kode utama dashboard Streamlit.
- `requirements.txt` — daftar package untuk Streamlit Cloud.
- `.streamlit/config.toml` — konfigurasi tema dark dashboard.
- `data/clean_dataset_ai_student_impact.csv` — clean dataset hasil Modul 4.
- `data/data_cleaning_log.csv` — log pembersihan data.
- `dashboard_validation_tests.py` — script uji kualitas data dasar sebelum deploy.

## Fitur dashboard

Dashboard memenuhi instruksi Modul 6:

1. Minimal 5 visualisasi interaktif.
2. Filter `Major_Category`, `Year_of_Study`, dan `Institutional_Policy`.
3. KPI rata-rata Post GPA, rata-rata Skill Retention Score, dan persentase High Burnout Risk.
4. Ringkasan insight yang menjawab pertanyaan bisnis utama.
5. Uji data tidak valid dan filter ekstrem pada tab **Kualitas data & uji**.
6. Bahasa bisnis yang jelas dan etis, dengan penekanan bahwa hasil bersifat asosiasi, bukan kausalitas.

Visualisasi wajib yang dimasukkan:

- Distribusi GPA Pre vs Post per `Major_Category`.
- Distribusi `Burnout_Risk_Level` per `Institutional_Policy`.
- Komposisi penggunaan AI per `Year_of_Study`.
- Profil risiko mahasiswa berdasarkan AI dependency dan burnout risk.
- Scatter `Weekly_GenAI_Hours` vs `Post_Semester_GPA`.
- Scatter `Weekly_GenAI_Hours` vs `Skill_Retention_Score`.
- Boxplot `Perceived_AI_Dependency` vs `Burnout_Risk_Level`.
- Ringkasan segmentasi Light, Moderate, dan Heavy User.

## Cara menjalankan lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Cara deploy ke Streamlit Cloud

1. Buat repository GitHub baru.
2. Upload seluruh isi folder ini ke repository.
3. Buka Streamlit Cloud.
4. Pilih repository dan branch.
5. Set main file path ke `app.py`.
6. Deploy.

Tidak diperlukan secrets karena dashboard memakai file CSV lokal pada folder `data/`.

## Catatan interpretasi

Dashboard ini menyajikan pola pada level agregat. Hasil tidak boleh digunakan sebagai diagnosis individu atau bukti sebab-akibat langsung antara penggunaan AI dan outcome akademik/kesejahteraan.

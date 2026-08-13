STRUKTUR FILE:
- notebook: skripsi.ipynb
- streamlit UI: app.py
- data siap training: paired_datase.npz
- data setelah clustering: clustered_meta.csv & clustered_data.csv
- hasil skor clustering: cluster_metrics.npz & cluster_metrics_2.npz

HOW TO RUN:
1. Training & clustering dengan data yang sudah siap:
   - run cell 1 (import library)
   - 17 (load data dan buat batch generator)
   - 18, 19 (defininsikan dan buat model)
   - 23 (fungsi training)
   - 24 (training)
   - 26, 27 (save model)
   - 30, 35 (buat fungsi ekstraksi fitur & buat embeddings(fitur))
   - 36, 37, 38 (K-Means clustering, Elbow Method dan save hasilnya ke file)
   - 42, 43 (evaluasi silhouette, DBI dan stability)
2. Menyiapkan dan Training & clustering dengan data baru:
   - edit dataset diluar code jika tidak menggunakan semua data aslinya
   - run cell 1 (import library)
   - run cell 2 (ganti path ke dataset jika berbeda)
   - 4, 5 (bersihkan data dari tanda baca)
   - 8 (bersihkan kata berulang dan tidak bermakna)
   - 9, 10 (augmentasi lirik lagu)
   - 13, 14 (tentukan panjang lirik seragam)
   - 15 (tokenize, sequence dan pair semua data)
   - 16 (save paired_data)
   - lanjutkan seperti training & clustering dengan data yang sudah siap
3. Aplikasi streamlit:
   - pastikan modul streamlit telah terinstall
   - copy path dari app.py
   - dalam terminal ketik "streamlit run 'path-to-app.py'"
   - buka browser

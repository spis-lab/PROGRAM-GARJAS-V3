## 🚀 Panduan Pengaturan dan Menjalankan Program Garjas V3

Selamat datang di Program Garjas V3! Panduan ini akan memandu Anda langkah demi langkah untuk menyiapkan lingkungan yang diperlukan dan menjalankan aplikasi.

### ⚠️ Persyaratan Sistem Penting

Aplikasi ini sangat bergantung pada *library* **`mediapipe`**, yang memiliki batasan versi Python yang ketat.

* **Versi Python Wajib:** Pastikan Anda telah menginstal **Python versi 3.9, 3.10, 3.11, atau 3.12**.
    * (Jika Anda menggunakan versi di luar rentang ini, kemungkinan besar instalasi akan gagal atau aplikasi tidak berjalan dengan benar.)
* **Akses Internet:** Diperlukan untuk proses instalasi *library* di langkah 4.

---

### 📋 Langkah-Langkah Instalasi dan Menjalankan Program

Ikuti langkah-langkah ini secara berurutan.

#### 1. Ekstraksi File

Ekstrak file ZIP atau folder proyek yang Anda terima ke lokasi yang mudah diakses di komputer Anda. (misalnya, di Desktop).

#### 2. Buka Terminal / Command Prompt

Buka aplikasi **Terminal** (di macOS/Linux) atau **Command Prompt / PowerShell** (di Windows), lalu navigasikan ke folder proyek yang baru Anda ekstrak.

Ganti `[PATH_FOLDER_ANDA]` dengan jalur yang sesuai di komputer Anda:

```bash
cd "[PATH_FOLDER_ANDA]/Program Garjas V3"
```

#### 3. (Opsional namun Disarankan) Membuat Virtual Environment Baru

Sangat disarankan untuk membuat virtual environment baru untuk menghindari konflik library dengan program lain di komputer Anda.

1. Buat Venv Baru:
    ```bash
    python -m venv venv_garjasv3
    ```

2. Aktifkan Venv:
    * Di Windows:
    ```bash
    venv_garjasv3\Scripts\activate
    ```

    * Di MacOs/Linux:
    ```bash
    source venv_garjasv3/bin/activate
    ```
    Setelah berhasil diaktifkan, Anda akan melihat ```(garjas_venv)``` muncul di awal baris Terminal Anda.

#### 4. Instalasi Dependensi (Library)

Proyek ini membutuhkan beberapa library Python yang terdaftar dalam file ```requirements.txt```.

Jalankan perintah ini untuk menginstal semua library secara otomatis:

```bash
pip install -r requirements.txt
```

**Catatan:** Proses ini mungkin memerlukan waktu beberapa menit tergantung kecepatan koneksi internet Anda.

#### 5. Menjalankan Aplikasi

Setelah semua library terinstal, Anda siap menjalankan aplikasi utama!

```bash
python main.py
```

Aplikasi GUI (KivyMD) seharusnya akan terbuka dan siap digunakan.
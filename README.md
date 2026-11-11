# ORBIT Backend

**ORBIT (Online Retail Behavior & Insight Tracker)** adalah backend REST API untuk mengolah data transaksi retail, menghitung *Recency, Frequency, Monetary* (RFM), dan menyediakan data yang akan ditampilkan oleh dashboard frontend.

Backend menggunakan **Python, FastAPI, Pandas, SQLAlchemy, dan PostgreSQL**. Modul **Fuzzy Mamdani** untuk segmentasi pelanggan masih dalam pengembangan: fungsi keanggotaan dan *rule base* belum ditetapkan.

> **Status:** aplikasi FastAPI dan Swagger UI sudah berhasil dijalankan secara lokal. Pengujian upload dataset Online Retail dan integrasi frontend masih perlu dilakukan.

## Tech stack

| Komponen | Teknologi |
|---|---|
| REST API | FastAPI + Uvicorn |
| Data processing | Pandas + NumPy |
| Baca Excel | OpenPyXL |
| Fuzzy inference (rencana) | Scikit-fuzzy |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy |
| Konfigurasi | Pydantic Settings (`.env`) |
| Testing | Pytest |

## Prasyarat

Pastikan sudah tersedia:

1. **Git**
2. **Python** (direkomendasikan 3.10–3.12; jika menggunakan 3.9, gunakan versi dependensi kompatibel yang berhasil terpasang)
3. **Docker Desktop** atau PostgreSQL lokal yang sudah berjalan
4. **VS Code** atau editor pilihan

Periksa instalasi:

```bash
python3 --version  # macOS / Linux
git --version
docker --version
docker compose version
```

> Docker Desktop harus **dibuka dan berjalan** sebelum menggunakan `docker compose`. Bila menggunakan PostgreSQL yang sudah terpasang secara lokal, Docker tidak wajib.

## 1. Clone repository

```bash
git clone https://github.com/USERNAME/REPO_NAME.git
cd REPO_NAME
```

Ganti `USERNAME/REPO_NAME` dengan alamat repository GitHub ORBIT yang sebenarnya. Jika folder project sudah tersedia, cukup buka folder tersebut di terminal.

## 2. Buat virtual environment

### macOS / Linux (zsh / bash)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Jika PowerShell menolak aktivasi, jalankan perintah ini **hanya untuk sesi terminal saat ini**, lalu ulangi aktivasi:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Setelah aktif, biasanya terminal menampilkan `(.venv)`. **Jangan commit folder `.venv` ke GitHub.**

## 3. Install dependencies

Dengan virtual environment aktif:

```bash
python -m pip install -r requirements.txt
```

Cek Uvicorn:

```bash
python -m uvicorn --version
```

Jika `uvicorn: command not found`, gunakan selalu `python -m uvicorn ...` dengan `.venv` yang aktif.

## 4. Konfigurasi environment

Buat file `.env` dari contoh:

### macOS / Linux

```bash
cp .env.example .env
```

### Windows (PowerShell)

```powershell
Copy-Item .env.example .env
```

Contoh isi `.env` dari repository ini:

```dotenv
DATABASE_URL=postgresql+psycopg://orbit:orbit_dev_password@localhost:5432/orbit
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
MAX_UPLOAD_MB=25
```

Keterangan:

- `DATABASE_URL`: kredensial dan alamat PostgreSQL; harus cocok dengan database yang berjalan.
- `CORS_ORIGINS`: alamat frontend yang diizinkan mengakses API melalui browser. Tambahkan origin lain bila frontend menggunakan port berbeda.
- `MAX_UPLOAD_MB`: batas ukuran file upload, saat ini **25 MB**.

**Keamanan:** `.env` berisi konfigurasi lokal, tidak boleh diunggah ke GitHub. Kredensial pada contoh ini hanya untuk **development lokal**, bukan production.

## 5. Menjalankan PostgreSQL

### Opsi A — Docker Compose (direkomendasikan)

Pastikan Docker Desktop sudah berjalan, lalu dari root repository:

```bash
docker compose up -d
```

Cek status:

```bash
docker compose ps
```

Container `postgres` seharusnya berstatus berjalan (dan akhirnya `healthy`). Konfigurasi `docker-compose.yml` menyiapkan:

- Host: `localhost`
- Port: `5432`
- Database: `orbit`
- Username: `orbit`
- Password: `orbit_dev_password`

Untuk melihat error database:

```bash
docker compose logs --tail=50 postgres
```

**Jika port 5432 sudah digunakan** oleh PostgreSQL atau Docker dari project lain, jangan menjalankan instance kedua pada port yang sama. Kamu bisa menggunakan instance yang sudah ada (dengan kredensial `.env` yang sesuai), atau mengganti port host pada `docker-compose.yml` dan `DATABASE_URL` bersama-sama.

Untuk menghentikan container tanpa menghapus data:

```bash
docker compose down
```

> Hindari `docker compose down -v` untuk troubleshooting biasa; opsi `-v` menghapus volume database.

### Opsi B — PostgreSQL lokal

Jika PostgreSQL sudah berjalan tanpa Docker, buat database dan user yang sesuai atau ubah `DATABASE_URL` di `.env` berdasarkan kredensial PostgreSQL lokalmu.

## 6. Jalankan backend FastAPI

Dari **root repository** dengan `.venv` aktif dan database berjalan:

```bash
python -m uvicorn app.main:app --reload
```

Output yang menandakan server aktif:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
INFO: Application startup complete.
```

Buka:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json
- **Health check:** http://127.0.0.1:8000/api/v1/health

Untuk menghentikan server, tekan **Ctrl+C** pada terminal.

> Akses `http://127.0.0.1:8000/` dapat menghasilkan `404 Not Found`. Itu normal karena route `/` tidak didefinisikan. Gunakan `/docs` atau `/api/v1/health`.

## 7. Menguji API

### Health check

Dari Swagger UI, jalankan `GET /api/v1/health`, atau gunakan:

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Harus merespons HTTP `200 OK`.

### Upload dataset

1. Buka http://127.0.0.1:8000/docs.
2. Pilih endpoint **`POST /api/v1/analyses`**.
3. Klik **Try it out**.
4. Isi field `file` dengan dataset `.csv` atau `.xlsx`.
5. Klik **Execute**.
6. Simpan nilai **`analysis_id`** dari response.

Endpoint upload akan membaca file, menjalankan cleaning dan perhitungan RFM, membuat ringkasan dashboard, lalu menyimpan hasilnya ke PostgreSQL. Pada starter ini proses upload masih **sinkron**, jadi pemrosesan file besar dapat memakan waktu.

Untuk dataset Online Retail yang sama seperti dalam laporan awal ORBIT, angka acuan yang perlu diverifikasi adalah:

| Metrik | Nilai acuan |
|---|---:|
| Baris awal | 541.909 |
| Baris setelah cleaning | 392.692 |
| Customer unik | 4.338 |
| Invoice unik | 18.532 |
| Total nilai pembelian positif | 8.887.208,89 |

Nilai tersebut merupakan **baseline dari laporan**, bukan jaminan output otomatis. Hasil harus diperiksa dengan dataset dan aturan pembersihan yang digunakan.

### Ambil dashboard

Ganti `ANALYSIS_ID` dengan nilai yang diperoleh dari upload:

```bash
curl http://127.0.0.1:8000/api/v1/analyses/ANALYSIS_ID/dashboard
```

### Endpoint yang tersedia

| Method | Endpoint | Keterangan |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/analyses` | Upload dataset CSV/XLSX |
| GET | `/api/v1/analyses` | Riwayat analisis |
| GET | `/api/v1/analyses/{analysis_id}/dashboard` | Data KPI dashboard |
| GET | `/api/v1/analyses/{analysis_id}/overview` | Ringkasan data dan cleaning |
| GET | `/api/v1/analyses/{analysis_id}/rfm?limit=100&offset=0` | Data RFM per pelanggan, dengan pagination |
| GET | `/api/v1/analyses/{analysis_id}/customers/{customer_id}` | Detail RFM pelanggan |
| GET | `/api/v1/analyses/{analysis_id}/segments` | Belum dikonfigurasi (Fuzzy Mamdani) |
| GET | `/api/v1/analyses/{analysis_id}/insights` | Belum dikonfigurasi (rekomendasi) |

Untuk struktur response aktual, lihat Swagger UI di `/docs`.

## 8. Integrasi frontend

Backend development secara default tersedia pada:

```text
http://127.0.0.1:8000
```

Contoh penggunaan di React:

```js
const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function getDashboard(analysisId) {
  const response = await fetch(
    `${API_BASE_URL}/analyses/${analysisId}/dashboard`
  );

  if (!response.ok) {
    throw new Error(`Gagal mengambil dashboard: ${response.status}`);
  }

  return response.json();
}
```

Catatan:

- Frontend perlu menyimpan `analysis_id` yang diterima setelah upload.
- Jika React menggunakan Vite (`localhost:5173`) atau port `3000`, origin tersebut sudah ada dalam `CORS_ORIGINS` contoh.
- Jika origin frontend berbeda, perbarui `.env` dan restart server.
- `localhost` pada browser frontend dan backend harus mengacu ke komputer/server yang tepat. Saat frontend dibuka dari laptop lain, `localhost` bukan laptop yang menjalankan backend.

## 9. Menjalankan test

```bash
python -m pytest -q
```

Test yang disiapkan mencakup preprocessing, RFM, perhitungan dashboard, dan placeholder/status fuzzy. Test unit **tidak menggantikan** pengujian upload end-to-end menggunakan PostgreSQL dan dataset asli.

## 10. Struktur folder

```text
orbit-backend-structured/
├── app/
│   ├── main.py                   # Inisialisasi FastAPI
│   ├── api/v1/
│   │   ├── router.py             # Registrasi APIRouter
│   │   └── endpoints/            # HTTP endpoints
│   ├── core/                     # Config dan security
│   ├── db/                       # Database, models, repositories
│   ├── schemas/                  # Skema request/response
│   ├── services/                 # Cleaning, RFM, dashboard, fuzzy
│   └── utils/                    # File handling
├── tests/                        # Pytest
├── .env.example                  # Contoh env (aman di-commit)
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 11. Troubleshooting

**`zsh: command not found: python`**

Gunakan `python3` untuk membuat virtual environment; setelah `.venv` diaktifkan, gunakan `python`.

**`zsh: command not found: uvicorn`**

Aktifkan `.venv`, install requirements, kemudian jalankan `python -m uvicorn app.main:app --reload`.

**`Connection refused` pada PostgreSQL port 5432**

Pastikan Docker Desktop berjalan, cek `docker compose ps`, periksa `.env`, serta pastikan port database tidak bentrok.

**`Address already in use` pada port 8000**

Hentikan backend lain yang menggunakan port 8000 (`Ctrl+C`), atau jalankan backend baru di port berbeda:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

**`404 Not Found` pada `/`**

Normal. Akses `/docs` atau `/api/v1/health`.

**`422 Unprocessable Entity` saat upload**

Periksa tipe file, ukuran file, nama kolom wajib, format tanggal, dan nilai transaksi. Lihat detail error pada response Swagger.

**CORS error dari React**

Periksa origin frontend (protokol + hostname + port) dan tambahkan ke `CORS_ORIGINS` di `.env`. Restart backend.

**`ModuleNotFoundError`**

Pastikan berada di root repository, virtual environment aktif, dan dependencies sudah terinstall.

## 12. Status dan rencana pengembangan

- [x] Struktur modular FastAPI
- [x] Konfigurasi database PostgreSQL
- [x] Endpoint health check
- [x] Endpoint upload, cleaning, RFM, dan ringkasan dashboard dalam starter
- [ ] Validasi end-to-end upload dataset asli dan hasil RFM
- [ ] Implementasi Fuzzy Mamdani (*membership functions*, aturan, inferensi, defuzzifikasi)
- [ ] Customer segmentation dan recommendation engine
- [ ] Autentikasi dan otorisasi pengguna
- [ ] Integrasi penuh dengan frontend
- [ ] Migrasi database (Alembic), background jobs, dan pengamanan production

> **Penting:** login/register dan Fuzzy Mamdani belum siap. Backend ini ditujukan untuk **pengembangan lokal**, bukan deployment publik tanpa autentikasi dan pengamanan tambahan.

## 13. Kolaborasi GitHub

Setelah clone dan setup, setiap anggota sebaiknya membuat branch sendiri:

```bash
git checkout -b feature/nama-fitur
# Kerjakan perubahan
git add .
git commit -m "feat: implement nama fitur"
git push -u origin feature/nama-fitur
```

Buat **Pull Request** ke branch `main`, lalu lakukan code review sebelum merge.

Jangan commit `.env`, `.venv/`, cache Python, atau dataset pelanggan yang bersifat sensitif.

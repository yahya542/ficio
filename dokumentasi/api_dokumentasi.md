1. Register User
Method: POST

URL: http://localhost:8000/api/register/ (sesuaikan dengan URL kamu)

Body (JSON):

json
Copy
Edit
{
  "noreg_bkp": "user001",
  "password": "password123"
}
Expected:
Response 201 Created, pesan sukses user dibuat.

2. Login
Method: POST

URL: http://localhost:8000/api/login/

Body (JSON):

json
Copy
Edit
{
  "noreg_bkp": "user001",
  "password": "password123"
}
Expected:
Response 200 OK dengan token access dan refresh.

3. Input Kapal (User biasa)
Method: POST

URL: http://localhost:8000/api/kapal/input/

Headers:
Authorization: Bearer <access_token_dari_login>

Body (JSON):

json
Copy
Edit
{
  "nama_kapal": "Kapal Mutiara",
  "nahkoda": "user002"   // noreg_bkp si nahkoda (pastikan user ini sudah ada)
}
Expected:
Response 201 Created dengan data kapal.

4. List Kapal
Method: GET

URL: http://localhost:8000/api/list-kapal/

Headers:
Authorization: Bearer <access_token>

Expected:
Daftar kapal yang dimiliki user atau semua kapal kalau admin.

5. Input Tangkapan (Admin)
Method: POST

URL: http://localhost:8000/api/tangkapan/input/

Headers:
Authorization: Bearer <admin_access_token>
X-ADMIN-KEY: rahasia_admin_123

Body (JSON) contoh (batch input):

json
Copy
Edit
[
  {
    "kapal": 1,             // ID kapal
    "jenis_ikan": 1,        // ID jenis ikan
    "weight": 100.5,
    "location": 713         // kode WPP
  },
  {
    "kapal": 1,
    "jenis_ikan": 2,
    "weight": 50,
    "location": 713
  }
]
Expected:
Response 201 Created, jumlah data yang berhasil disimpan.

6. List Tangkapan
Method: GET

URL: http://localhost:8000/api/list-tangkapan/

Headers:
Authorization: Bearer <access_token>
(tambahkan X-ADMIN-KEY jika mau lihat semua data)

Expected:
Daftar tangkapan sesuai hak akses.

Tips:
Pastikan dulu kamu sudah buat user untuk pemilik kapal, nahkoda, dan admin (bisa lewat register atau langsung lewat admin panel).

Gunakan token access di header Authorization: Bearer <token> untuk endpoint yang perlu autentikasi.

Jangan lupa untuk pasang header X-ADMIN-KEY untuk akses admin khusus.


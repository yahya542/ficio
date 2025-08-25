
# Dokumentasi API Fishcast

## Register Pemilik
```json
{
    "username": "dummy",
    "email": "dummy@email.com",
    "password": "dummy123",
    "role": "pemilik_kapal",
    "nama_kapal": "dummy kapal",
    "no_buku_kapal": "BKxxxx",
    "wpp_code": "000"
}
```

## Login Pemilik
```json
{
    "username/no_buku_kapal": "BKxxxx",
    "password": "dummy123"
}
```

## Register Nahkoda
```json
{
    "username": "dummy_nahkoda",
    "email": "dummy@email.com",
    "password": "dummy123",
    "role": "nahkoda",
    "no_buku_kapal": "BKxxxx"
}
```

## Login Nahkoda
```json
{
    "username/no_buku_kapal": "BKxxxx",
    "password": "dummy123"
}
```

## Register Admin
```json
{
    "username": "admin_dummy",
    "email": "admin@email.com",
    "password": "dummy123"
}
```

## Login Admin
```json
{
    "username/no_buku_kapal": "admin_dummy",
    "password": "dummy123"
}
```

## Register Regulator / Auditori
```json
{
    "username": "regulator_dummy",
    "email": "dummy@email.com",
    "password": "dummy123",
    "role": "regulator"
}
```

## Login Regulator / Auditori
```json
{
    "username/no_buku_kapal": "regulator_dummy",
    "password": "dummy123"
}
```

## Input Kuota Kapal (Regulator)
```json
{
    "no_buku_kapal": "BKxxxx",
    "kuota": 500
}
```

## Admin Import Data Kapal Manual
```python
Kapal.objects.create(no_buku_kapal='BKxxxx', nama_kapal='Dummy Kapal')
```

## Input Tangkapan
```json
{
    "no_buku_kapal": "BKxxxx",
    "tangkapan": [
        {"jenis_ikan_id": 27, "berat": 150.5, "jumlah": 50, "wpp_id": 712},
        {"jenis_ikan_id": 2, "berat": 200, "jumlah": 30, "wpp_id": 712}
    ]
}
```

## History Tangkapan
- Untuk Admin: sertakan parameter `no_buku_kapal`
- Untuk User biasa (Nahkoda/Pemilik): cukup GET tanpa parameter tambahan

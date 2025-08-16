# register pemilik #
{
  "username": "pemilik02",
  "email": "pemilik02@email.com",
  "password": "rahasia123",
  "role": "pemilik_kapal",
  "nama_kapal": "Kapal kencana",
  "no_buku_kapal": "BK23456",
  "wpp_code": "712"
}

#response : {
    "message": "User berhasil daftar",
    "noregbkp": "REG71256002"
}

# register nahkoda #

{
    "username": "nahkoda2",
    "email": "nahkoda@example.com",
    "password": "pass123",
    "role": "nahkoda",
    "no_reg_bkp": "REG71256002"
}

#response : {
    "message": "User berhasil daftar",
    "noregbkp": "REG71256002"
}

# login pemilik # 

{
    "password": "rahasia123",
    "username/noreg_bkp": "REG71256002"
}

#response : {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NTgzMzcwMSwiaWF0IjoxNzU1MjI4OTAxLCJqdGkiOiI1YTE5YTQ3ZDNjMGI0ZWYyYmVkMTBjNzVlODNiZTAyOSIsInVzZXJfaWQiOiIyIn0.irlnbvJyRdha_2fIhAKC6tahx5qWvexoPJbb53nA3o4",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1MjMyNTAxLCJpYXQiOjE3NTUyMjg5MDEsImp0aSI6ImE2MDJjNDdkMTE1MDQ4ODk5NzIwMDE5YjVkMzhjMTZkIiwidXNlcl9pZCI6IjIifQ.n9pyIv2SoN3m8U95WcbvIXyrVnqRmubeyD4ynu6lzLQ",
    "user": {
        "id": 2,
        "username": "pemilik02",
        "email": null,
        "role": "pemilik_kapal",
        "kapal": "REG71256002"
    }
}

# login nahkoda # 

{
    "password": "pass123",
    "username/noreg_bkp": "REG71256002"
}

#response : {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NTgzMzc5OSwiaWF0IjoxNzU1MjI4OTk5LCJqdGkiOiI0YzRiNmIwOGJjYWU0MmFhYTY5MzU3NzhmNWUxOTcwMSIsInVzZXJfaWQiOiIzIn0.Iq33JWq-ApbLqccFDqvVc4PRUQuOSfbOZSPiCOH47nE",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1MjMyNTk5LCJpYXQiOjE3NTUyMjg5OTksImp0aSI6IjJmNzg1NjFmMWMwYzQ5NTNiYWJhMzg2ZDA1NDJkMzI0IiwidXNlcl9pZCI6IjMifQ.wxqEYoj9LtzoiXU9Ms7_rsfnsZg4yQkO2s_poTZUqf0",
    "user": {
        "id": 3,
        "username": "nahkoda2",
        "email": "nahkoda@example.com",
        "role": "nahkoda",
        "kapal": "REG71256002"
    }
}

# admin # 

    username='admin1',
    password='rahasia123',
    email='admin@example.com'

# login admin # 
{
    "username/noreg_bkp":"admin1",
    "password":"rahasia123"
}

#response : {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1NTgzNjc2MywiaWF0IjoxNzU1MjMxOTYzLCJqdGkiOiIyYTZjMTJmN2JmNDM0ZWE3OTMwODY0YWVmYzQxNTViYSIsInVzZXJfaWQiOiI0In0.kf07U2pCvjbI_Hdf1Aa1GfMTdreFueKdEf28M7vcOn4",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1MjM1NTYzLCJpYXQiOjE3NTUyMzE5NjMsImp0aSI6IjM1ZTRkZmE3NzAwZTQ4ZjI5OTM0M2E1NDM0YmVlZGZkIiwidXNlcl9pZCI6IjQifQ.yir__atgrxreDuS62VDz9nSrFYKFnaeZJaxXOj_VIxc",
    "user": {
        "id": 4,
        "username": "admin1",
        "email": "admin@example.com",
        "role": "admin",
        "kapal": null
    }
}



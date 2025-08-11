from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Kapal, JenisIkan, WPP

class ApiTests(APITestCase):
    def setUp(self):
        # Buat admin user
        self.admin_user = CustomUser.objects.create_user(
            noreg_bkp='admin001', password='adminpass', role='admin', is_staff=True
        )
        # Buat user biasa
        self.user = CustomUser.objects.create_user(
            noreg_bkp='user001', password='userpass', role='user'
        )

        # Login endpoint URL
        self.login_url = reverse('login')  # sesuaikan nama url login kamu

        # Kapal URL
        self.kapal_url = reverse('input_kapal')  # sesuaikan nama url

        # Tangkapan URL
        self.tangkapan_url = reverse('input_tangkapan_batch')  # sesuaikan nama url

    def get_token(self, noreg_bkp, password):
        res = self.client.post(self.login_url, {'username': noreg_bkp, 'password': password})
        return res.data.get('access')

    def test_register_login_kapal(self):
        # Test Register
        register_url = reverse('register')  # sesuaikan nama url register
        data = {'noreg_bkp': 'newuser', 'password': 'newpass123'}
        res = self.client.post(register_url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Test Login
        token = self.get_token('newuser', 'newpass123')
        self.assertIsNotNone(token)

        # Pakai token untuk input kapal
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        kapal_data = {'nama_kapal': 'Kapal Baru', 'nahkoda': None}
        res = self.client.post(self.kapal_url, kapal_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_list_kapal_user_vs_admin(self):
        # Buat kapal untuk user biasa
        Kapal.objects.create(nama_kapal='Kapal User', pemilik=self.user)

        # Login user biasa
        token_user = self.get_token('user001', 'userpass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user}')
        res_user = self.client.get(reverse('list_kapal'))
        self.assertEqual(res_user.status_code, status.HTTP_200_OK)
        self.assertTrue(all(k['pemilik'] == 'user001' for k in res_user.data))

        # Login admin
        token_admin = self.get_token('admin001', 'adminpass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_admin}')
        # Kirim header admin key juga kalau perlu
        res_admin = self.client.get(reverse('list_kapal'), HTTP_X_ADMIN_KEY='rahasia_admin_123')
        self.assertEqual(res_admin.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res_admin.data) >= 1)  # admin bisa lihat semua kapal

    def test_input_tangkapan_admin_only(self):
        # Login user biasa (bukan admin)
        token_user = self.get_token('user001', 'userpass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user}')
        res = self.client.post(self.tangkapan_url, data={})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        # Login admin
        token_admin = self.get_token('admin001', 'adminpass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_admin}')
        tangkapan_data = [
            {
                "kapal": 1,  # sesuaikan id kapal yang sudah ada
                "jenis_ikan": 1,
                "weight": 10.5,
                "location": 713
            }
        ]
        res = self.client.post(self.tangkapan_url, data=tangkapan_data, format='json', HTTP_X_ADMIN_KEY='rahasia_admin_123')
        # Cek response
        self.assertIn(res.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])  # 201 kalau data valid, 400 kalau data belum lengkap/invalid


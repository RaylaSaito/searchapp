from django.test import TestCase
from .models import Product, Favorite, Category
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class FavoriteToggleTest(TestCase):
    def setUp(self):
        # カテゴリーを作成
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        # ユーザーを作成
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            account_id='test_account'
        )
        # 商品を作成
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=1000.00,
            category=self.category
        )
        self.client.login(email='testuser@example.com', password='testpassword')

        
    def test_toggle_favorite(self):
        url = reverse('search_app:toggle_favorite', args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.count(), 1)

        # 再度トグルして削除
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.count(), 0)

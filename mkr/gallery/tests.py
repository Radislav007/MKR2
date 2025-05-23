from django.test import TestCase
from .models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

class CategoryModelTest(TestCase):
    def test_category_str_and_creation(self):
        """Тестуємо створення категорії та метод __str__"""
        category = Category.objects.create(name="Природа")
        self.assertEqual(str(category), "Природа")
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().name, "Природа")


class ImageModelTest(TestCase):
    def setUp(self):
        """Створення початкових даних перед кожним тестом"""
        self.category_sea = Category.objects.create(name="Море")
        self.category_mountains = Category.objects.create(name="Гори")

    def create_test_image(self, title="Відпочинок"):
        """Допоміжний метод для створення тестового зображення"""
        test_image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # GIF header, допустимий як fake image
            content_type='image/jpeg'
        )
        return Image.objects.create(
            title=title,
            image=test_image_file,
            created_date=date.today(),
            age_limit=12
        )

    def test_image_creation_and_category_assignment(self):
        """Тестуємо створення зображення і призначення категорій"""
        image = self.create_test_image()

        image.categories.set([self.category_sea, self.category_mountains])
        image.save()

        self.assertEqual(str(image), "Відпочинок")
        self.assertEqual(image.categories.count(), 2)
        self.assertEqual(Image.objects.count(), 1)
        self.assertIn(self.category_sea, image.categories.all())
        self.assertIn(self.category_mountains, image.categories.all())

    def test_image_without_categories(self):
        """Тестуємо створення зображення без категорій"""
        image = self.create_test_image(title="Без категорій")
        self.assertEqual(image.categories.count(), 0)
        self.assertEqual(Image.objects.count(), 1)

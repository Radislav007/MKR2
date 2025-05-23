from django.test import TestCase
from .models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Природа")
        self.assertEqual(str(category), "Природа")
        self.assertEqual(Category.objects.count(), 1)

class ImageModelTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Море")
        self.category2 = Category.objects.create(name="Гори")

    def test_image_creation_with_categories(self):
        # Створюємо фейковий файл зображення
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/jpeg'
        )

        image = Image.objects.create(
            title="Відпочинок",
            image=image_file,
            created_date=date.today(),
            age_limit=12
        )
        image.categories.set([self.category1, self.category2])

        self.assertEqual(str(image), "Відпочинок")
        self.assertEqual(image.categories.count(), 2)
        self.assertEqual(Image.objects.count(), 1)
        self.assertIn(self.category1, image.categories.all())
        self.assertIn(self.category2, image.categories.all())

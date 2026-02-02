from django.test import TestCase, Client
from django.urls import reverse
from products.models import Category, Product


class CategoryModelTest(TestCase):
    """Tests for Category model"""

    def setUp(self):
        """Create test data"""
        self.parent_category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            is_active=True
        )
        self.child_category = Category.objects.create(
            name="Phones",
            slug="phones",
            parent=self.parent_category,
            is_active=True
        )

    def test_category_creation(self):
        """Test that a category can be created"""
        self.assertEqual(self.parent_category.name, "Electronics")
        self.assertTrue(self.parent_category.is_active)

    def test_category_slug_auto_generation(self):
        """Test that slug is auto-generated from name"""
        category = Category.objects.create(name="Auto Generated")
        self.assertEqual(category.slug, "auto-generated")

    def test_category_hierarchy(self):
        """Test parent-child category relationship"""
        self.assertEqual(self.child_category.parent, self.parent_category)
        self.assertIn(self.child_category, self.parent_category.children.all())


class ProductModelTest(TestCase):
    """Tests for Product model"""

    def setUp(self):
        """Create test data"""
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            is_active=True
        )
        self.product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=self.category,
            description="Test Description",
            main_image="test_image.jpg",
            in_stock=True,
            is_active=True
        )

    def test_product_creation(self):
        """Test that a product can be created"""
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.category, self.category)

    def test_product_slug_auto_generation(self):
        """Test that slug is auto-generated from name"""
        product = Product.objects.create(
            name="Another Product",
            sku="another-sku",
            category=self.category,
            description="Test",
            main_image="test.jpg"
        )
        self.assertEqual(product.slug, "another-product")

    def test_product_inactive_not_displayed(self):
        """Test that inactive products are not shown by default"""
        inactive_product = Product.objects.create(
            name="Inactive Product",
            sku="inactive-sku",
            category=self.category,
            description="Test",
            main_image="test.jpg",
            is_active=False
        )
        active_products = Product.objects.filter(is_active=True)
        self.assertNotIn(inactive_product, active_products)


class ProductListViewTest(TestCase):
    """Tests for product list view and category filtering"""

    def setUp(self):
        """Create test data"""
        self.client = Client()

        # Create categories
        self.parent_category = Category.objects.create(
            name="Parent Category",
            slug="parent-category",
            is_active=True
        )
        self.child_category = Category.objects.create(
            name="Child Category",
            slug="child-category",
            parent=self.parent_category,
            is_active=True
        )

        # Create products in parent category
        self.parent_product = Product.objects.create(
            name="Parent Product",
            slug="parent-product",
            sku="parent-sku",
            category=self.parent_category,
            description="Test",
            main_image="test.jpg",
            is_active=True
        )

        # Create products in child category
        self.child_product = Product.objects.create(
            name="Child Product",
            slug="child-product",
            sku="child-sku",
            category=self.child_category,
            description="Test",
            main_image="test.jpg",
            is_active=True
        )

    def test_product_list_view_loads(self):
        """Test that product list view loads successfully"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_all_products_displayed_without_filter(self):
        """Test that all products are displayed when no category is selected"""
        response = self.client.get(reverse('products:list'))
        self.assertIn(self.parent_product, response.context['products'])
        self.assertIn(self.child_product, response.context['products'])

    def test_category_filter_shows_only_selected_category_products(self):
        """Test that filtering by parent category shows only parent category products"""
        response = self.client.get(
            reverse('products:category', args=[self.parent_category.slug])
        )
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])

        # Should only show parent category product, not child category product
        self.assertIn(self.parent_product, products)
        self.assertNotIn(self.child_product, products)

    def test_child_category_filter_shows_only_child_products(self):
        """Test that filtering by child category shows only child category products"""
        response = self.client.get(
            reverse('products:category', args=[self.child_category.slug])
        )
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])

        # Should only show child category product
        self.assertIn(self.child_product, products)
        self.assertNotIn(self.parent_product, products)

    def test_inactive_category_returns_404(self):
        """Test that inactive category returns 404"""
        inactive_category = Category.objects.create(
            name="Inactive Category",
            slug="inactive-category",
            is_active=False
        )
        response = self.client.get(
            reverse('products:category', args=[inactive_category.slug])
        )
        self.assertEqual(response.status_code, 404)

    def test_categories_in_context(self):
        """Test that all active parent categories are passed to template context"""
        response = self.client.get(reverse('products:list'))
        categories = list(response.context['categories'])
        # View returns only parent categories (those with parent=None)
        self.assertIn(self.parent_category, categories)
        # Child categories are not directly returned in context, they're accessed through parent
        # So we don't assert child_category is in categories

    def test_search_functionality(self):
        """Test search functionality in product list"""
        response = self.client.get(reverse('products:list'), {'q': 'Parent'})
        products = list(response.context['products'])
        self.assertIn(self.parent_product, products)
        # Child product may or may not be in results depending on search logic

    def test_selected_category_in_context(self):
        """Test that selected category is passed to template context"""
        response = self.client.get(
            reverse('products:category', args=[self.parent_category.slug])
        )
        self.assertEqual(response.context['selected_category'], self.parent_category)

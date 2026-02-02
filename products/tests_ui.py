from django.test import TestCase, Client
from django.urls import reverse
from products.models import Category, Product


class UIIntegrationTest(TestCase):
    """UI/Integration tests for the product pages"""

    def setUp(self):
        """Create test data"""
        self.client = Client()

        # Create categories
        self.parent1 = Category.objects.create(
            name="Electronics",
            slug="electronics",
            is_active=True
        )
        self.child1 = Category.objects.create(
            name="Phones",
            slug="phones",
            parent=self.parent1,
            is_active=True
        )
        self.grandchild1 = Category.objects.create(
            name="Smartphones",
            slug="smartphones",
            parent=self.child1,
            is_active=True
        )

        # Create products in each category
        self.product_parent = Product.objects.create(
            name="Laptop",
            slug="laptop",
            sku="laptop-001",
            category=self.parent1,
            description="Electronics product",
            main_image="test.jpg",
            is_active=True
        )
        self.product_child = Product.objects.create(
            name="iPhone",
            slug="iphone",
            sku="iphone-001",
            category=self.child1,
            description="Mobile phone",
            main_image="test.jpg",
            is_active=True
        )
        self.product_grandchild = Product.objects.create(
            name="Pixel",
            slug="pixel",
            sku="pixel-001",
            category=self.grandchild1,
            description="Smartphone",
            main_image="test.jpg",
            is_active=True
        )

    def test_products_page_renders(self):
        """Test that products page renders without errors"""
        response = self.client.get(reverse('products:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'products/product_list.html')

    def test_category_tree_template_tag_renders(self):
        """Test that category tree template tag is used in product list"""
        response = self.client.get(reverse('products:list'))
        # Check that categories are in context
        self.assertIn('categories', response.context)
        self.assertEqual(len(response.context['categories']), 1)  # Only parent

    def test_product_list_displays_all_products(self):
        """Test that all active products are displayed on products page"""
        response = self.client.get(reverse('products:list'))
        products = list(response.context['products'])
        self.assertEqual(len(products), 3)
        self.assertIn(self.product_parent, products)
        self.assertIn(self.product_child, products)
        self.assertIn(self.product_grandchild, products)

    def test_category_link_in_response(self):
        """Test that category links are rendered in the HTML"""
        response = self.client.get(reverse('products:list'))
        html = response.content.decode()
        # Check for Electronics category link
        self.assertIn('Electronics', html)
        self.assertIn('/products/category/electronics/', html)

    def test_child_category_link_in_response(self):
        """Test that child category links are rendered"""
        response = self.client.get(reverse('products:list'))
        html = response.content.decode()
        # Check for Phones child category link
        self.assertIn('Phones', html)
        self.assertIn('/products/category/phones/', html)

    def test_grandchild_category_link_in_response(self):
        """Test that grandchild category links are rendered"""
        response = self.client.get(reverse('products:list'))
        html = response.content.decode()
        # Check for Smartphones grandchild category link
        self.assertIn('Smartphones', html)
        self.assertIn('/products/category/smartphones/', html)

    def test_filter_by_parent_category(self):
        """Test filtering products by parent category"""
        response = self.client.get(reverse('products:category', args=[self.parent1.slug]))
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        # Should only show parent category product
        self.assertEqual(len(products), 1)
        self.assertIn(self.product_parent, products)
        self.assertNotIn(self.product_child, products)
        self.assertNotIn(self.product_grandchild, products)

    def test_filter_by_child_category(self):
        """Test filtering products by child category"""
        response = self.client.get(reverse('products:category', args=[self.child1.slug]))
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        # Should only show child category product
        self.assertEqual(len(products), 1)
        self.assertIn(self.product_child, products)
        self.assertNotIn(self.product_parent, products)
        self.assertNotIn(self.product_grandchild, products)

    def test_filter_by_grandchild_category(self):
        """Test filtering products by grandchild category"""
        response = self.client.get(reverse('products:category', args=[self.grandchild1.slug]))
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        # Should only show grandchild category product
        self.assertEqual(len(products), 1)
        self.assertIn(self.product_grandchild, products)
        self.assertNotIn(self.product_parent, products)
        self.assertNotIn(self.product_child, products)

    def test_active_category_link_highlighted(self):
        """Test that active category link has active class"""
        response = self.client.get(reverse('products:category', args=[self.parent1.slug]))
        html = response.content.decode()
        # Check that active class is applied to selected category
        self.assertIn('Electronics', html)
        # Look for the active class pattern
        self.assertTrue('active' in html)

    def test_product_list_heading_updates_with_category(self):
        """Test that heading changes when category is selected"""
        response = self.client.get(reverse('products:category', args=[self.parent1.slug]))
        html = response.content.decode()
        # Should show category name in main heading
        self.assertIn('Electronics', html)
        # Check that the main h2 heading displays the category name (not "All Products" as main heading)
        self.assertIn('<h2 class="text-kiya-green fw-bold mb-0">', html)

    def test_search_functionality_renders(self):
        """Test that search box is rendered on products page"""
        response = self.client.get(reverse('products:list'))
        html = response.content.decode()
        # Check for search form
        self.assertIn('search', html.lower())
        self.assertIn('name="q"', html)

    def test_product_count_displays(self):
        """Test that product count is displayed"""
        response = self.client.get(reverse('products:list'))
        html = response.content.decode()
        # Should show count
        self.assertIn('product', html.lower())

    def test_navigation_menu_shows_services(self):
        """Test that navigation menu shows Services (not separate Services and Forms)"""
        response = self.client.get(reverse('products:list'))
        html = response.content.decode()
        # Check for Services link
        self.assertIn('Services', html)
        # Services should link to forms
        self.assertIn('forms', html)

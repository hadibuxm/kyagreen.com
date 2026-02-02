from django.test import TestCase, Client
from django.template import Template, Context
from products.models import Category, Product
from core.templatetags.core_tags import render_category_tree


class RenderCategoryTreeTagTest(TestCase):
    """Tests for render_category_tree template tag"""

    def setUp(self):
        """Create test data"""
        # Create parent category
        self.parent_category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            is_active=True
        )
        
        # Create child category
        self.child_category = Category.objects.create(
            name="Phones",
            slug="phones",
            parent=self.parent_category,
            is_active=True
        )
        
        # Create grandchild category
        self.grandchild_category = Category.objects.create(
            name="Smartphones",
            slug="smartphones",
            parent=self.child_category,
            is_active=True
        )

    def test_template_tag_returns_dict(self):
        """Test that template tag returns correct context dict"""
        categories = Category.objects.filter(parent__isnull=True)
        result = render_category_tree(categories, None)
        
        self.assertIsInstance(result, dict)
        self.assertIn('categories', result)
        self.assertIn('selected_category', result)

    def test_template_tag_with_selected_category(self):
        """Test that template tag correctly handles selected category"""
        categories = Category.objects.filter(parent__isnull=True)
        result = render_category_tree(categories, self.parent_category)
        
        self.assertEqual(result['selected_category'], self.parent_category)
        self.assertEqual(result['categories'], categories)

    def test_template_tag_without_selected_category(self):
        """Test that template tag handles no selected category"""
        categories = Category.objects.filter(parent__isnull=True)
        result = render_category_tree(categories, None)
        
        self.assertIsNone(result['selected_category'])
        self.assertEqual(result['categories'], categories)

    def test_template_tag_in_template(self):
        """Test that template tag renders correctly in a template"""
        template = Template(
            "{% load core_tags %}"
            "{% render_category_tree categories selected_category %}"
        )
        
        categories = Category.objects.filter(parent__isnull=True)
        context = Context({
            'categories': categories,
            'selected_category': self.parent_category
        })
        
        # Should not raise an exception
        result = template.render(context)
        self.assertIsNotNone(result)

    def test_category_hierarchy_preserved(self):
        """Test that category hierarchy is correctly passed to template"""
        categories = Category.objects.filter(parent__isnull=True)
        result = render_category_tree(categories)
        
        # Parent should be in the categories
        self.assertIn(self.parent_category, result['categories'])
        
        # Child should be accessible through parent
        self.assertIn(self.child_category, self.parent_category.children.all())
        self.assertIn(self.grandchild_category, self.child_category.children.all())


class GetContactInfoTagTest(TestCase):
    """Tests for get_contact_info template tag"""

    def test_contact_info_tag_loads(self):
        """Test that get_contact_info template tag can be loaded"""
        template = Template("{% load core_tags %}{% get_contact_info %}")
        # Should not raise an exception
        result = template.render(Context({}))
        self.assertIsNotNone(result)

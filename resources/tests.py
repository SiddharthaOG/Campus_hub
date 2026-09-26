from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Resource


class ResourceModelTest(TestCase):
    def setUp(self):
        self.resource = Resource.objects.create(
            title="Test Notes",
            subject="Math",
            semester=1,
            resource_type="Notes",
            external_url="https://example.com",
            description="Test description",
            tags="math,algebra,test"
        )

    def test_resource_creation(self):
        self.assertEqual(self.resource.title, "Test Notes")
        self.assertEqual(self.resource.subject, "Math")
        self.assertEqual(self.resource.semester, 1)
        self.assertEqual(self.resource.resource_type, "Notes")
        self.assertEqual(self.resource.download_count, 0)
        self.assertEqual(self.resource.upvotes, 0)
        self.assertEqual(str(self.resource), "Test Notes")

    def test_resource_default_ordering(self):
        """Test that resources are ordered by created_at descending"""
        Resource.objects.create(
            title="Newer Resource",
            subject="Physics",
            semester=2,
            resource_type="Notes",
            external_url="https://newer.com"
        )
        resources = Resource.objects.all()
        self.assertEqual(resources[0].title, "Newer Resource")

    def test_resource_tags_property(self):
        """Test that tags are stored correctly"""
        self.assertEqual(self.resource.tags, "math,algebra,test")


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.resource = Resource.objects.create(
            title="View Test",
            subject="Physics",
            semester=2,
            resource_type="Notes",
            external_url="https://test.com",
            description="Test resource for view testing",
            uploaded_by=self.user
        )

    def test_home_page_status(self):
        response = self.client.get(reverse('resources:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Campus Resource Hub")
        self.assertTemplateUsed(response, 'resources/home.html')

    def test_list_page_status(self):
        response = self.client.get(reverse('resources:resource_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test")
        self.assertTemplateUsed(response, 'resources/resource_list.html')

    def test_detail_page_status(self):
        response = self.client.get(reverse('resources:resource_detail', args=[self.resource.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test")
        self.assertContains(response, "Physics")
        self.assertTemplateUsed(response, 'resources/resource_detail.html')

    def test_detail_page_404(self):
        response = self.client.get(reverse('resources:resource_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_search_functionality(self):
        response = self.client.get(reverse('resources:resource_list'), {'search': 'Physics'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test")
        self.assertNotContains(response, "Test Notes")

    def test_filter_by_subject(self):
        response = self.client.get(reverse('resources:resource_list'), {'subject': 'Physics'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test")

    def test_filter_by_semester(self):
        response = self.client.get(reverse('resources:resource_list'), {'semester': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test")

    def test_filter_by_resource_type(self):
        response = self.client.get(reverse('resources:resource_list'), {'resource_type': 'Notes'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test")


class UpvoteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.resource = Resource.objects.create(
            title="Upvote Test",
            subject="Chemistry",
            semester=3,
            resource_type="Study Material",
            external_url="https://upvote.com"
        )

    def test_upvote_increments_count(self):
        initial_upvotes = self.resource.upvotes
        response = self.client.post(reverse('resources:upvote_resource', args=[self.resource.pk]))
        self.resource.refresh_from_db()
        self.assertEqual(self.resource.upvotes, initial_upvotes + 1)
        self.assertRedirects(response, reverse('resources:resource_detail', args=[self.resource.pk]))

    def test_upvote_htmx_request(self):
        """Test upvote with HTMX header returns partial"""
        response = self.client.post(
            reverse('resources:upvote_resource', args=[self.resource.pk]),
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/partials/upvote_button.html')
        self.resource.refresh_from_db()
        self.assertEqual(self.resource.upvotes, 1)


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_signup_page_status(self):
        response = self.client.get(reverse('resources:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_login_page_status(self):
        response = self.client.get(reverse('resources:login'))
        self.assertEqual(response.status_code, 200)

    def test_add_resource_requires_login(self):
        response = self.client.get(reverse('resources:add_resource'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)

    def test_add_resource_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('resources:add_resource'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/add_resource.html')


class HTMXPartialTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.resource = Resource.objects.create(
            title="HTMX Test",
            subject="Biology",
            semester=1,
            resource_type="Lab Manual",
            external_url="https://htmx.com"
        )

    def test_resource_grid_partial(self):
        """Test that HTMX request returns partial template"""
        response = self.client.get(
            reverse('resources:resource_list'),
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/partials/resource_grid.html')
        self.assertContains(response, "HTMX Test")

    def test_search_htmx(self):
        """Test HTMX search functionality"""
        response = self.client.get(
            reverse('resources:resource_list'),
            {'search': 'Biology'},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "HTMX Test")


class AddResourceTest(TestCase):
    """Tests for add_resource view"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
    
    def test_add_resource_requires_login(self):
        """Test that add_resource redirects to login for anonymous users"""
        response = self.client.get(reverse('resources:add_resource'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_add_resource_get_authenticated(self):
        """Test that authenticated users can access add resource page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('resources:add_resource'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resources/add_resource.html')
    
    def test_add_resource_post_valid(self):
        """Test successful resource creation"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('resources:add_resource'), {
            'title': 'New Test Resource',
            'description': 'Test description',
            'subject': 'Computer Science',
            'semester': 3,
            'branch': 'CSE',
            'resource_type': 'Notes',
            'tags': 'test,notes',
            'external_url': 'https://example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Resource.objects.filter(title='New Test Resource').exists())
    
    def test_add_resource_post_invalid(self):
        """Test resource creation with missing required fields"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('resources:add_resource'), {
            'title': '',  # Missing required field
            'subject': 'Computer Science',
            'semester': 3,
            'branch': 'CSE',
            'resource_type': 'Notes',
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFormError(response, 'form', 'title', 'This field is required.')
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from mailing.apps.users.tests.mixins import SetUpUserMixin

class UserRegistrationTestCase(APITestCase):
    """Class for testing user registration."""

    def setUp(self):
        self.url = reverse('user_register')
        self.email = 'test@test.test'
        self.password = '123'
        self.name = 'Mr Test'

    def testRegisterUser(self):
        """Checks user registration."""
        post_data = {
            'email': self.email,
            'password': self.password,
            'name': self.name
        }
        r = self.client.post(self.url, data=post_data)
        self.assertEqual(status.HTTP_201_CREATED, r.status_code)

        self.assertTupleEqual(
            (r.data['email'], r.data['name']),
            (self.email, self.name)
        )
        self.assertNotIn('password', r.data)

    def testRegisterUserWithInvalidEmail(self):
        """Checks user registration with invalid email in post data."""
        invalid_email = "just_email"
        post_data = {
            'email': invalid_email,
            'password': self.password,
            'name': self.name,
        }
        r = self.client.post(self.url, data=post_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def testRegisterUserWithoutPassword(self):
        """Checks user registration without password in post data."""
        invalid_email = "just_email"
        post_data = {
            'email': self.email,
            'password': '',
            'name': self.name,
        }
        r = self.client.post(self.url, data=post_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

class LoginUserTestCase(SetUpUserMixin, APITestCase):
    """Class for testing user login."""

    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')

    def _authenticate(self, user_data):
        self.client.post(self.register_url, data=user_data)
        user_data.pop('name')
        r = self.client.post(self.login_url, data=user_data)
        self.token = r.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def testSuccessLogin(self):
        """Checks fetching token for registered user."""
        register_data = {
            'email': 'qq@qq.qq',
            'name': 'name',
            'password': 'pwd'
        }
        self.client.post(self.register_url, data=register_data)
        register_data.pop('name')
        r = self.client.post(self.login_url, data=register_data)
        self.assertEqual(status.HTTP_200_OK, r.status_code)
        self.assertIn('token', r.data)

    def testFailedLogin(self):
        """Checks login failed for unregistered user."""
        post_data = {
            'email': 'test@test.re',
            'password': '111'
        }

        r = self.client.post(self.login_url, data=post_data)
        # Strange rest_framework_jwt response status
        self.assertEqual(status.HTTP_400_BAD_REQUEST, r.status_code)

    def testGetApiForAuthenticatedUser(self):
        """Checks getting API for authenticated user."""
        url = reverse('inbox-list')
        user_data = {
            'email': 'test@qq.qq',
            'name': 'name_test',
            'password': 'pwd_test'
        }
        self._authenticate(user_data)
        r = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)


class LogoutUserTestCase(SetUpUserMixin, APITestCase):
    """Class for testing user logout."""

    def setUp(self):
        self.register_url = reverse('user_register')
        self.login_url = reverse('token_obtain_pair')
        self.logout_url = reverse('token_logout')

    def _authenticate(self, user_data):
        self.client.post(self.register_url, data=user_data)
        user_data.pop('name')
        r = self.client.post(self.login_url, data=user_data)
        self.token = r.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def testFetchListAnonymous(self):
        """Checks AnonymousUser logout."""
        r = self.client.get(self.logout_url)
        self.assertEquals(status.HTTP_401_UNAUTHORIZED, r.status_code)

    def testSuccessLogout(self):
        """Checks logout for registered user."""
        user_data = {
            'email': 'test@qq.qq',
            'name': 'name_test',
            'password': 'pwd_test'
        }
        self._authenticate(user_data)
        r = self.client.post(self.logout_url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def testGetApiForLoggedOutUser(self):
        """Checks getting API for logged out user."""
        url = reverse('sent-list')
        user_data = {
            'email': 'test@qq.qq',
            'name': 'name_test',
            'password': 'pwd_test'
        }
        self._authenticate(user_data)
        r = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        self.client.post(self.logout_url)
        self.assertEqual(status.HTTP_200_OK, r.status_code)

        r = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, r.status_code)

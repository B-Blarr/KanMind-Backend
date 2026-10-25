"""Tests for the rate limits on the authentication endpoints."""

from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class ThrottleTests(APITestCase):
    """Repeated requests on the auth endpoints are slowed down."""

    def setUp(self):
        """Start with empty throttle counters and one known user."""
        cache.clear()
        self.user = User.objects.create_user(
            username='anna@test.de', email='anna@test.de',
            password='SuperSecret123!', first_name='Anna')

    def test_eleventh_login_in_a_minute_is_rejected(self):
        """Ten tries go through, the eleventh answers 429."""
        payload = {'email': 'anna@test.de', 'password': 'wrong'}
        for _ in range(10):
            response = self.client.post(reverse('login'), payload)
            self.assertEqual(
                response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('login'), payload)
        self.assertEqual(
            response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_faked_forwarded_header_does_not_reset_the_limit(self):
        """A new X-Forwarded-For per request still counts as one client."""
        payload = {'email': 'anna@test.de', 'password': 'wrong'}
        for number in range(10):
            self.client.post(
                reverse('login'), payload,
                HTTP_X_FORWARDED_FOR=f'10.0.0.{number}')
        response = self.client.post(
            reverse('login'), payload, HTTP_X_FORWARDED_FOR='10.0.0.99')
        self.assertEqual(
            response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_login_still_works_below_the_limit(self):
        """A correct login inside the limit returns the token."""
        response = self.client.post(
            reverse('login'),
            {'email': 'anna@test.de', 'password': 'SuperSecret123!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_email_check_is_limited_to_thirty_a_minute(self):
        """The thirty-first lookup in a minute answers 429."""
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('email-check')
        for _ in range(30):
            response = self.client.get(url, {'email': 'anna@test.de'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, {'email': 'anna@test.de'})
        self.assertEqual(
            response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

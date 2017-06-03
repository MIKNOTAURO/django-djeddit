from django.contrib.auth.models import User
from django.conf import settings


def createUser(username, email, password, **kwargs):
    user = User(username=username, email=email, **kwargs)
    user.set_password(password)
    user.save()
    return user


class TestCalls(object):
    def __init__(self, template=''):
        self.template = template
        self.user = None

    def login(self, username='', password=''):
        username = username or self.username
        password = password or self.password
        if username and password:
            self.client.login(username=username, password=password)

    @classmethod
    def _setup_user(cls, username, email, password, **kwargs):
        cls.user = createUser(username, email, password, **kwargs)
        cls.username = username
        cls.password = password

    def _test_call_view_loads(self, url, data=None):
        data = data or {}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.template)

    def _test_call_view_submit(self, url, code=200, data=None):
        data = data or {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, code)
        if self.template:
            self.assertTemplateUsed(self.template)

    def _test_call_view_redirected_login(self, url, data=None):
        data = data or {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(settings.LOGIN_URL))

    def _test_call_view_redirects(self, url, redirected_url, data=None, startswith=False):
        data = data or {}
        response = self.client.get(url, data)
        if startswith:
            self.assertTrue(response.url.startswith(redirected_url))
        else:
            self.assertRedirects(response, redirected_url)

    def _test_call_view_code(self, url, code, data=None, post=False):
        data = data or {}
        response = self.client.post(url, data) if post else self.client.get(url, data)
        self.assertEqual(response.status_code, code)

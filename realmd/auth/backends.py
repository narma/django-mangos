
from mangos.realmd.models import Account
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

#from django.contrib.auth.backends import ModelBackend
from supportlib.utils.importlib import import_class

def load_auth_handler(path):
	cls = import_class(path)
	return cls()

class RealmdDefaultHandler(object):
	def login(self, account, password):
		try:
			user = User.objects.get(username=account.username)
		except User.DoesNotExist:
			email = account.email if account.email else settings.REALMD_EMPTY_EMAIL
			user  = User.objects.create(username=account.username, email=email)
			user.set_password(password)
			user.save()
		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

class RealmdBackend(object):
	def authenticate(self, username=None, password=None):
		try:
			account = Account.objects.get(username=username)
			if not account.check_password(password):
				return None
		except Account.DoesNotExist:
			return None

		handler = self.get_handler()
		return handler.login(account, password)

	def get_handler(self):
		handler_path = getattr(settings, 'REALM_AUTH_HANDLER', None)
		if handler_path:
			return load_auth_handler(handler_path)
		else:
			return RealmdDefaultHandler()

	def get_user(self, user_id):
		return self.get_handler().get_user(user_id)
	


from mangos.realmd.models import Account

def get_account(user):
	if user.is_anonymous():
		return None
	try:
		return Account.objects.get(username=user.username)
	except Account.DoesNotExist: 
		return None

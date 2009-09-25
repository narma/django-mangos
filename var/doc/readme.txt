Чтобы подключить приложение mangos в джанго-проект:

Добавте в INSTALLED_APS нужные аппликэйшины:

INSTALLED_APPS = (
		...
		'mangos.items',
		'mangos.realmd',
		'mangos.characters',
		'mangos.dbc',
)

Подключите в вашем проектном файле settings.py файл settings.py находящемся в корне приложения mangos:
from mangos.settings import *

Для использования аккаунтов realmd для аунтефикации:
Бэкенд 'mangos.realmd.auth.backends.RealmdBackend' (определяется в AUTHENTICATION_BACKENDS)
	Аунтефицирует юзера из реалмд базы.


	Аунтефицирует юзера из реалмд базы, и передает управление кастомному хандлеру, который определяется настройкой
	REALM_AUTH_HANDLER.

	Пример:

	в settings.py:
	AUTHENTICATION_BACKENDS = (
		'mangos.realmd.auth.backends.RealmdBackend',
	)
	REALM_AUTH_HANDLER = 'path.to.AuthHandler'

	интерфейс хандлера:

	class AuthHandler:
		def login(self, account, password):
			return <User-like model instance>

		def get_user(self, user_id):
			return <User-like model instance or none>

	Если настройка REALM_AUTH_HANDLER не определена, используется дефолтный хандлер который возвращает стандартного джанговского юзера.

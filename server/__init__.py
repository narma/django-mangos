import socket
from django.conf import settings
from supportlib.types import SingletonType

SERVER_DOWN = 0
SERVER_UP = 1
SERVER_HALTED = 2

class GameServer(object):
	__metaclass__ = SingletonType
	
	def get_status(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(0.25)
		
		status = SERVER_DOWN
		
		try:
			s.connect((settings.WORLD_IP, settings.WORLD_PORT))
		except socket.error:
			status = SERVER_DOWN
		else:
			status = SERVER_UP
		finally:
			s.close()
		return status
	status = property(get_status)
	
	def get_status_display(self):
		return {
			SERVER_UP: 'up',
			SERVER_DOWN: 'down',
			SERVER_HALTED: 'halted'
		}[self.status]
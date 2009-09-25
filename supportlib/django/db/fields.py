
from django.db import models
from datetime import datetime

class TimeStampField(models.PositiveIntegerField):
	__metaclass__ = models.SubfieldBase
	
	def to_python(self, value):
		if isinstance(value, datetime):
			return value
		return datetime.fromtimestamp(value)
		
	def get_db_prep_value(self, value):
		if isinstance(value, int):
			return value
		return int(value.strftime('%s'))

class BoolField(models.BooleanField):
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
		if isinstance(value, bool):
			return value
		return bool(value)
	
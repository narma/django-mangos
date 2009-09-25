
from django.db import models
from mangos.characters.opcode.formats import DataFormat, ItemInstanceFormat

from mangos.characters.helpers import Money

class ATLoginFlags(object):
	AT_LOGIN_NONE = 0
	AT_LOGIN_RENAME = 1
	AT_LOGIN_RESET_SPELLS = 2
	AT_LOGIN_RESET_TALENTS = 4

	def __init__(self, value):
		self.bitmask = value

	def _set_bit(bit):
		def set_wrapper(self, flag):
			if flag:
				self.bitmask = self.bitmask | bit
			else:
				self.bitmask = self.bitmask & ~bit
		return set_wrapper

	def _get_bit(bit):
		def get_wrapper(self):
			return bool(self.bitmask & bit)
		return get_wrapper

	rename = property(_get_bit(AT_LOGIN_RENAME), _set_bit(AT_LOGIN_RENAME))
	reset_spells = property(_get_bit(AT_LOGIN_RESET_SPELLS), _set_bit(AT_LOGIN_RESET_SPELLS))
	reset_talents = property(_get_bit(AT_LOGIN_RESET_TALENTS), _set_bit(AT_LOGIN_RESET_TALENTS))


class ATLoginField(models.PositiveIntegerField):
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
		if isinstance(value, ATLoginFlags):
			return value
		return ATLoginFlags(value)

	def get_db_prep_value(self, value):
		return value.bitmask


class MoneyField(models.PositiveIntegerField):
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
		if isinstance(value, Money):
			return value
		return Money(value)

	def get_db_prep_value(self, value):
		return value.total_coppers


class DataField(models.TextField):
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
		if isinstance(value, DataFormat):
			return value
		return DataFormat(value)

	def get_db_prep_value(self, value):
		return value.join()
	
class ItemDataField(models.TextField):
	__metaclass__ = models.SubfieldBase

	def to_python(self, value):
		if isinstance(value, ItemInstanceFormat):
			return value
		return ItemInstanceFormat(value)

	def get_db_prep_value(self, value):
		return value.join()


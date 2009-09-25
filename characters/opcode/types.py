#
# See http://wiki.udbforums.org/index.php/Character_data
#

import struct

class DataField(object):
	"""
	Base DataField for character's data field. Can be used directly for string types.
	For more complex cases extend from them.
	"""
	def __init__(self, index):
		self.index = index

	def __get__(self, instance, owner=None):
		raw_value = instance.data[self.index]
		return self.getter(raw_value)

	def __set__(self, instance, value):
		old_value = instance.data[self.index]
		instance.data[self.index] = str(self.setter(old_value, value))

	def getter(self, x):
		return x

	def setter(self, old, x):
		return x


class FloatField(DataField):
	def getter(self, x):
		return struct.unpack("f", struct.pack("i", int(x)))[0]

	def setter(self, old, x):
		return struct.unpack("i", struct.pack("f", float(x)))[0]

class IntegerField(DataField):
	def getter(self, x):
		return int(x)

	def setter(self, old, x):
		return int(x)

class PackedIntField(DataField):
	def __init__(self, index, offset, length=8):
		super(PackedIntField, self).__init__(index)
		self.offset = offset
		self.length = length

	def getter(self, x):
		x = int(x)
		x = x >> self.offset
		x = x & (2**self.length - 1)
		return x

	def setter(self, old, x):
		d = (2**self.length - 1)
		d = ~(d << self.offset)
		old = int(old) & d
		x = int(x)
		x = x << self.offset
		return old | x

	
	

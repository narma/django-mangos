
class DataFormatMeta(type):
	def get_field(cls, field_name):
		return cls.__dict__[field_name]

class DataFormatBase(object):
	__metaclass__ = DataFormatMeta

	def __init__(self, raw_data):
		#self.raw_data = raw_data
		self.data = raw_data.split(' ')

	def join(self):
		# TODO: if fields dont changed return old data ?
		return ' '.join(self.data)

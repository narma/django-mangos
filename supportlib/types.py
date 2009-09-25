
import threading
import thread

class SingletonType(type):
	"""
	To create singleton class just set metaclass to this model.
	Example:

	class Singleton(object):
		__metaclass__ = SingletonType
	"""
	def __new__(mcls, name, bases, namespace):
		# Allocate lock, if not already allocated manually
		namespace.setdefault('__lock__', threading.RLock())
		# Since we already using __new__, we can also initialize the
		# __instance__ attribute here
		namespace.setdefault('__instance__', None)
		return super(SingletonType, mcls).__new__(mcls, name, bases, namespace)

	def __call__(cls):
		cls.__lock__.acquire()
		try:
			# __instance__ is now always initialized, so no need to use default
			# value
			if cls.__instance__ is None:
				instance = cls.__new__(cls)
				instance.__init__()
				cls.__instance__ = instance
		finally:
			cls.__lock__.release()
		return cls.__instance__

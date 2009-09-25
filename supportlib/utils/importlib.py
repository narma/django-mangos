# -*- coding: utf-8 -*-

from django.utils.importlib import import_module

class ImportClassException(Exception):
	pass

def import_class(path):
	i = path.rfind('.')
	module, attr = path[:i], path[i+1:]
	try:
		mod = import_module(module)
	except ImportError, e:
		raise ImportClassException, 'Error importing class %s: "%s"' % (module, e)
	except ValueError, e:
		raise ImproperlyConfigured, 'Error importing class. Path to class a correctly defined ?'
	try:
		cls = getattr(mod, attr)
	except AttributeError:
		raise ImportClassException, 'Module "%s" does not define a "%s" class' % (module, attr)
	return cls

def import_module_names(path):
	m = import_module(path)
	return ((k,v) for k,v in m.__dict__.iteritems() if not k.startswith('_'))
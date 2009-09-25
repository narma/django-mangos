# -*- coding:utf-8 -*-
import sys, re

from django.core.management.base import BaseCommand

class Command(BaseCommand):
	help = u'Конвертирует UpdateFields.h в питоновский файл для импорта'
	args = '[path/to/file]'
	
	def handle(self, *args, **kwargs):
		if len(args) < 1:
			print >>sys.stderr, u'Укажите путь до файла'
			sys.exit(1)
		filename = args[0]
		
		input = file(filename)
		s = input.read()
		input.close()
	
		def hide_cpp_comments(s):
			def _convert_cpp(obj):
				for string in obj.groups():
					result = ''
					for line in string.splitlines():
						result += '#%s\n' % line
				return result
				
			s = re.sub(r'(/\*[\w\s\W]+\*/)', _convert_cpp, s) # Hide cpp comments
			s = re.sub(r'//', '#', s) # Hide ANSI C comments
			return s
		
		def stage2(s):
			''' Remove enums and dots in end of lines'''
			def _process(obj):
				result = ''
				rp = re.compile(r'\s+(.*?)(0x[A-F\d]{4}),')
				for s in obj.groups():
					for line in s.splitlines():
						result += '%s\n' % re.sub(rp, r'\1\2', line)
				return result
			
			return re.sub(r'enum\s[\w]+\n{([\w\s\W]*?)};', _process, s)
		
		result = hide_cpp_comments(s)
		result = stage2(result)
			
		print result	
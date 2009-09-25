from django.db import models
from django.db.models.query import Q 
from string import upper
from hashlib import sha1
from datetime import datetime
from django.utils.encoding import force_unicode

from django.db.models import F

BURNING_CRUSADE = 1
LICH_KING = 2

DEFAULT_EXPANSION = BURNING_CRUSADE

EXPANSIONS = (
	(BURNING_CRUSADE, 'Burning Crusade'),
	(LICH_KING, 'Lich King'),
)

class Account(models.Model):
	
	class Meta:
		db_table = 'realmd.account'
		managed = False
		
	username = models.CharField(max_length=32)
	sha_pass_hash = models.CharField(max_length=40)
	gmlevel = models.PositiveSmallIntegerField(default=0)
	sessionkey = models.TextField()
	v = models.TextField()
	s = models.TextField()
	email = models.CharField(max_length=64, null=True)
	joindate = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField() # default '0000-00-00 00:00:00',
	reg_ip = models.IPAddressField(default='127.0.0.1')
	last_ip = models.IPAddressField(default='127.0.0.1')
	failed_logins = models.PositiveIntegerField(default=0)
	locked = models.BooleanField(default=False)
	online = models.BooleanField(default=False)
	expansion = models.PositiveSmallIntegerField(default=DEFAULT_EXPANSION)
	mutetime = models.PositiveIntegerField(default=0)
	locale = models.PositiveSmallIntegerField(default=0)

	def __unicode__(self):
		return self.username

	@staticmethod
	def generate_pass(username, password):
		password = force_unicode(password).encode('utf-8')
		username =  force_unicode(username).encode('utf-8')
		return sha1(upper(username)+':'+upper(password)).hexdigest()
	
	def check_password(self, password):
		pass_hash = self.generate_pass(self.username, password)
		return pass_hash == self.sha_pass_hash
	
	def set_password(self, new_password):
		self.sha_pass_hash = self.generate_pass(self.username, new_password)
	
	

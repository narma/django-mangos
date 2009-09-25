from django.db import models
from django.conf import settings
import os

from mangos.dbc.models import Area

from mangos.characters.helpers import Money, Pvp
from mangos.characters import fields
from supportlib.django.db.fields import TimeStampField

from datetime import datetime
from django.db.models import F
from django.db.models.query import Q

from opcode import formats

from django.db.models.query import QuerySet

class CharacterQuerySet(QuerySet):
	def select_data(self, field):
		index = formats.DataFormat.get_field(field).index
		select_sql = "CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`data`, ' ', %d), ' ', -1) AS UNSIGNED)" % (index + 1)
		select_dict = {}
		select_dict[field] = select_sql
		return self.extra(select=select_dict)

	def sorted_data_by(self, field):
		reversed = False
		if field.startswith("-"):
			reversed = True
			field = field[1:]
		return sorted(self, key=lambda p: getattr(p.data, field), reverse=reversed)
	

class CharacterManager(models.Manager):
	def get_query_set(self):
		return CharacterQuerySet(self.model)

	def select_data(self, *args, **kwargs):
		return self.get_query_set().select_data(*args, **kwargs)


class Character(models.Model):
	""" Character model
	"""
	
	class Meta:
		db_table = 'characters.characters'
		managed = False

	# Fraction ( custom contants, not mapping on mangos db. )
	ALLIANCE = 0
	HORDE = 1
	
	# class
	WARRIOR = 1
	PALADIN = 2
	HUNTER = 3
	ROGUE = 4
	PRIEST = 5
	DEATH_KNIGHT = 6
	SHAMAN = 7
	MAGE = 8
	WARLOCK = 9
	DRUID = 11
	
	CLASS_CHOICES = (
		(WARRIOR, 'Warrior'),
		(PALADIN, 'Paladin'),
		(HUNTER, 'Hunter'),
		(ROGUE, 'Rogue'),
		(PRIEST,'Priest'),
		(DEATH_KNIGHT, 'Death Knight'),
		(SHAMAN, 'Shaman'),
		(MAGE, 'Mage'),
		(WARLOCK, 'Warlock'),
		(DRUID, 'Druid'),
	)
	
	# race
	HUMAN = 1 
	ORC = 2
	DWARF = 3
	NIGHT_ELF = 4 
	UNDEAD = 5
	TAUREN = 6
	GNOME = 7
	TROLL = 8
	BLOOD_ELF = 10 
	DRAENEI = 11

	# gender

	GENDER_MALE = 0
	GENDER_FEMALE = 1
	GENDER_NONE = 2
	
	RACE_CHOICES = (
		(HUMAN, 'Human'),
		(ORC, 'Orc'),
		(DWARF, 'Dwarf'),
		(NIGHT_ELF, 'Night Elf'),
		(UNDEAD, 'Undead'),
		(TAUREN, 'Tauren'),
		(GNOME, 'Gnome'),
		(TROLL, 'Troll'),
		(BLOOD_ELF, 'Blood Elf'),
		(DRAENEI, 'Draenei'),
	)
	
	guid = models.PositiveIntegerField(default=0, primary_key=True)
	account = models.ForeignKey('realmd.Account', db_column='account')
	data = fields.DataField() # dont use __getattr__ and __setattr__ to handle this field!
	name = models.CharField(max_length=12, db_index=True, unique=True)
	race = models.PositiveSmallIntegerField(default=0, choices=RACE_CHOICES)
	klass = models.PositiveSmallIntegerField(default=0, choices=CLASS_CHOICES, db_column='class')
	position_x = models.FloatField(default=0)
	position_y = models.FloatField(default=0)
	position_z = models.FloatField(default=0)
	map = models.ForeignKey('dbc.Map', db_column='map')
	orientation = models.FloatField(default=0)
	taximask = models.TextField()
	online = models.BooleanField(default=False, db_index=True)
	cinematic = models.BooleanField(default=0)
	totaltime = models.PositiveIntegerField(default=0)
	leveltime = models.PositiveIntegerField(default=0)
	logout_time = TimeStampField(default=0) # bigint
	is_logout_resting = models.BooleanField(default=False)
	rest_bonus = models.FloatField(default=0)
	resettalents_cost = models.PositiveIntegerField(default=0)
	resettalents_time = models.PositiveIntegerField(default=0) # bigint
	trans_x = models.FloatField(default=0)
	trans_y = models.FloatField(default=0)
	trans_z = models.FloatField(default=0)
	trans_o = models.FloatField(default=0)
	transguid = models.PositiveIntegerField(default=0) # bigint
	stable_slots = models.PositiveSmallIntegerField(default=0)
	at_login = fields.ATLoginField(default=0)
	zone = models.PositiveIntegerField(default=0) 
	death_expire_time = models.PositiveIntegerField(default=0) # bigint
	taxi_path = models.TextField()

	objects = CharacterManager()
	
	def __unicode__(self):
		return self.name

	
	@property
	def area(self):
		areas = Area.objects.filter(map=self.map, zoneid=self.zone)
		if areas.count():
			return areas[0]
		return None

	@property
	def area_name(self):
		return self.area and self.area.name or ''

	@property
	def map_name(self):
		return self.map and self.map.name or ''

	@property
	def fraction(self):
		# TODO: use faction_id from DBC
		if self.race in (self.HUMAN, self.DWARF, self.NIGHT_ELF, self.GNOME, self.DRAENEI):
			return self.ALLIANCE
		else:
			return self.HORDE

	@property
	def is_alliance(self):
		return self.fraction == self.ALLIANCE

	@property
	def is_horde(self):
		return self.fraction == self.HORDE

	@property
	def money(self):
		if not hasattr(self, '_moneyobj'):
			self._moneyobj = Money(self.data.money)
		return self._moneyobj

	@property
	def pvp(self):
		if not hasattr(self, '_pvpobj'):
			self._pvpobj = Pvp(self.data.honor, self.data.arenapoints, self.data.kills)
		return self._pvpobj
		
	@property
	def guild(self):
		guild_id = self.data.guild
		if guild_id:
			try:
				return Guild.objects.get(pk=guild_id)
			except Guild.DoesNotExist:
				pass
		return None

	@property
	def professions(self):
		if not hasattr(self, '_profsobj'):
			self._profsobj = Professions(self.data.data)
		return self._profsobj

	# ######### DATABASE MANIPULATIONS ###########

	def set_gender(self, gender):
		if gender == self.data.gender:
			return
		new_display_id = self.data.native_display_id
		if gender == self.GENDER_MALE:
			new_display_id = new_display_id + 1 if self.race == self.BLOOD_ELF else new_display_id - 1
		elif gender == self.GENDER_FEMALE:
			new_display_id = new_display_id - 1 if self.race == self.BLOOD_ELF else new_display_id + 1
		self.data.gender = gender
		self.data.display_id = new_display_id
		self.data.native_display_id = new_display_id

	def teleport_to_home(self):
		"""
		Teleport character to home.
		"""
		if not self.homebind:
			return
		self.position_x = self.homebind.position_x
		self.position_y = self.homebind.position_y
		self.position_z = self.homebind.position_z
		self.map = self.homebind.map
		self.zone = self.homebind.zone

	def attempt_fix(self):
		"""
		Fix character of 134 error and possible over.
		"""
		# clear auras
		for aura in self.aura_set.all():
			aura.delete()

		# clear raids
		for group in self.member_in.filter(Q(member__gt=F('leader')) & Q(member__lt=F('leader'))):
			group.delete()

		self.transguid = 0
		self.teleport_to_home()
		self.save()
	
	
class Guild(models.Model):
	class Meta:
		db_table = 'characters.guild'
		managed = False
	
	guildid = models.PositiveIntegerField(default=0, primary_key=True)
	name = models.CharField(max_length=255)
	leader = models.ForeignKey(Character, default=0, db_column='leaderguid')
	EmblemStyle = models.SmallIntegerField(default=0)
	EmblemColor = models.SmallIntegerField(default=0)
	BorderStyle = models.SmallIntegerField(default=0)
	BorderColor = models.SmallIntegerField(default=0)
	BackgroundColor = models.SmallIntegerField(default=0)
	info = models.TextField()
	motd = models.CharField(max_length=255)
	createdate = models.DateTimeField(null=True)
	BankMoney = models.PositiveIntegerField(default=0) # bigint
	
	def __unicode__(self):
		return self.name

class Aura(models.Model):
	class Meta:
		db_table = 'characters.character_aura'
		managed = False

	guid = models.ForeignKey(Character, primary_key=True, db_column='guid')
	caster_guid = models.PositiveIntegerField(default=0) # TODO: bigint
	spell = models.PositiveIntegerField(default=0, primary_key=True) # TODO: reference
	effect_index = models.PositiveIntegerField(default=0, primary_key=True) # TODO: reference
	amount = models.IntegerField(default=0)
	maxduration = models.IntegerField(default=0)
	remaintime = models.IntegerField(default=0)
	remaincharges = models.IntegerField(default=0)

class GroupMember(models.Model):
	class Meta:
		db_table = 'characters.group_member'
		unique_together = ('leader', 'member')
		managed = False

	leader = models.ForeignKey(Character, primary_key=True, related_name='leader_in', db_column='leaderGuid')
	member = models.ForeignKey(Character, primary_key=True, related_name='member_in', db_column='memberGuid')
	assistant = models.SmallIntegerField()
	subgroup = models.SmallIntegerField()

class HomeBind(models.Model):
	class Meta:
		db_table = 'characters.character_homebind'
		managed = False

	character = models.OneToOneField(Character, primary_key=True, related_name='homebind', db_column='guid')
	map = models.ForeignKey('dbc.Map', db_column='map')
	zone = models.PositiveIntegerField(default=0)
	position_x = models.FloatField(default=0)
	position_y = models.FloatField(default=0)
	position_z = models.FloatField(default=0)


class ItemText(models.Model):
	class Meta:
		db_table = 'characters.item_text'
		managed = False

	text = models.TextField()

class Mail(models.Model):
	class Meta:
		db_table = 'characters.mail'
		managed = False

	message_type = models.SmallIntegerField(default=0, db_column='messageType')
	stationery = models.PositiveSmallIntegerField(default=41)
	mail_template_id = models.PositiveIntegerField(default=0, db_column='mailTemplateId') # TODO: reference ?
	sender = models.ForeignKey(Character, db_column='sender', related_name='mail_sended')
	receiver = models.ForeignKey(Character, db_column='receiver', related_name='mail_receviewed')
	subject = models.CharField(max_length=255)
	item_text = models.OneToOneField(ItemText, related_name='mail', db_column='ItemTextId')
	has_items = models.BooleanField(default=False)
	expire_time = TimeStampField()
	deliver_time = TimeStampField()
	money = fields.MoneyField()
	cod = fields.MoneyField()
	checked = models.SmallIntegerField()

	def __unicode__(self):
		return self.subject

	# help functions for template

	def get_expired_days(self):
		return (self.expire_time - datetime.now()).days

	def is_empty(self):
		"""
		Check mail for empty state.
		Returns True if mail no have COD, money, attachments and body message
		"""

		if self.cod.total_coppers > 0:
			return False
		if self.money.total_coppers > 0:
			return False
		if self.item_text.text:
			return False
		if self.items.count() > 0:
			return False

		return True


class ItemInstance(models.Model):
	class Meta:
		db_table = 'characters.item_instance'
		managed = False

	guid = models.PositiveIntegerField(primary_key=True)
	owner = models.ForeignKey(Character, related_name='item_instances', db_column='owner_guid')
	data = fields.ItemDataField()

	# help functions for template
	def is_many(self):
		return self.data.stack_count > 1

class MailItem(models.Model):
	class Meta:
		db_table = 'characters.mail_items'
		managed = False

	mail = models.ForeignKey(Mail, primary_key=True, related_name='items')
	instance = models.ForeignKey(ItemInstance, primary_key=True, related_name='in_mail', db_column='item_guid')
	template = models.ForeignKey('items.ItemTemplate', db_column='item_template')
	receiver = models.ForeignKey(Character, related_name='mail_recvitems', db_column='receiver')

class Ticket(models.Model):
	class Meta:
		db_table = 'characters.character_ticket'
		managed = False
	
	ticket_id = models.PositiveIntegerField(primary_key=True)
	author = models.ForeignKey(Character, db_column='guid')
	content = models.TextField(db_column='ticket_text', null=True)
	lastchange = TimeStampField(default=0, db_column='ticket_lastchange')


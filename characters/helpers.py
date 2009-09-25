from django.utils.importlib import import_module
from django.conf import settings

from mangos.server.shared_defines import *

from supportlib.utils.importlib import import_module_names

locals().update(import_module_names('mangos.characters.opcode.constants_%s' % settings.CLIENT_VERSION_SLUG))

from mangos.bit_utils import *

__all__ = ('Money', 'Pvp', 'Professions')

class Money(object):
	def __init__(self, coppers = 0):
		coppers = int(coppers) if coppers is not None else 0
		self.total_coppers = coppers
		self.copper = coppers % 100
		self.silver = (coppers / 100 ) % 100
		self.gold = coppers / 10000

	def __unicode__(self):
		return '%s, %s, %s' % (self.gold, self.silver, self.copper)

class Pvp(object):
	HONOR_RANKS = {
		0: 0,
		500: 1,
		1500: 2,
		3000: 3,
		5000: 4,
		7500: 5,
		10000: 6,
		15000: 7,
		20000: 8,
		30000: 9,
		40000: 10,
		50000: 11,
		75000: 12,
		100000: 13,
		150000: 14,
	}
	def __init__(self, honor = 0, arenapoints = 0, kills = 0):
		self.honor = honor
		self.ap = arenapoints
		self.kills = kills
		self.rank = self._get_rank()

	def _get_rank(self):
		if self.honor == 0:
			return 0
		for cap in sorted(self.HONOR_RANKS.keys()):
			if self.honor < cap:
				return self.HONOR_RANKS[cap]
		return 15


# TODO: move it to right place.
skill_value = pair32_lopart
skill_max = pair32_hipart
make_skill_value = make_pair32

skill_temp_bonus = lambda x: 0x0000FFFF & pair32_lopart(x)
skill_perm_bonus = lambda x: 0x0000FFFF & pair32_hipart(x)
make_skill_bonus = make_pair32


class Professions(object):
	_primary_profs = {
		SKILL_BLACKSMITHING: "Blacksmithing",
		SKILL_LEATHERWORKING: "Leatherworking",
		SKILL_ALCHEMY: "Alchemy",
		SKILL_HERBALISM: "Herbalism",
		SKILL_MINING: "Mining",
		SKILL_TAILORING: "Tailoring",
		SKILL_ENGINERING: "Engineering",
		SKILL_ENCHANTING: "Enchanting",
		SKILL_SKINNING: "Skinning",
		SKILL_JEWELCRAFTING: "Jewelcrafting",
		#SKILL_INSCRIPTION #in WOTLK
	}
	_secondary_profs = {
		SKILL_COOKING: "Cooking",
		SKILL_FISHING: "Fishing",
		SKILL_FIRST_AID: "First aid"
	}
	
	class Skill(object):

		def __init__(self, id, value, bonus, name):
			self.value = skill_value(value)
			self.max = skill_max(value)
			self.temp_bonus = skill_temp_bonus(bonus)
			self.perm_bonus = skill_perm_bonus(bonus)
			self.name = name
		
		def getBaseBalue(self):
			return self.value + self.perm_bonus
		
		def getValue(self):
			return self.value + self.perm_bonus + self.temp_bonus
		
			
		def __unicode__(self):
			return u'<%s: %s>' % (self.__class__.__name__, self.name)
		
		def __str__(self):
			return self.__unicode__()
		def __repr__(self):
			return self.__unicode__() 
	
	def __init__(self, data):
		self._primary_skills = []
		self._secondary_skills = []
		for i in xrange(PLAYER_SKILL_INFO_1_1, PLAYER_CHARACTER_POINTS1, 3):
			skill = int(data[i])
			if not skill:
				continue
			skill = skill & 0x0000FFFF
			
			key = None
			if skill in self._primary_profs:
				key = '_primary'
			if skill in self._secondary_profs:
				key = '_secondary'
				
			if key:
				
				getattr(self, '%s_skills' % key).append(
					self.Skill(
						id=skill,
						value=int(data[i+1]),
						bonus=int(data[i+2]),
						name=getattr(self, '%s_profs' % key)[skill]
					)
				)
		self._skills = self._primary_skills + self._secondary_skills
	
	
	@property
	def primary(self):
		return self._primary_skills
	
	@property
	def secondary(self):
		return self._secondary_skills 
	
	def __len__(self):
		return len(self._skills)
	
	def __iter__(self):
		return iter(self._skills)
	
	def __getitem__(self, key):
		if not isinstance(key, int):
			raise TypeError("key must be int")
		if key > 256 or key < 0:
			raise IndexError("key must be positive")
		return self._skills[key]
	
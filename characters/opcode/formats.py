#
# Formats info: http://wiki.udbforums.org/index.php
#

from mangos.characters.opcode.types import *
from mangos.characters.opcode import DataFormatBase
from django.conf import settings

from mangos.server.shared_defines import *

from supportlib.utils.importlib import import_module_names

locals().update(import_module_names('mangos.characters.opcode.constants_%s' % settings.CLIENT_VERSION_SLUG))

class DataFormat(DataFormatBase):
	"""
	Items parser for Character.data
	See http://wiki.udbforums.org/index.php/Character_data
	"""
	strength =  IntegerField(index=UNIT_FIELD_STAT0)
	agility = IntegerField(index=UNIT_FIELD_STAT1)
	stamina = IntegerField(index=UNIT_FIELD_STAT2)
	intelect = IntegerField(index=UNIT_FIELD_STAT3)
	spirit = IntegerField(index=UNIT_FIELD_STAT4)

	display_id = IntegerField(index=UNIT_FIELD_DISPLAYID)
	native_display_id = IntegerField(index=UNIT_FIELD_NATIVEDISPLAYID)
	mount_display_id = IntegerField(index=UNIT_FIELD_MOUNTDISPLAYID)

	faction_id = IntegerField(index=UNIT_FIELD_FACTIONTEMPLATE)

	race = PackedIntField(index=UNIT_FIELD_BYTES_0, offset=0)    
	klass = PackedIntField(index=UNIT_FIELD_BYTES_0, offset=8)
	gender = PackedIntField(index=UNIT_FIELD_BYTES_0, offset=16)
	powertype = PackedIntField(index=UNIT_FIELD_BYTES_0, offset=24)

	health = IntegerField(index=UNIT_FIELD_HEALTH)
	health_max = IntegerField(index=UNIT_FIELD_MAXHEALTH)
	mana = IntegerField(index=UNIT_FIELD_MAXPOWER1)

	duel_team = IntegerField(index=PLAYER_DUEL_TEAM)

	guild = IntegerField(index=PLAYER_GUILDID)
	guild_rank = IntegerField(index=PLAYER_GUILDRANK)

	level = IntegerField(index=UNIT_FIELD_LEVEL)
	xp = IntegerField(index=PLAYER_XP)
	next_xp = IntegerField(index=PLAYER_NEXT_LEVEL_XP)

	honor = IntegerField(index=PLAYER_FIELD_HONOR_CURRENCY)
	kills = IntegerField(index=PLAYER_FIELD_LIFETIME_HONORBALE_KILLS)
	arenapoints = IntegerField(index=PLAYER_FIELD_ARENA_CURRENCY)

	money = IntegerField(index=PLAYER_FIELD_COINAGE)

	spell_holy_crit = FloatField(index=PLAYER_SPELL_CRIT_PERCENTAGE1+SPELL_SCHOOL_HOLY)
	spell_fire_crit = FloatField(index=PLAYER_SPELL_CRIT_PERCENTAGE1+SPELL_SCHOOL_FIRE)
	spell_nature_crit = FloatField(index=PLAYER_SPELL_CRIT_PERCENTAGE1+SPELL_SCHOOL_NATURE)
	spell_frost_crit = FloatField(index=PLAYER_SPELL_CRIT_PERCENTAGE1+SPELL_SCHOOL_FROST)
	spell_shadow_crit = FloatField(index=PLAYER_SPELL_CRIT_PERCENTAGE1+SPELL_SCHOOL_SHADOW)
	spell_arcane_crit = FloatField(index=PLAYER_SPELL_CRIT_PERCENTAGE1+SPELL_SCHOOL_ARCANE)

	spell_holy_bonus = IntegerField(index=PLAYER_FIELD_MOD_DAMAGE_DONE_POS+SPELL_SCHOOL_HOLY)
	spell_fire_bonus = IntegerField(index=PLAYER_FIELD_MOD_DAMAGE_DONE_POS+SPELL_SCHOOL_FIRE)
	spell_nature_bonus = IntegerField(index=PLAYER_FIELD_MOD_DAMAGE_DONE_POS+SPELL_SCHOOL_NATURE)
	spell_frost_bonus = IntegerField(index=PLAYER_FIELD_MOD_DAMAGE_DONE_POS+SPELL_SCHOOL_FROST)
	spell_shadow_bonus = IntegerField(index=PLAYER_FIELD_MOD_DAMAGE_DONE_POS+SPELL_SCHOOL_SHADOW)
	spell_arcane_bonus = IntegerField(index=PLAYER_FIELD_MOD_DAMAGE_DONE_POS+SPELL_SCHOOL_ARCANE)
	
	healing_bonus = IntegerField(index=PLAYER_FIELD_MOD_HEALING_DONE_POS)

	block = FloatField(index=PLAYER_BLOCK_PERCENTAGE)
	dodge = FloatField(index=PLAYER_DODGE_PERCENTAGE)
	parry = FloatField(index=PLAYER_PARRY_PERCENTAGE)
	armor = IntegerField(index=UNIT_FIELD_RESISTANCES)

	melee_crit = FloatField(index=PLAYER_CRIT_PERCENTAGE)
	range_crit = FloatField(index=PLAYER_RANGED_CRIT_PERCENTAGE)



class ItemInstanceFormat(DataFormatBase):
	"""
	Items parser for ItemInstance.data
	"""
	guid = IntegerField(index=0)
	template_entry = IntegerField(index=3)
	contained = IntegerField(index=8)
	creator = IntegerField(index=10)
	gift_creator = IntegerField(index=12)
	stack_count = IntegerField(index=14)
	duration = IntegerField(index=15)
	spell_charges = IntegerField(index=16)
	flags = IntegerField(index=21)
	enchantment = IntegerField(index=22)
	text_id = IntegerField(index=57)
	durability = IntegerField(index=58)
	max_durability = IntegerField(index=59)

__all__ = ('DataFormat', 'ItemInstanceFormat')

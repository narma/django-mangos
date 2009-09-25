
from django.db import models


class Map(models.Model):
	class Meta:
		db_table = 'mangos.dbc_map'
		managed = False
	
	name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

class Area(models.Model):
	class Meta:
		db_table = 'mangos.dbc_areatable'
		managed = False
	
	map = models.ForeignKey(Map, db_column='mapid') # bigint
	zoneid = models.PositiveIntegerField(db_index=True) # TODO: make reference # bigint
	flag = models.PositiveIntegerField()
	type = models.IntegerField()
	faction = models.IntegerField()
	name = models.CharField(max_length=128)

	def __unicode__(self):
		return self.name

class ItemDisplayInfo(models.Model):
	class Meta:
		db_table = 'mangos.dbc_itemdisplayinfo'
		managed = False

	id = models.OneToOneField('items.ItemTemplate', related_name='display_info', primary_key=True, db_column='id', to_field='displayid')
	icon = models.CharField(max_length=255)


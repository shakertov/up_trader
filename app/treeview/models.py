from django.db import models


class Menu(models.Model):
	name = models.CharField(
		max_length=50,
		verbose_name='Наименование меню')
	service_name = models.CharField(
		max_length=50,
		verbose_name='Служебное наименование')

	def __str__(self):
		return self.name

	class Meta:
		unique_together = ('id', 'service_name')
		verbose_name = 'Меню'
		verbose_name_plural = 'Меню'


class MenuItem(models.Model):
	menu = models.ForeignKey(
		Menu, on_delete=models.CASCADE,
		related_name='items',
		verbose_name='Корневое меню'
	)
	parent = models.ForeignKey(
		'MenuItem', on_delete=models.SET_NULL,
		null=True, blank=True,
		verbose_name='Родительский элемент'
	)
	title = models.CharField(
		max_length=50,
		verbose_name='Наименование элемента')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Элемент'
		verbose_name_plural = 'Элементы'

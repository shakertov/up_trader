from django import template
from django.urls import reverse_lazy
from treeview.models import Menu, MenuItem
from typing import List, Dict, Any


register = template.Library()


def list_tree(data: List[dict]) -> dict:
	"""
	Функция формирует словарь с элементами меню,
	которые вкладываются друг в друга в зависимости от
	значения родительского элемента, создавая
	иерархичную структуру по типу:
	Root
	-- Element
	----Subelement
	----Subelement
	------SubSubelement

	:data: список с исходными данными
	"""
	out = {
		None: { 'id': None, 'parent': None, 'name': 'Root', 'sub': [] }
	}

	for d in data:
		out.setdefault(d['id'], { 'sub': [] })
		out.setdefault(d['parent'], { 'sub': [] })
		out[d['id']].update(d)
		out[d['parent']]['sub'].append(out[d['id']])

	return out


def find_path(buff: Dict[int, Any], id: int, start: bool=False) -> List[int]:
	"""
	Функция формирует список индексов элементов до необходимого элемента
	для того, чтобы раскрывать только необходимые подменю

	:buff: словарь, в котором ищется путь до элемента
	:id: идентификатор элемента до которого необходимо найти путь
	:start: флажок для того, чтобы в список попал элемент
			с которого начинается путь
	"""
	if start == True:
		list_of_indexes = [buff[id]['id']] + [buff[id]['parent']]
	else:
		list_of_indexes = [buff[id]['parent']]
	if buff[id]['parent'] != None:
		return list_of_indexes + find_path(buff, buff[id]['parent'])
	else:
		return list_of_indexes


def build_items(buff: Dict[str, Any], path_to_item: List[int],
				check_key: bool, id_one: int, output: str='') -> str:
	"""
	Функция создает элемента списка HTML <li><a></a></li>

	:buff: элемент меню в виде словаря с наличием вложенных элементов в ключе 'sub'
	:path_to_item: результат работы функции find_path, определенной выше
	:check_key: т.к. меню на одной странице может быть несколько,
				то этот флажок указывает на то, что элементе с данным ID
				нет в словаре; заглушка от ошибок KeyError
	:id_one: идентификатор URL, взятый из request.resolver_match, для
			 определения какой элемент меню сейчас активен
	:output: результат работы функции, убрал в аргументы, чтобы не тратить строчку
	"""
	url = reverse_lazy('treeview_id', args=[id_one])
	url_for_one = reverse_lazy('treeview_id', args=[buff['id']])
	if url == url_for_one and id_one != None:
		output += '<li><a>'
	else:
		output += '<li><a href="{}">'.format(url_for_one)
	output += buff['title']
	output += '</a></li>'
	if buff['id'] in path_to_item and len(buff['sub']) > 0 and check_key:
		output += build_menu(buff, path_to_item, check_key, id_one)
	return output


def build_menu(buff: Dict[str, Any], path_to_item: List[int],
			   check_key: bool, id_one: int, output: str='') -> str:
	"""
	Функция создает элемента списка HTML <ul></ul>

	:buff: элемент меню в виде словаря с наличием вложенных элементов в ключе 'sub'
	:path_to_item: результат работы функции find_path, определенной выше
	:check_key: т.к. меню на одной странице может быть несколько,
				то этот флажок указывает на то, что элементе с данным ID
				нет в словаре; заглушка от ошибок KeyError
	:id_one: идентификатор URL, взятый из request.resolver_match, для
			 определения какой элемент меню сейчас активен
	:output: результат работы функции, убрал в аргументы, чтобы не тратить строчку
	"""
	submenu = [sub for sub in buff['sub']]
	if len(submenu) > 0:
		output += '<ul>'
		for sub in submenu:
			output += build_items(sub, path_to_item, check_key, id_one)
		output += '</ul>'
	return output


def check_key_in_menu(buff: Dict[int, Dict], key: int) -> bool:
	"""
	Функция для проверки наличия ключа в словаре

	:buff: словарь, в котором необходимо проверить ключ
	:key: ключ, который необходимо найти
	"""
	if buff.get(key, 0) == 0:
		return False
	return True


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name: str) -> str:
	"""
	Тэг шаблона, который выводит древовидное меню

	:context: context django
	:menu_id: идентификатор меню из БД
	"""
	item_id = context['request'].resolver_match.kwargs.get('id', None)
	try:
		dataset = Menu.objects.prefetch_related('items').get(service_name=menu_name)
		menu_name = dataset.name
		dataset = dataset.items.values('id', 'parent', 'title')
		dataset = list_tree(dataset)
		check_key = check_key_in_menu(dataset, item_id)
		if check_key:
			path_to = find_path(dataset, item_id, start=True)
		else:
			path_to = []
		output = '<h1>' + menu_name + '</h1>\n'
		output += build_menu(dataset[None], path_to, check_key, item_id)
	except Menu.DoesNotExist:
		return '<h1>Такого меню нет в БД</h1>'
	return output

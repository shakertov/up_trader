from django.shortcuts import render
from django.http import HttpResponse
from treeview.models import Menu, MenuItem


def treeview(request, id=None):
	return render(request, 'base.html', {'id': id})


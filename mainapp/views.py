from django.shortcuts import render
from django.views.generic import DetailView
from .models import Notebook, Smartphone


def test(request):
	return render(request, 'mainapp/base.html')


class ProductDetailView(DetailView):

	CT_MODEL_CLASS = {
		'notebook': Notebook,
		'smartphone': Smartphone,
	}

	def dispatch(self, request, *args, **kwargs):
		self.model = self.CT_MODEL_CLASS.get(kwargs.get('ct_model'))
		return super().dispatch(request, *args, **kwargs)

	context_object_name = 'product'
	template_name = 'mainapp/product_detail.html'

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


TABLE_HEAD = """
		<table class="table">
			<tbody>
"""

TABLE_TAIL = """
			</tbody>
		</table>
"""

TABLE_CONTENT = """
				<tr>
					<td>{key}</td>
					<td>{value}</td>
				</tr>
"""

PRODUCT_SPEC = {
	'notebook': {
		'Диагональ': 'diagonal',
		'Тип дисплея': 'display_type',
		'Частота процессора': 'processor_freq',
		'Оперативная память': 'ram',
		'Видеокарта': 'video',
		'Время работы от аккумулятора': 'time_without_charge',
	},
	'smartphone': {
		'Диагональ': 'diagonal',
		'Тип дисплея': 'display_type',
		'Разрешение экрана': 'resolution',
		'Объем аккумулятора': 'accum_volume',
		'Оперативная память': 'ram',
		'Разъем sd карты': 'sd',
		'Максимальный объeм встроенной памяти': 'sd_volume_max',
		'Разрешение главной камеры': 'main_cam_mp',
		'Разрешение фронтальной камеры': 'frontal_cam_mp'
	}
}


@register.filter
def product_spec(product):
	model_name = product.__class__._meta.model_name
	table_content = ''
	for key, value in PRODUCT_SPEC[model_name].items():
		table_content += TABLE_CONTENT.format(
			key=key, value=getattr(product, value)
		)
	return mark_safe(TABLE_HEAD + table_content + TABLE_TAIL)

from django import forms
from django.contrib.auth.models import User

from .models import Order


class OrderForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['order_date'].label='Дата получения заказа'

	order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

	class Meta:
		model = Order
		exclude = ['customer', 'status', 'cart']


class LoginForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'

	def clean(self):
		print(dir(self))
		username = self.cleaned_data['username']
		passwd = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь не найден в системе')
		user = User.objects.filter(username=username).first()
		if user:
			if not user.check_password(passwd):
				raise forms.ValidationError('Неверный пароль')
		return self.cleaned_data

	class Meta:
		model = User
		fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
	
	confirm_password = forms.CharField(widget=forms.PasswordInput)
	password = forms.CharField(widget=forms.PasswordInput)
	phone = forms.CharField(required=True)
	address = forms.CharField(required=True)
	email = forms.EmailField(required=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'
		self.fields['confirm_password'].label = 'Подтвердите пароль'
		self.fields['phone'].label = 'Номер телефон'
		self.fields['first_name'].label = 'Ваше имя'
		self.fields['last_name'].label = 'Ваша фамилия'
		self.fields['address'].label = 'Ваш адрес'
		self.fields['email'].label = 'Электронная почта'

	def clean_email(self):
		email = self.cleaned_data['email']
		domain = email.split('.')[-1]
		if domain not in ['ru',]:
			raise forms.ValidationError('Регистрация только с "ru" почтой')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Пользователь с такой почтой уже существует')
		return email

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь с таким логином уже существует')
		return username

	def clean(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']
		if password != confirm_password:
			raise forms.ValidationError('Пароли не совпадают')
		return self.cleaned_data

	class Meta:
		model = User
		fields = [
			'username', 'password', 'confirm_password', 
			'first_name', 'last_name', 'address', 'phone', 'email'
		]


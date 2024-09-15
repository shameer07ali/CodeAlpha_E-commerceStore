from django import forms
from .models import Profile, Product, CustomUser

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Product.objects.filter(slug=slug).exists():
            raise forms.ValidationError('This slug is already in use.')
        return slug

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'image']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser  # Use the CustomUser model
        fields = ('username', 'email', 'image', 'password', 'password2')  # Include the image field

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd.get('password')  # Use get() method to safely access the dictionary
        password2 = cd.get('password2')  # Use get() method to safely access the dictionary

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

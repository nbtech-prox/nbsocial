from django import forms
from django.utils.translation import gettext_lazy as _
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomSignupForm(SignupForm):
    """Formulário personalizado para registro de usuários"""
    
    first_name = forms.CharField(
        max_length=30,
        label=_('Nome'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Seu nome'),
            'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label=_('Sobrenome'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Seu sobrenome'),
            'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none'
        })
    )
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'bio', 'facebook', 'instagram', 'tiktok', 'github']
        labels = {
            'avatar': _('Foto de Perfil'),
            'bio': _('Bio'),
            'facebook': _('Facebook'),
            'instagram': _('Instagram'),
            'tiktok': _('TikTok'),
            'github': _('GitHub'),
        }
        help_texts = {
            'avatar': _('Formatos permitidos: JPG, JPEG, PNG e GIF. Tamanho máximo: 5MB.'),
            'bio': _('Uma breve descrição sobre você.'),
            'facebook': _('Link completo do seu perfil no Facebook'),
            'instagram': _('Link completo do seu perfil no Instagram'),
            'tiktok': _('Link completo do seu perfil no TikTok'),
            'github': _('Link completo do seu perfil no GitHub'),
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://facebook.com/seu.perfil'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://instagram.com/seu.perfil'
            }),
            'tiktok': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://tiktok.com/@seu.perfil'
            }),
            'github': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://github.com/seu.perfil'
            }),
        }

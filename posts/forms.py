from django import forms
from .models import Post, Comment, Report
from hashtags.models import Hashtag
from django.utils.translation import gettext_lazy as _

class PostForm(forms.ModelForm):
    hashtags_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Adicione hashtags (ex: #python #django)'),
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
        }),
        label=_('Hashtags')
    )

    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['hashtags_text'].initial = ' '.join(
                [f'#{tag.name}' for tag in self.instance.hashtags.all()]
            )

    def clean_hashtags_text(self):
        hashtags_text = self.cleaned_data.get('hashtags_text', '')
        if not hashtags_text:
            return []
        
        # Extrair nomes das hashtags do texto
        hashtag_names = [
            word[1:] for word in hashtags_text.split() 
            if word.startswith('#')
        ]
        
        # Criar ou obter objetos Hashtag
        hashtags = []
        for name in hashtag_names:
            if name:  # Ignorar hashtags vazias
                hashtag, _ = Hashtag.objects.get_or_create(name=name.lower())
                hashtags.append(hashtag)
        
        return hashtags

    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            # Limpar hashtags existentes e adicionar as novas
            post.hashtags.set(self.cleaned_data['hashtags_text'])
        
        return post

class CommentForm(forms.ModelForm):
    """Formulário para criação de comentários"""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            })
        }

class ReportForm(forms.ModelForm):
    """Formulário para denúncias"""
    
    class Meta:
        model = Report
        fields = ['report_type', 'description']
        widgets = {
            'report_type': forms.Select(attrs={
                'class': 'w-full px-3 py-2 text-gray-700 border rounded-lg focus:outline-none'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500'
            })
        }

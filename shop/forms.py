from django import forms 
from .models import Product , Comment
# from django.contrib.auth.forms import AuthenticationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body'] #'name' , 
        widgets = {
            'body' : forms.TextInput(attrs={
                'placeholder' : 'body ...',
                'class' : 'comment-body',
            }),
        }
    #         'name' : forms.TextInput(attrs={
    #             'placeholder' : 'name ...',
    #             'class' : 'comment-name',
    #         }),
    #     }

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if name:
    #         if len(name)<3:
    #             raise forms.ValidationError('نام کوتاه است !')
    #         else:
    #             return name


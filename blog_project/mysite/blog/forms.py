from django import forms
# import models that we created in Modal class so we can create forms based on them
from blog.models import Post,Comment

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author','title','text')
        # widget attribute which is a dictionary
        widgets = {
            # each key respond to a field
        #||field name|||| widget name||  ||subdictionary in which we use css built in classes or own classes ||
        #      |               |              |   || our own class ||
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            #   editable class : so we can edit the field
            #   medium-editor-textarea : give styling foractual medium editor
            #   postcontent : Our own class       || css built in classes||       || our own class ||
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')

        widget = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }

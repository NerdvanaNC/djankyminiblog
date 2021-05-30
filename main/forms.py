from django import forms

class NewPost(forms.Form):
  text = forms.CharField(label="", max_length=240, widget=(forms.TextInput(
    attrs={"class": "new-post form-control", "placeholder": "What's on your mind?", "rows": 2})))
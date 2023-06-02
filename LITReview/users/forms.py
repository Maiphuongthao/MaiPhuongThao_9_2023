from django import forms


class SubscriptionsForm(forms.Form):
    followed_user = forms.CharField(label=False, widget=forms.TextInput())
    # class Meta:
    #     model = UserFollows
    #     fields = ["followed_user"]
    #     labels = {
    #         "followed_user": ""
    #     }
    #     widgets = {'followed_user': forms.TextInput()} # attrs={
    #     #     'class': 'form-control col-auto', "placeholder":"Nom d'utilisateur"
    #     # })}

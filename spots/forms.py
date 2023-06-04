from django import forms

from spots.models import Spot, Tag, Province


class CreateSpotForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        choices=Tag.objects.all()
    )
    province = forms.ChoiceField(
        choices=Province.objects.all()
    )

    class Meta:
        model = Spot()
        fields = ('name', 'province', 'longitude', 'latitude', 'tags', 'photo')
        
from django import forms
from django.core.exceptions import ValidationError

from spots.models import Spot, Tag, Province


class CreateSpotForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        choices=[(tag.pk, tag) for tag in Tag.objects.all()]
    )
    province = forms.ChoiceField(
        choices=[(province.pk, province) for province in Province.objects.all()]
    )

    class Meta:
        model = Spot
        fields = ('name', 'province', 'longitude', 'latitude', 'tags', 'photo')

    def clean_province(self):
        prov_pk = self.cleaned_data.get('province')
        if not prov_pk:
            raise ValidationError(f'Please select province')

        return Province.objects.get(pk=int(prov_pk))

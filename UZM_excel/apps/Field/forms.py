from django import forms

from . import models


class AddContractorNNBForm(forms.ModelForm):
    class Meta:
        model = models.ContractorNNB
        fields = '__all__'


class AddContractorDrillForm(forms.ModelForm):
    class Meta:
        model = models.ContractorDrill
        fields = '__all__'


class AddFieldForm(forms.ModelForm):
    class Meta:
        model = models.Field
        fields = '__all__'


class AddPadForm(forms.ModelForm):
    class Meta:
        model = models.Pad
        fields = '__all__'


class AddWellForm(forms.ModelForm):
    class Meta:
        model = models.Well
        fields = '__all__'
        widgets = {
            'latitude': forms.TextInput(),
            'longtitude': forms.TextInput(),
        }


class AddWellboreForm(forms.ModelForm):
    class Meta:
        model = models.Wellbore
        fields = '__all__'
        # exclude = ['wellbore']


class AddSectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        fields = '__all__'


class AddRunForm(forms.ModelForm):
    class Meta:
        model = models.Run
        fields = '__all__'


class AddClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'

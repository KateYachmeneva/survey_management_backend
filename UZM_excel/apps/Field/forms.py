from django.forms import ModelForm, widgets

from . import models


class AddContractorNNBForm(ModelForm):
    class Meta:
        model = models.ContractorNNB
        fields = '__all__'


class AddContractorDrillForm(ModelForm):
    class Meta:
        model = models.ContractorDrill
        fields = '__all__'


class AddFieldForm(ModelForm):
    class Meta:
        model = models.Field
        fields = '__all__'


class AddPadForm(ModelForm):
    class Meta:
        model = models.Pad
        fields = '__all__'


class AddWellForm(ModelForm):
    class Meta:
        model = models.Well
        fields = '__all__'
        widgets = {
            'geomagnetic_date': widgets.DateInput(attrs={'type': 'date'}),
            'T1_start': widgets.DateInput(attrs={'type': 'date'}),
            'T1_end': widgets.DateInput(attrs={'type': 'date'}),
            'T3_start': widgets.DateInput(attrs={'type': 'date'}),
            'T3_end': widgets.DateInput(attrs={'type': 'date'}),
        }


class AddWellboreForm(ModelForm):
    class Meta:
        model = models.Wellbore
        fields = '__all__'
        # exclude = ['wellbore']


class AddSectionForm(ModelForm):
    class Meta:
        model = models.Section
        fields = '__all__'


class AddRunForm(ModelForm):
    class Meta:
        model = models.Run
        fields = '__all__'
        widgets = {
            'start_date': widgets.DateInput(attrs={'type': 'date'}),
            'end_date': widgets.DateInput(attrs={'type': 'date'}),
        }


class AddClientForm(ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'

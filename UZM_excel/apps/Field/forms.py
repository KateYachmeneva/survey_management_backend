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
            'latitude': widgets.TextInput(),
            'longtitude': widgets.TextInput(),
        }

    def transform(self):
        """ [Доп. функционал] [Не используется] Преобразуем значения долготы и широты в десятичные значения """
        if self.data['latitude'] != '' or self.data['longtitude'] != '':  # Ввод КООРДИНАТЫ УСТЬЯ XX YY ZZ
            _mutable = self.data._mutable  # изменяем QueryDicts
            self.data._mutable = True
            try:
                lat_v = [float(idx) for idx in self.data['latitude'].replace(',', '.').split(' ')]
                self.data['latitude'] = (round(float(lat_v[0]) + float(lat_v[1]) / 60 + float(lat_v[2]) / 3600, 3)
                                         if len(lat_v) > 2 else float(lat_v[0]))
            except:
                self.data['latitude'] = ''

            try:
                long_v = [float(idx) for idx in self.data['longtitude'].replace(',', '.').split(' ')]
                self.data['longtitude'] = (round(float(long_v[0]) + float(long_v[1]) / 60 + float(long_v[2]) / 3600, 3)
                                           if len(long_v) > 2 else float(long_v[0]))
            except:
                self.data['longtitude'] = ''

            self.data._mutable = _mutable


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
    """ Форма для создания экземпляра рейса"""
    class Meta:
        model = models.Run
        exclude = ['start_date', 'end_date', 'start_depth', 'end_depth']
        widgets = {
            'start_date': widgets.DateInput(attrs={'type': 'date'}),
            'end_date': widgets.DateInput(attrs={'type': 'date'}),
        }


class AddClientForm(ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'

from django.db import models
from Field.models import Run
""" модель из генератора отчетов зависит от модели из парсера
    нужно либо вынести модель с рейсами в apps  либо перенести ReportIndex
    в parcer
"""
# Create your models here


def get_run_by_id(run_id):
    return Run.objects.get(id=run_id)


class ReportIndex(models.Model):
    """Модель для запоминания полей в report форме"""
    raw_dynamic_depth = models.CharField("Сырые динамические глубина", max_length=10, null=True)
    raw_dynamic_corner = models.CharField("Сырые динамические угол", max_length=10, null=True)
    raw_dynamic_depth_excel = models.CharField("Сырые динамические глубина excel", max_length=10, null=True)
    raw_dynamic_corner_excel = models.CharField("Сырые динамические угол excel", max_length=10, null=True)
    raw_dynamic_list_name = models.CharField("Сырые динамические лист эксель", max_length=10, null=True)
    nnb_static_depth = models.CharField("Статические от ННБ глубина", max_length=10, null=True)
    nnb_static_corner = models.CharField("Статические от ННБ угол", max_length=10, null=True)
    nnb_static_azimut = models.CharField("Статические от ННБ азимут", max_length=10, null=True)
    nnb_static_list_name = models.CharField("Статические от ННБ лист эксель", max_length=10, null=True)
    nnb_dynamic_depth = models.CharField("Динамические от ННБ глубина", max_length=10, null=True)
    nnb_dynamic_corner = models.CharField("Динамические от ННБ угол", max_length=10, null=True)
    nnb_dynamic_azimut = models.CharField("Динамические от ННБ азимут", max_length=10, null=True)
    nnb_dynamic_list_name = models.CharField("Динамические от ННБ лист эксель", max_length=10, null=True)
    igirgi_static_depth = models.CharField("Статические ИГиРГИ глубина", max_length=10, null=True)
    igirgi_static_corner = models.CharField("Статические ИГиРГИ угол", max_length=10, null=True)
    igirgi_static_azimut = models.CharField("Статические ИГиРГИ азимут", max_length=10, null=True)
    igirgi_list_name = models.CharField("Статические ИГиРГИ лист эксель", max_length=10, null=True)
    plan_depth = models.CharField("Плановая траектория глубина", max_length=10, null=True)
    plan_corner = models.CharField("Плановая траектория угол", max_length=10, null=True)
    plan_azimut = models.CharField("Плановая траектория азимут", max_length=10, null=True)
    plan_list_name = models.CharField("Плановая траектория лист эксель", max_length=10, null=True)
    nnb_dynamic_read = models.IntegerField("Считываем динамические данные  от ННБ с этой строки", null=True)
    nnb_static_read = models.IntegerField("Считываем статические данные от ННБ с этой строки", null=True)
    plan_str = models.IntegerField("Считываем данные плана с этой строки",  null=True)
    igirgi_str = models.IntegerField("Считываем данные статика ИГиРГИ с этой строки", null=True)
    raw_str = models.IntegerField("Считываем сырые данные с этой строки",  null=True)

    run = models.OneToOneField(Run, on_delete=models.CASCADE, unique=True)

    class Meta:
        verbose_name = 'Индекс для формы'
        verbose_name_plural = 'Индексы для формы'
        db_table = 'report_index'


class DynamicNNBData(models.Model):
    """Динамические замеры ННБ"""
    depth = models.FloatField('глубина')
    corner = models.FloatField('угол', null=True)
    azimut = models.FloatField('азимут', null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Глубина {self.depth}"

    class Meta:
        ordering = ['depth']
        verbose_name = 'Динамический замер ННБ'
        verbose_name_plural = 'Динамические замеры ННБ'
        db_table = 'meas_dynamic_NNB'


class StaticNNBData(models.Model):
    """Статические замеры ННБ"""
    depth = models.FloatField('глубина')
    corner = models.FloatField('угол', null=True)
    azimut = models.FloatField('азимут', null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)
    comment = models.TextField('комментарий', null=True)

    def __str__(self):
        return f"Глубина {self.depth}"

    class Meta:
        ordering = ['depth']
        verbose_name = 'Статический замер ННБ'
        verbose_name_plural = 'Статические замеры ННБ'
        db_table = 'meas_static_NNB'


class IgirgiStatic(models.Model):
    """Статические замеры ИГИРГИ"""
    depth = models.FloatField('глубина')
    corner = models.FloatField('угол', null=True)
    azimut = models.FloatField('азимут', null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Глубина {self.depth}"

    class Meta:
        ordering = ['depth']
        verbose_name = 'Статический замер ИГИРГИ'
        verbose_name_plural = 'Статические замеры ИГИРГИ'
        db_table = 'meas_static_igirgi'


class IgirgiDynamic(models.Model):
    """Динамические замеры ИГИРГИ"""
    depth = models.FloatField('глубина')
    corner = models.FloatField('угол', null=True)
    azimut = models.FloatField('азимут', null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Глубина {self.depth}"

    class Meta:
        ordering = ['depth']
        verbose_name = 'Динамический замер ИГИРГИ'
        verbose_name_plural = 'Динамические замеры ИГИРГИ'
        db_table = 'meas_dynamic_igirgi'


class Raw(models.Model):
    depth = models.FloatField('глубина')
    corner = models.FloatField('угол', null=True)
    azimut = models.FloatField('азимут', null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Глубина {self.depth}"

    class Meta:
        ordering = ['depth']
        verbose_name = 'Сырой замер'
        verbose_name_plural = 'Сырые замер'
        db_table = 'meas_raw'


class Plan(models.Model):
    """Плановые замеры ННБ"""
    depth = models.FloatField('глубина')
    corner = models.FloatField('угол', null=True)
    azimut = models.FloatField('азимут', null=True)
    plan_version = models.CharField('версия плана', max_length=20, null=True)
    run = models.ForeignKey(Run, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Глубина {self.depth}"

    class Meta:
        ordering = ['depth']
        verbose_name = 'Замер плановой траектории'
        verbose_name_plural = 'Замеры плановой траектории'
        db_table = 'meas_plan'

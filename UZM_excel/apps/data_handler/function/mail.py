from report.function.model_service import last_depth, waste


class BodyData:
    """ Даннные под тело письма get_body - формирует текст письма"""

    def __init__(self, Well: object):
        """Создание тела письма"""
        self.field = Well.pad_name.field.field_name
        self.pad = Well.pad_name.pad_name
        self.well = Well.well_name
        self.depth = last_depth(Well)
        self.departure = ''  # Берём отходы в fetch запросе с сервера функция report из report/views
        self.horiz = ''  # Горизантальные отходы
        self.vert = ''  # вертикальные отходы


class Letter:
    """ Здесь хранятся данные для пиьсма """

    def __init__(self, Well: object):
        """ Передаем экземпляр скважины по которой отправляем отчёт """
        self.data_body = BodyData(Well)
        self.subject = 'test'  # тема письма Будет заполянться в js функции при выдаче файла
        self.mailto = Well.mail_To  # кому отправить
        self.cc = Well.mail_Cc  # копия
        # тело письма
        self.body = 'Это тело письма'  # get_body() - перезаписывает все переменные ниже
        self.comm_waste = "Это строка с общими отходами"
        self.hor_waste = 'Это строка с горизонтальными отходами'
        self.ver_waste = 'Это строка с вертикальными отходами'
        self.endbody = 'Это конец письма'
        self.get_body()

    def get_body(self):
        """Из записанных параметров скважины формируем string"""
        # %0D%0A - enter
        self.body = f"Контроль качетсва инклинометрии во время бурения:%0D%0A %0D%0A" \
                    f"Месторождение: {self.data_body.field}%0D%0A" \
                    f"Куст: {self.data_body.pad}%0D%0A" \
                    f"Скважина: {self.data_body.well}%0D%0A %0D%0A" \
                    f"Общий отход на точку замера {self.data_body.depth} м от траектории подрядчика ННБ составляет "
        self.comm_waste = f" {self.data_body.departure} м;%0D%0A %0D%0A"
        self.hor_waste = f"По горизонтали - {self.data_body.horiz}"
        self.ver_waste = f"; %0D%0A %0D%0AПо вертикали - {self.data_body.vert}"
        self.endbody = f"."

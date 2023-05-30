from report.function.model_service import last_depth


class Letter:
    """ Здесь хранятся данные для пиьсма """
    def __init__(self, Well: object):
        """ Передаем экземпляр скважины по которой отправляем отчёт """
        # data_body = self.BodyData(Well)
        self.subject = 'test'  # тема письма
        self.body = 'Это тело письма'  # data_body.get_body()  # тело письма
        self.mailto = Well.mail_To  # кому отправить
        self.cc = Well.mail_Cc  # копия

    class BodyData:
        """ Даннные под тело письма get_body - формирует текст письма"""
        def __int__(self, Well: object):
            """Создание тела письма"""
            self.field = Well.pad_name.field.field_name
            self.pad = Well.pad_name.pad_name
            self.well = Well.well_name
            self.depth = last_depth(Well)
            self.departure = ''
            self.horiz = ''  # Горизантальные отходы
            self.vert = ''  # вертикальные отходы

    def get_body(self):
        self.body = f"Контроль качетсва инклинометрии во время бурения:\n" \
                    f"Месторождение:{self.BodyData.field}\n" \
                    f"Куст:{self.BodyData.pad}\n" \
                    f"Скважина:{self.BodyData.well}\n\n" \
                    f"Общий отход на точку замера{self.BodyData.depth} м от траектории подрядчика ННБ составляет" \
                    f" {self.BodyData.departure} м;\n\n" \
                    f"По горизонтали - {self.BodyData.horiz};\n\n" \
                    f"По вертикали - {self.BodyData.vert}.\n"
        return self.body


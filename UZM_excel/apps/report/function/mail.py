class Letter:
    subject = ''  # тема письма
    body = ''  # тело письма
    mailto = ''  # кому отправить
    cc = ''  # копия
    bc = ''  # копия

    class BodyData:
        field = ''
        pad = ''
        well = ''
        depth = ''
        departure = ''
        horiz = ''
        vert = ''

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


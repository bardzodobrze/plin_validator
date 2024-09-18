# Utils
from utils.DateFormat import DateFormat

class Movie():

    def __init__(self, id_tienda, fechahora_canje) -> None:
        self.id_tienda = id_tienda
        self.fechahora_canje = fechahora_canje


    def to_JSON(self):
        return {
            'id_tienda': self.id_tienda,
            'fechahora_canje': DateFormat.convert_date(self.fechahora_canje)
        }
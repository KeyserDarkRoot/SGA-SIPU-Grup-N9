class Notificacion: 
    def __init__(self, idNotificacion, mensaje, fecha_envio, estado):
        self.__idNotificacion = idNotificacion
        self.mensaje = mensaje
        self.fecha_envio = fecha_envio
        self.estado = estado

    def enviar(self):
        print(f"Enviando notificación: {self.mensaje}")

    def marcar_leido(self):
        self.estado = "leído"
        print("Notificación marcada como leída")
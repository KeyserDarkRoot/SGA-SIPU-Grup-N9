from abc import ABC, abstractmethod
import sqlite3
from datetime import datetime

# 🔷 Interfaz general de notificación
class INotificacion(ABC):
    @abstractmethod
    def enviar(self, mensaje: str, destinatario: str) -> None:
        pass

    @abstractmethod
    def marcar_leido(self, id_notificacion: int) -> None:
        pass

# 🔷 Notificación por consola (útil para pruebas y desarrollo)
class NotificacionConsola(INotificacion):
    def enviar(self, mensaje: str, destinatario: str) -> None:
        print(f"[Consola] Notificación a {destinatario}: {mensaje}")

    def marcar_leido(self, id_notificacion: int) -> None:
        print(f"[Consola] Notificación {id_notificacion} marcada como leída.")

# 🔷 Notificación persistente en base de datos
class NotificacionDB(INotificacion):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def enviar(self, mensaje: str, destinatario: str) -> None:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notificaciones (mensaje, destinatario, estado, fechaRegistro)
            VALUES (?, ?, 'activo', ?)
        """, (mensaje, destinatario, fecha))
        conn.commit()
        conn.close()
        print(f"[DB] Notificación registrada para {destinatario}: {mensaje}")

    def marcar_leido(self, id_notificacion: int) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE notificaciones SET estado = 'inactivo' WHERE idNotificacion = ?
        """, (id_notificacion,))
        conn.commit()
        conn.close()
        print(f"[DB] Notificación {id_notificacion} marcada como leída.")

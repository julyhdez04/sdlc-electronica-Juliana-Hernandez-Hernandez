VALID_ALERT_STATUSES = {"OPEN", "ACKNOWLEDGED", "RESOLVED"}


class AlertService:
    def __init__(self, repository):
        self.repository = repository

    def register_alert(self, sensor_id: str, level: str, reading_value: float):
        return self.repository.create(sensor_id=sensor_id, level=level, reading_value=reading_value)

    def list_open_alerts(self):
        return self.repository.list_open()

    def change_status(self, alert_id: int, status: str):
        if status not in VALID_ALERT_STATUSES:
            raise ValueError(f"status inválido. Permitidos: {VALID_ALERT_STATUSES}")
        updated = self.repository.update_status(alert_id, status)
        if not updated:
            raise ValueError(f"Alert con id {alert_id} no encontrada")
        return updated

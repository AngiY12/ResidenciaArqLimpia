from dataclasses import dataclass
from datetime import datetime

@dataclass
class AlertaDeCaidaDetectada:
    residente_id: str
    momento: datetime
    aceleracion_registrada: float

@dataclass
class AnomaliaSignosVitalesDetectada:
    residente_id: str
    momento: datetime
    tipo_metrica: str
    valor_anomalo: float
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MetricaVital:
    tipo_metrica: str
    valor: float
    unidad_medida: str
    timestamp: datetime

@dataclass(frozen=True)
class DatosAcelerometro:
    eje_x: float
    eje_y: float
    eje_z: float
    timestamp: datetime

@dataclass(frozen=True)
class UmbralMedico:
    tipo_metrica: str
    valor_minimo: float
    valor_maximo: float
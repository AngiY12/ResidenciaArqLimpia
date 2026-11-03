from typing import Optional
from application.ports import IResidenteMonitorizadoRepository
from domain.entities import ResidenteMonitorizado
from domain.value_objects import UmbralMedico

class SqliteResidenteRepository(IResidenteMonitorizadoRepository):
    def obtener_por_id(self, residente_id: str) -> Optional[ResidenteMonitorizado]:
        # Simulamos una consulta a SQLite (SELECT * FROM residentes...)
        if residente_id == "R-001":
            umbrales = [
                UmbralMedico(tipo_metrica="pulso", valor_minimo=50.0, valor_maximo=100.0),
                UmbralMedico(tipo_metrica="temperatura", valor_minimo=36.0, valor_maximo=37.5)
            ]
            return ResidenteMonitorizado(residente_id=residente_id, umbrales=umbrales)
        return None
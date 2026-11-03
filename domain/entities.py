from typing import List
from domain.value_objects import UmbralMedico, MetricaVital, DatosAcelerometro
from domain.services import EvaluadorSignosVitales, DetectorCaidas

class ResidenteMonitorizado:
    def __init__(self, residente_id: str, umbrales: List[UmbralMedico]):
        self.residente_id = residente_id
        self.umbrales = umbrales
        self.eventos_dominio = []
        self._evaluador_signos = EvaluadorSignosVitales()
        self._detector_caidas = DetectorCaidas()

    def procesar_metrica(self, metrica: MetricaVital):
        evento = self._evaluador_signos.evaluar(self.residente_id, metrica, self.umbrales)
        if evento:
            self.eventos_dominio.append(evento)

    def procesar_caida(self, datos: DatosAcelerometro):
        evento = self._detector_caidas.evaluar(self.residente_id, datos)
        if evento:
            self.eventos_dominio.append(evento)
            
    def obtener_eventos_pendientes(self) -> list:
        eventos = self.eventos_dominio.copy()
        self.eventos_dominio.clear()
        return eventos
from typing import List, Optional
import math
from domain.value_objects import MetricaVital, UmbralMedico, DatosAcelerometro
from domain.events import AnomaliaSignosVitalesDetectada, AlertaDeCaidaDetectada

class EvaluadorSignosVitales:
    def evaluar(self, residente_id: str, metrica: MetricaVital, umbrales: List[UmbralMedico]) -> Optional[AnomaliaSignosVitalesDetectada]:
        for umbral in umbrales:
            if umbral.tipo_metrica == metrica.tipo_metrica:
                if metrica.valor < umbral.valor_minimo or metrica.valor > umbral.valor_maximo:
                    return AnomaliaSignosVitalesDetectada(
                        residente_id=residente_id,
                        momento=metrica.timestamp,
                        tipo_metrica=metrica.tipo_metrica,
                        valor_anomalo=metrica.valor
                    )
        return None

class DetectorCaidas:
    def evaluar(self, residente_id: str, datos: DatosAcelerometro) -> Optional[AlertaDeCaidaDetectada]:
        # Calculamos la magnitud del vector de aceleración
        magnitud = math.sqrt(datos.eje_x**2 + datos.eje_y**2 + datos.eje_z**2)
        UMBRAL_CAIDA_G = 2.5 # Umbral simulado de 2.5 gravedades
        
        if magnitud > UMBRAL_CAIDA_G:
            return AlertaDeCaidaDetectada(
                residente_id=residente_id,
                momento=datos.timestamp,
                aceleracion_registrada=magnitud
            )
        return None
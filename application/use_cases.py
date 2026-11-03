from dataclasses import dataclass
from datetime import datetime
import uuid
from domain.value_objects import MetricaVital, DatosAcelerometro
from domain.events import AnomaliaSignosVitalesDetectada, AlertaDeCaidaDetectada
from application.ports import IResidenteMonitorizadoRepository, IEventOutboxPort, IEventPublisherPort

@dataclass
class EvaluarLecturaCommand:
    """DTO de entrada que trae los datos crudos del sensor"""
    residente_id: str
    tipo_sensor: str
    valor_x: float
    valor_y: float = 0.0
    valor_z: float = 0.0
    unidad: str = ""

@dataclass
class AlertaDetectadaIntegrationEvent:
    """DTO de salida que viajará a la nube mediante mensajería"""
    evento_id: str
    residente_id: str
    tipo_alerta: str
    momento: datetime
    detalles: str

class EvaluarMonitorizacionUseCase:
    def __init__(
        self, 
        repositorio: IResidenteMonitorizadoRepository,
        outbox: IEventOutboxPort,
        publisher: IEventPublisherPort
    ):
        # Inyección de dependencias a través de los puertos
        self.repositorio = repositorio
        self.outbox = outbox
        self.publisher = publisher

    def ejecutar(self, comando: EvaluarLecturaCommand):
        # 1. Recuperar el agregado (Residente y sus umbrales)
        residente = self.repositorio.obtener_por_id(comando.residente_id)
        if not residente:
            print(f"[Log] Residente {comando.residente_id} no encontrado en BD.")
            return

        # 2. Transformar el comando al Lenguaje Ubicuo (Value Objects)
        if comando.tipo_sensor == "acelerometro":
            datos = DatosAcelerometro(
                eje_x=comando.valor_x,
                eje_y=comando.valor_y,
                eje_z=comando.valor_z,
                timestamp=datetime.now()
            )
            residente.procesar_caida(datos)
        else:
            metrica = MetricaVital(
                tipo_metrica=comando.tipo_sensor,
                valor=comando.valor_x,
                unidad_medida=comando.unidad,
                timestamp=datetime.now()
            )
            residente.procesar_metrica(metrica)

        # 3. Capturar eventos de dominio generados si hubo alguna anomalía
        eventos_dominio = residente.obtener_eventos_pendientes()

        # 4. Mapear a eventos de integración y garantizar tolerancia a fallos
        for evento in eventos_dominio:
            evento_integracion = self._mapear_a_integracion(evento)
            
            # Patrón Outbox: guardamos localmente por si no hay internet
            self.outbox.guardar_para_reenvio(evento_integracion)
            
            # Publicamos el evento hacia la nube
            self.publisher.publicar(evento_integracion)

    def _mapear_a_integracion(self, evento) -> AlertaDetectadaIntegrationEvent:
        """Transforma un Domain Event interno a un Integration Event genérico"""
        evento_id = str(uuid.uuid4())
        if isinstance(evento, AlertaDeCaidaDetectada):
            return AlertaDetectadaIntegrationEvent(
                evento_id=evento_id,
                residente_id=evento.residente_id,
                tipo_alerta="CAIDA",
                momento=evento.momento,
                detalles=f"Magnitud: {evento.aceleracion_registrada:.2f}G"
            )
        elif isinstance(evento, AnomaliaSignosVitalesDetectada):
            return AlertaDetectadaIntegrationEvent(
                evento_id=evento_id,
                residente_id=evento.residente_id,
                tipo_alerta=f"ANOMALIA_{evento.tipo_metrica.upper()}",
                momento=evento.momento,
                detalles=f"Valor: {evento.valor_anomalo}"
            )
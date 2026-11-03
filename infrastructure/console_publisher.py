from application.ports import IEventPublisherPort, IEventOutboxPort
from application.use_cases import AlertaDetectadaIntegrationEvent

class ConsoleEventPublisher(IEventPublisherPort):
    def publicar(self, evento: AlertaDetectadaIntegrationEvent) -> None:
        print(f"\n[NUBE - AMQP] 🚨 ¡ALERTA ENVIADA AL SERVICIO CENTRAL!")
        print(f"  -> ID Evento : {evento.evento_id}")
        print(f"  -> Residente : {evento.residente_id}")
        print(f"  -> Tipo      : {evento.tipo_alerta}")
        print(f"  -> Detalles  : {evento.detalles}")
        print("-" * 55)

class LocalEventOutboxAdapter(IEventOutboxPort):
    def __init__(self):
        self.eventos_pendientes = []

    def guardar_para_reenvio(self, evento: AlertaDetectadaIntegrationEvent) -> None:
        self.eventos_pendientes.append(evento)
        print(f"[EDGE - OUTBOX] 💾 Evento '{evento.tipo_alerta}' guardado localmente (tolerancia a fallos).")
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import ResidenteMonitorizado

class IEventPublisherPort(ABC):
    """Puerto de salida para publicar eventos hacia la nube (ej. vía AMQP)"""
    @abstractmethod
    def publicar(self, evento: 'AlertaDetectadaIntegrationEvent') -> None:
        pass

class IEventOutboxPort(ABC):
    """Puerto de salida para guardar eventos temporalmente en caso de fallo de red"""
    @abstractmethod
    def guardar_para_reenvio(self, evento: 'AlertaDetectadaIntegrationEvent') -> None:
        pass

class IResidenteMonitorizadoRepository(ABC):
    """Puerto para obtener la configuración y umbrales del residente"""
    @abstractmethod
    def obtener_por_id(self, residente_id: str) -> Optional[ResidenteMonitorizado]:
        pass
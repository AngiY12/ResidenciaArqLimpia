from infrastructure.sqlite_repository import SqliteResidenteRepository
from infrastructure.console_publisher import ConsoleEventPublisher, LocalEventOutboxAdapter
from application.use_cases import EvaluarMonitorizacionUseCase
from infrastructure.simulador_sensores import SimuladorSensores

def main():
    # 1. Inicializar Adaptadores (Infraestructura)
    repositorio = SqliteResidenteRepository()
    outbox = LocalEventOutboxAdapter()
    publisher = ConsoleEventPublisher()

    # 2. Inyectar dependencias en el Caso de Uso (Aplicación)
    caso_uso = EvaluarMonitorizacionUseCase(
        repositorio=repositorio,
        outbox=outbox,
        publisher=publisher
    )

    # 3. Arrancar el simulador (Edge)
    simulador = SimuladorSensores(caso_uso)
    simulador.iniciar_simulacion(residente_id="R-001", ciclos=3)

if __name__ == "__main__":
    main()
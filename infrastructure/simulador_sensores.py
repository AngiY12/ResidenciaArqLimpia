import random
import time
from application.use_cases import EvaluarMonitorizacionUseCase, EvaluarLecturaCommand

class SimuladorSensores:
    def __init__(self, caso_uso: EvaluarMonitorizacionUseCase):
        self.caso_uso = caso_uso

    def iniciar_simulacion(self, residente_id: str, ciclos: int = 3):
        print(f"=== INICIANDO SIMULACIÓN DE SENSORES PARA {residente_id} ===")
        for i in range(ciclos):
            print(f"\n[Tick {i+1}] Leyendo sensores MQTT...")
            
            # 1. Simular lectura normal de pulso
            pulso = random.uniform(70, 85)
            print(f" Pulso leído: {pulso:.1f} bpm")
            self.caso_uso.ejecutar(EvaluarLecturaCommand(
                residente_id=residente_id, tipo_sensor="pulso", valor_x=pulso, unidad="bpm"
            ))

            # 2. Forzar fiebre en el ciclo 2
            temp = 39.5 if i == 1 else 36.5
            if i == 1: print(f" Temperatura leída (ANÓMALA): {temp:.1f} °C")
            else: print(f" Temperatura leída: {temp:.1f} °C")
            
            self.caso_uso.ejecutar(EvaluarLecturaCommand(
                residente_id=residente_id, tipo_sensor="temperatura", valor_x=temp, unidad="C"
            ))

            # 3. Forzar caída en el último ciclo
            if i == ciclos - 1:
                print(f" ¡Impacto detectado en acelerómetro!")
                # Vector que da una magnitud > 2.5G (ej: sqrt(1.5^2 + 2.0^2 + 1.0^2) = 2.69G)
                self.caso_uso.ejecutar(EvaluarLecturaCommand(
                    residente_id=residente_id, tipo_sensor="acelerometro", 
                    valor_x=1.5, valor_y=2.0, valor_z=1.0, unidad="G"
                ))
            
            time.sleep(2) # Muestreo cada 2 segundos simulado
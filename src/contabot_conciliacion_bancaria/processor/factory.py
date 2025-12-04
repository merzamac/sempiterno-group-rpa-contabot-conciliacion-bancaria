from contabot_conciliacion_bancaria.processor.concrete_strategies import (
    # VentasProcessor,  # type: ignore
    # ComprasProcessor,  # type: ignore
    ConciliacionProcessor,
    # PlanillasProcessor,  # type: ignore
)
from typing import Dict


from contabot_conciliacion_bancaria.processor.strategy import ProcessProcessor
from contabot_conciliacion_bancaria.types import ProcessTypes
from typing import Optional


class ProcessProcessorFactory:
    """Factory para crear los procesadores adecuados"""

    @staticmethod
    def create_processor(
        process_type: str,
    ) -> Optional[ProcessProcessor]:
        processors: Dict[str, ProcessProcessor] = {
            ProcessTypes.CONCILIACION.value: ConciliacionProcessor(),
        }
        return processors.get(process_type.upper())

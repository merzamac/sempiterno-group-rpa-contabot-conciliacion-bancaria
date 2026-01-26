from pathlib import Path

from loguru import logger
from datetime import datetime
from contabot_conciliacion_bancaria import paths
from contabot_conciliacion_bancaria.processor.strategy import ProcessProcessor
from contabot_conciliacion_bancaria.path_reader.infrastructure.get_files_input_to_process import (
    GetInputFilesToProcess,
)

from contabot_conciliacion_bancaria.processor.concrete_strategies import (
    ConciliacionProcessor,
)


def main() -> None:
    processable_input_files = GetInputFilesToProcess.execute(
        input_dir=paths.INPUT_DIR,
        output_dir=paths.OUTPUT_DIR,
        current_date=datetime.now(),
    )

    if not processable_input_files:
        logger.warning("No files to process.")
        return
    for processable_file in processable_input_files:
        with logger.contextualize(
            file_path=processable_file.element_path,
            period=processable_file.get_period_date,
        ):
            save_directory = (
                Path(paths.OUTPUT_DIR).resolve()
                / processable_file.year
                / processable_file.month
                / processable_file.day
            )

            # By default, the bodies of untyped functions are not checked, consider using --check-untyped-defsMypy(annotation-unchecked)

            save_directory.mkdir(parents=True, exist_ok=True)
            # se crea el proceso...
            logger.info("file process...")
            processor: ConciliacionProcessor = ConciliacionProcessor()

            # Ejecutar procesamiento específico
            processor.process(processable_file, save_directory)


if __name__ == "__main__":
    main()

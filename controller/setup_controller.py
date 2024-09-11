from .meta_data_controller import MetadataController
from .columns_controller import ColumnsController
from .unique_values_controller import UniqueValuesController
from model.excel_data_parser import ExcelDataParser
from typing import Callable
from services.task_manager import TaskManager, manage_task
import asyncio

class SetupController:
    def __init__(self, metadata_controller: MetadataController, columns_controller: ColumnsController, unique_values_controller: UniqueValuesController, excel_data_parser: ExcelDataParser, on_file_uploaded_callback: Callable, task_manager: TaskManager):
        self.metadata_controller = metadata_controller
        self.columns_controller = columns_controller
        self.excel_data_parser = excel_data_parser
        self.unique_values_controller = unique_values_controller
        self.on_file_uploaded_callback = on_file_uploaded_callback
        self.task_manager = task_manager

    @manage_task(lambda self: self.task_manager)
    async def process_files_async(self, file_paths: list):
        """파일을 비동기적으로 가져와 메타데이터를 반환하고 집계 데이터를 생성합니다."""
        try:
            # 메타데이터 리셋
            self.metadata_controller.reset_metadata()

            # 파일 경로별로 데이터를 가져오고 메타데이터로 만들기
            for file_path in file_paths:
                file_data = await self.excel_data_parser.get_single_data(file_path)
                self.metadata_controller.generate_metadata(file_path, file_data)
                self.unique_values_controller.initialize_unique_values(file_data)
                await asyncio.sleep(0.1)

            self.columns_controller.initialize_columns(self.metadata_controller)
            self.on_file_uploaded_callback(self.metadata_controller, self.columns_controller, self.unique_values_controller)
        except Exception as ex:
            raise ex

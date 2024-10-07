# controller/edit_controller.py

from model.file_generator import FileGenerator
from model.input_validator import InputValidator
from .columns_controller import ColumnsController
from .meta_data_controller import MetadataController
from .unique_values_controller import UniqueValuesController
from typing import Callable
from services.task_manager import TaskManager, manage_task
from view.components.AlertModal import AlertModal

class EditController:
    def __init__(self, metadata_controller:MetadataController, 
                 columns_controller:ColumnsController, 
                 unique_values_controller:UniqueValuesController, 
                 data_manipulator, 
                 tabs, 
                 options, 
                 on_file_generated_callback: Callable, 
                 task_manager:TaskManager):
        self.metadata_controller = metadata_controller
        self.columns_controller = columns_controller
        self.unique_values_controller = unique_values_controller
        self.data_manipulator = data_manipulator
        self.tabs = tabs
        self.options = options
        self.file_generator = FileGenerator(data_manipulator, self.columns_controller, self.unique_values_controller, tabs)
        self.on_file_generated_callback = on_file_generated_callback
        self.task_manager = task_manager

    def set_options(self):
        """파일 생성에 필요한 옵션을 설정합니다."""
        detail_options = {
            'select_key': self.tabs.isSperate.value,
            'select_unique_column': self.options.sperate_df_option.dropdown.get_selected_value(),
            'sperate_df_values': self.options.sperate_df_option.isSperate.value,
            'save_option': self.options.sperate_df_option.radio_group.value,
            'sort_options': self.options.sort_options.get_sort_options()
        }
        return detail_options

    @manage_task(lambda self: self.task_manager)
    async def create_files(self, alert_modal:AlertModal):
        """파일 생성 작업을 수행합니다."""
        detail_options = self.set_options()  # 옵션 설정

        validate = InputValidator(detail_options, self.unique_values_controller, self.columns_controller).validate()
        
        if validate is None:
            try:
                await self.file_generator.generate(self.metadata_controller, detail_options, alert_modal)
                if not self.task_manager._current_task.cancelled():
                    # Correctly pass both the message and the error argument
                    self.on_file_generated_callback("생성이 완료되었습니다! 다운로드 폴더를 확인해주세요.", error=False)
            except RuntimeError as err:
                self.on_file_generated_callback(f"파일 생성 중 오류가 발생했습니다: {err}", error=True)
        else:
            self.on_file_generated_callback(validate, error=True)

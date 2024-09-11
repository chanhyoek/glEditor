# controller/edit_controller.py

from model.file_generator import FileGenerator
from model.input_validator import InputValidator
from typing import Callable
from services.task_manager import TaskManager, manage_task

class EditController:
    def __init__(self, metadata_controller, data_manipulator, tabs, options, on_file_generated_callback: Callable, task_manager:TaskManager):
        self.metadata_controller = metadata_controller
        self.data_manipulator = data_manipulator
        self.tabs = tabs
        self.options = options
        self.file_generator = FileGenerator(data_manipulator, tabs)
        self.on_file_generated_callback = on_file_generated_callback
        self.task_manager = task_manager

    def set_options(self):
        """파일 생성에 필요한 옵션을 설정합니다."""
        detail_options = {
            'checkboxes': self.options.select_columns_option.checkbox_manager.get_selected_checkbox_labels_as_text(),
            'unique_value_checkboxes': self.options.sperate_df_option.checkbox_manager.get_selected_checkbox_labels_as_text(),
            'select_unique_column': self.options.sperate_df_option.dropdown.value,
            'sperate_df_values': self.options.sperate_df_option.isSperate.value,
            'save_option': self.options.sperate_df_option.radio_group.value,
            'only_selected_df': self.options.selected_df_option.is_selected_df,
            'sort_options': self.options.sort_options.get_sort_options()
        }
        return detail_options

    @manage_task(lambda self: self.task_manager)
    async def create_files(self):
        """파일 생성 작업을 수행합니다."""
        detail_options = self.set_options()  # 옵션 설정

        validate = InputValidator(detail_options).validate()

        if validate is None:
            try:
                selected_columns = list(
                    checkbox.value for checkbox in detail_options['checkboxes'] if isinstance(checkbox, str)
                )
                await self.file_generator.generate(selected_columns, self.metadata_controller, detail_options)
                if not self.task_manager._current_task.cancelled():
                    self.on_file_generated_callback("생성이 완료되었습니다! 다운로드 폴더를 확인해주세요.")
            except RuntimeError as err:
                self.on_file_generated_callback(f"파일 생성 중 오류가 발생했습니다: {err}", error=True)
        else:
            self.on_file_generated_callback(validate, error=True)

import asyncio
import flet as ft
from ...components.AlertModal import AlertModal
from model.input_validator import InputValidator
from model.task_manager import TaskManager
from model.task_manager import manage_task
from ...components.SnackbarNotifier import SnackbarNotifier

class ExcuteBtn:
    def __init__(self, options, file_generator, notifier, meta_data, page, tabs):
        self.options = options
        self.file_generator = file_generator
        self.notifier = notifier
        self.meta_data = meta_data
        self.page = page 
        self.tabs = tabs
        self.task_manager = TaskManager()  # TaskManager 인스턴스 생성
        self.snackbar_notifier = SnackbarNotifier(page)
    
    def build(self):
        self.excute_btn = ft.Container(
            content=ft.ElevatedButton(
                "파일생성하기",
                icon=ft.icons.MERGE_TYPE,
                adaptive=True,
                on_click=lambda e: asyncio.run(self.on_create_files_button_click(e)),  # 비동기 함수 호출
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN,
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            padding=20
        )
        return self.excute_btn
    
    def set_options(self):
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

    async def on_create_files_button_click(self, e):
        detail_options = self.set_options()
        
        # AlertModal 생성
        self.alert_modal = AlertModal(
            self.page,
            content_text = "파일 생성 중입니다. 잠시만 기다려주세요...",
            task_manager=self.task_manager,
            snackbar_notifier=self.snackbar_notifier
        )
        
        self.alert_modal.show()  # AlertModal 표시

        # 작업 실행
        asyncio.run(self.task_manager.run_task(
            self.create_files(e, detail_options),  
            on_complete=self.alert_modal.close,  # 작업 완료 시 모달 닫기
            on_error=lambda msg: self.snackbar_notifier.show_snackbar(f"오류가 발생했습니다: {msg}", error=True)  # 오류 발생 시 알림
        ))

    @manage_task(lambda self: self.task_manager)
    async def create_files(self, e, detail_options):
        validate = InputValidator(detail_options).validate()

        if validate is None:
            try:
                selected_columns = list(checkbox.value for checkbox in detail_options['checkboxes'] if isinstance(checkbox, ft.Text))
                await self.file_generator.generate(selected_columns, self.meta_data, detail_options)
                if not self.task_manager._current_task.cancelled(): 
                    self.notifier.show_snackbar("생성이 완료되었습니다! 다운로드 폴더를 확인해주세요.")
            except RuntimeError as err:
                self.notifier.show_snackbar(f"파일 생성 중 오류가 발생했습니다: {err}", error=True)
            finally:
                self.alert_modal.close()  
        else:
            self.notifier.show_snackbar(validate, error=True)

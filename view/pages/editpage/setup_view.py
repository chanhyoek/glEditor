# view/setup_view.py

import flet as ft
from model.meta_data_model import MetadataModel
from model.excel_data_parser import ExcelDataParser
from model.columns_model import Columns
from model.unique_values_model import UniqueValues

from controller.columns_controller import ColumnsController
from controller.unique_values_controller import UniqueValuesController
from controller.setup_controller import SetupController
from controller.meta_data_controller import MetadataController
from ...components.SnackbarNotifier import SnackbarNotifier
from ...components.AlertModal import AlertModal
from services.task_manager import TaskManager
import os

class SetupView:
    def __init__(self, page: ft.Page, task_manager:TaskManager ,on_file_uploaded_callback):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)

        if self.file_picker not in self.page.overlay:
            self.page.overlay.append(self.file_picker)

        self.on_file_uploaded_callback = on_file_uploaded_callback
        self.snackbar_notifier = SnackbarNotifier(page)
        self.metadata_model = MetadataModel()
        self.columns_model = Columns()
        self.unique_values_model = UniqueValues()

        self.excel_data_parser = ExcelDataParser()
        self.task_manager = task_manager

        self.metadata_controller = MetadataController(model=self.metadata_model)
        self.columns_controller = ColumnsController(columns=self.columns_model)
        self.unique_values_controller = UniqueValuesController(unique_values=self.unique_values_model)

        self.setup_controller = SetupController(
            metadata_controller=self.metadata_controller,
            unique_values_controller= self.unique_values_controller,
            columns_controller=self.columns_controller,
            excel_data_parser=self.excel_data_parser,
            on_file_uploaded_callback=self.on_file_uploaded_callback,
            task_manager=self.task_manager
        )


    def build(self):
        """UI를 생성합니다."""
        self.upload_btn = ft.ElevatedButton(
            "파일 업로드",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(allow_multiple=True, initial_directory=os.path.expanduser("~/Downloads")),
            adaptive=True,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE,
                shape=ft.RoundedRectangleBorder(radius=10),
            )
        )

        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("데이터 편집하기", size=32, weight="bold", color=ft.colors.BLUE),
                    ft.Text("여러 파일, 여러 시트의 데이터를 취합하여 원하는 방식대로 편집합니다.", size=16),
                    ft.Row(
                        controls=[
                            ft.Text("지원하는 파일양식: csv, xls, xlsx, xlsb"),
                            self.upload_btn
                        ],
                        spacing=200
                    )
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.only(left=20, right=20, top=20)
        )

        self.view = ft.Container(
            ft.Row(
                controls=[
                    header,
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            ),
            height=180,
            width=800,
            expand=0
        )
        return self.view

    def create_modal(self):
        """모달 다이얼로그를 생성합니다."""
        self.alert_modal = AlertModal(
            self.page,
            content_text="파일 첨부 중 입니다. 잠시만 기다려주세요...",
            task_manager=self.task_manager,
            snackbar_notifier=self.snackbar_notifier
        )
        self.alert_modal.show()

    async def file_picker_result(self, e):
        """파일 선택 결과를 처리합니다."""
        self.create_modal()  # 파일 업로드 모달을 표시

        # 파일 경로 목록 생성
        file_paths = [f.path for f in e.files]

        # 파일 처리를 비동기적으로 실행
        try:
            print(f"Processing files: {file_paths}")  # 디버그 프린트 문
            await self.setup_controller.process_files_async(file_paths)
        # except Exception as ex:
        #     # 오류 발생 시 스낵바를 띄웁니다.
        #     print(f"Error occurred during file processing: {str(ex)}")  # 디버그 프린트 문
        #     self.snackbar_notifier.show_snackbar(f"오류가 발생했습니다: {str(ex)}", error=True)
        finally:
            # 작업 완료 후 모달 닫기
            self.alert_modal.close()
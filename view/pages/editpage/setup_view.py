import flet as ft
from model.excel_data_parser import ExcelDataParser
from model.meta_data_manager import MetadataManager
from ...components.SnackbarNotifier import SnackbarNotifier
from ...components.AlertModal import AlertModal
from model.task_manager import TaskManager
from model.task_manager import manage_task
import os
import asyncio

class SetupView:
    def __init__(self, page: ft.Page, on_file_uploaded_callback):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)

        if self.file_picker not in self.page.overlay:
            self.page.overlay.append(self.file_picker)

        self.on_file_uploaded_callback = on_file_uploaded_callback
        self.snackbar_notifier = SnackbarNotifier(page)
        self.metadata_manager = MetadataManager()
        self.excel_data_parser = ExcelDataParser()
        self.task_manager = TaskManager()


    def build(self):
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
                        controls = [
                            ft.Text("지원하는 파일양식: csv, xls, xlsx, xlsb"),
                            self.upload_btn
                        ],
                        spacing = 200
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
        # 모달 다이얼로그 생성
        self.alert_modal = AlertModal(
            self.page,
            content_text="파일 첨부 중 입니다. 잠시만 기다려주세요...",
            task_manager=self.task_manager,
            snackbar_notifier = self.snackbar_notifier
        )

        # 파일 업로드 모달을 띄우기
        self.alert_modal.show()

    async def file_picker_result(self, e):

        self.create_modal()

        # 파일 처리를 비동기적으로 실행
        asyncio.create_task(self.process_files_async(e))
    @manage_task(lambda self: self.task_manager)
    async def process_files_async(self, e):
        """파일을 비동기적으로 가져와 메타데이터를 반환합니다."""
        try:
            #메타데이터 리셋
            self.metadata_manager.reset_metadata()

            #파일 경로별로 데이터를 가져오고 메타데이터로 만들기
            file_paths = [f.path for f in e.files]
            for file_path in file_paths:
                file_data = await self.excel_data_parser.get_single_data(file_path)
                self.metadata_manager.generate_metadata(file_path, file_data)
                await asyncio.sleep(0.1)  

            # 파일 업로드가 성공적으로 완료된 경우 콜백 호출
            self.on_file_uploaded_callback(self.metadata_manager)
        except Exception as ex:
            # 오류 발생 시 스낵바를 띄우기
            print(f"{str(ex)}")
            self.snackbar_notifier.show_snackbar(f"오류가 발생했습니다: {str(ex)}", error=True)
        finally:
            # 파일 업로드 완료 후 모달 닫기
            self.alert_modal.close()

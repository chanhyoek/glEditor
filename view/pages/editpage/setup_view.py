import flet as ft
from model.excel_data_parser import ExcelDataParser
from ...components.SnackbarNotifier import SnackbarNotifier
from ...components.AlertModal import AlertModal
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
        self.operation_cancelled = False

        # 모달 다이얼로그 생성
        self.alert_modal = AlertModal(
            page,
            content=[
                ft.ProgressRing(), 
                ft.Text("파일 첨부 중입니다. 잠시만 기다려주세요...", size=15),
            ],
            actions=[
                ft.TextButton(
                    "취소",
                    on_click=self.cancel_operation
                )
            ],
            on_cancel=self.cancel_operation
        )
    
    def build(self):
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("데이터 편집하기", size=32, weight="bold", color=ft.colors.BLUE),
                    ft.Text("여러 파일, 여러 시트의 데이터를 취합하여 원하는 방식대로 편집합니다.", size=16)
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.only(left=20, top=20)
        )
        
        file_upload_button = ft.Container(
            content=ft.ElevatedButton(
                "파일 업로드",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: self.file_picker.pick_files(allow_multiple=True, initial_directory=os.path.expanduser("~/Downloads")),
                adaptive=True,
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.BLUE,
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            padding=ft.padding.only(left=20)
        )
        
        self.view = ft.Container(
            ft.Row(
                controls=[
                    header,
                    file_upload_button
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            ),
            height=270,
            width=800,
            expand=0
        )    
        return self.view
    
    async def file_picker_result(self, e):
        # 작업이 취소되었는지 초기화
        self.operation_cancelled = False

        # 파일 업로드 모달을 띄우기
        self.alert_modal.show()

        # 파일 처리를 비동기적으로 실행
        asyncio.create_task(self.process_files_async(e))

    async def process_files_async(self, e):
        try:
            # 파일 경로 목록 가져오기
            file_paths = [f.path for f in e.files]
            print(file_paths)

            # 데이터 처리 중에 취소되었는지 확인
            file_data = await self.process_files(file_paths)

            if not self.operation_cancelled:
                self.on_file_uploaded_callback(file_data)
        except Exception as ex:
            # 오류 발생 시 스낵바를 띄우기
            self.snackbar_notifier.show_snackbar(f"오류가 발생했습니다: {str(ex)}", error=True)
        finally:
            # 파일 업로드 완료 후 모달 닫기
            self.alert_modal.close()

    async def process_files(self, file_paths):
        # 파일을 처리하는 동안 주기적으로 작업이 취소되었는지 확인
        file_data = {}
        for file_path in file_paths:
            if self.operation_cancelled:
                break
            single_data = await ExcelDataParser().get_single_data(file_path)
            file_data.update(single_data)
            await asyncio.sleep(0.1)  # 작업 중간에 취소를 확인할 수 있도록 약간의 지연 추가
        return file_data

    def cancel_operation(self, e=None):  # e 매개변수 추가
        # 작업 취소 플래그를 설정
        self.operation_cancelled = True
        self.alert_modal.close()
        self.snackbar_notifier.show_snackbar("작업이 취소되었습니다.", error=True)

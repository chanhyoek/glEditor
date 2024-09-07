import flet as ft
from typing import List
from model.task_manager import TaskManager
from .SnackbarNotifier import SnackbarNotifier


class AlertModal:
    def __init__(self, page: ft.Page, content_text: str = None, task_manager: TaskManager = None, snackbar_notifier: SnackbarNotifier = None):
        self.page = page
        self.task_manager = task_manager 
        self.snackbar_notifier = snackbar_notifier
        self.text_control = ft.Text(content_text, size=15)  # 텍스트 컨트롤 객체 저장


        # Content 동적으로 생성
        self.content = [
            ft.ProgressRing(),  # 애니메이션으로 로딩 표시
            self.text_control # 동적으로 전달받은 텍스트 사용
        ]

        self.modal_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                controls=self.content,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=300,
                height=100,
                spacing= 20
            ),
            actions= [
                ft.TextButton(
                    "취소",
                    on_click=self.cancel_operation  # 기본 취소 작업 연결
                )
            ],
        )

    def show(self):
        """모달을 표시합니다."""
        self.page.dialog = self.modal_dialog
        self.modal_dialog.open = True
        self.page.update()

    def close(self):
        """모달을 닫습니다."""
        self.modal_dialog.open = False
        self.page.update()

    def update_content_text(self, new_text: str):
        """모달의 텍스트 내용을 업데이트합니다."""
        self.text_control.value = new_text  # 텍스트 컨트롤의 내용을 변경
        self.page.update()  # 페이지 업데이트로 변경 사항 반영

    def cancel_operation(self, e=None):
        """모든 모달에서 호출되는 공통 취소 작업 처리 함수."""
        self.update_content_text("작업을 취소 중입니다.")
        
        if self.task_manager:
            self.task_manager.cancel_current_task()  # 작업 취소

        # 사용자에게 취소 알림
        self.snackbar_notifier.show_snackbar("작업이 취소되었습니다.", error=True)
        self.close()  # 모달 닫기
import flet as ft
from typing import List, Callable

class AlertModal:
    def __init__(self, page: ft.Page, content: List[ft.Control], actions: List[ft.Control] = None, on_cancel: Callable = None, width=300, height=100):
        self.page = page
        self.on_cancel = on_cancel
        self.modal_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                controls=content,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width= width,
                height= height
            ),
            actions=actions or [],
        )

    def show(self):
        self.page.dialog = self.modal_dialog
        self.modal_dialog.open = True
        self.page.update()

    def close(self):
        self.modal_dialog.open = False
        self.page.update()

    def cancel_operation(self, e):
        if self.on_cancel:
            self.on_cancel()  # 취소 버튼이 눌렸을 때 실행할 콜백 호출
        self.close()

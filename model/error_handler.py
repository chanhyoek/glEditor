import flet as ft
from view.components.SnackbarNotifier import SnackbarNotifier

class ErrorHandler:
    def __init__(self, page):
        self.page = page
        self.snackbar_notifier = SnackbarNotifier(page)  # SnackbarNotifier 인스턴스 생성

    def show_error(self, message):
        """오류 메시지를 스낵바로 표시합니다."""
        self.snackbar_notifier.show_snackbar(message, error=True)  # 오류 메시지를 스낵바로 표시

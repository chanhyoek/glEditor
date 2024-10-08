import flet as ft
from view.GL_editor import GLEditor
from services.task_manager import TaskManager
from controller.edit_controller import EditController
from controller.setup_controller import SetupController

def main(page: ft.Page):
    print("xcelator를 시작합니다.")

    task_manager = TaskManager()

    page.title = "Xcelator"
    page.window.icon = ft.icons.SPEED_SHARP
    page.theme_mode = ft.ThemeMode.DARK  # 기본값을 라이트 모드로 설정
    app = GLEditor(page, task_manager)
    app.build()
    app.initialize()

if __name__ == "__main__":
    print("Executing as the main script")
    ft.app(target=main)
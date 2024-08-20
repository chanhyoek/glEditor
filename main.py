import flet as ft
from view.GL_editor import GLEditor

def main(page: ft.Page):
    print("Main function called")
    page.title = "GL EDITOR"
    page.theme_mode = ft.ThemeMode.DARK  # 다크 테마 적용
    app = GLEditor(page)
    app.build()
    app.initialize()

if __name__ == "__main__":
    print("Executing as the main script")
    ft.app(target=main)

        

import flet as ft

class SnackbarNotifier:
    def __init__(self, page):
        self.page = page

    def show_snackbar(self, message, error=False):
        def close_snackbar(e):
            self.page.snack_bar.open = False
            self.page.update()

        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE if error else ft.colors.GREEN),
            bgcolor=ft.colors.RED if error else ft.colors.WHITE,
            # action=ft.Text("확인", on_click=close_snackbar)
        )
        self.page.snack_bar.open = True
        self.page.update()

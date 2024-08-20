import flet as ft

class HomePage:
    def __init__(self, app_layout, page):
        self.page = page
        self.app_layout = app_layout

    def create_card(self, title, explain, button_title, route):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(title, size=24, weight="bold"),
                            subtitle=ft.Text(explain)
                        ),
                        ft.Row(
                            [ft.TextButton(button_title, on_click=lambda _: self.page.go(route))],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10
            ),
            width=800,
            height=180,
            margin=5
        )

    def build(self):
        notice_explanation = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("HomePage", size=24, weight="bold"),
                    ft.Text(" "),
                    ft.Text("주의사항", size=16),
                    ft.Text("1. 편집하고자 하는 엑셀파일의 첫번째 행에 해더가 위치해야 합니다."),
                    ft.Text("2. 엑셀 내부에 수식이 포함된 경우 수식이 지워집니다.")
                ],
            ),
            padding=10,
        )

        cards = ft.Container(
            content=ft.Row(
                expand=True,
                controls=[
                    self.create_card("데이터 편집하기", "데이터를 원하는 형태로 편집하세요", "GO!", "/merge"),
                    # self.create_card("추출하기", "여러 데이터에서 원하는 부분만 편집하여 새로운 파일을 만듭니다", "추출하기", "/extract")
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=10,
            expand=True
        )

        self.view = ft.Container(
            content=ft.Column([
                ft.Row([notice_explanation]),
                ft.Container(
                    bgcolor=ft.colors.WHITE54,
                    border_radius=ft.border_radius.all(30),
                    alignment=ft.alignment.center_right,
                    width=800,
                    height=1,
                ),
                ft.Row([cards]),
            ]),
            expand=True,
            margin=ft.margin.all(10),
        )
        return self.view

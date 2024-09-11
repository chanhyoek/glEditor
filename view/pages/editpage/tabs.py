import flet as ft
import asyncio

class Tabs:
    def __init__(self, page, metadata_controller, window_width):
        self.page = page
        self.metadata_controller = metadata_controller
        self.tabs_button = ft.Row(scroll=ft.ScrollMode.ALWAYS, width=window_width)
        self.tabs_content = ft.Container()
        self.active_index = 0
        self.window_width = window_width

        # 창 크기 변경 이벤트 핸들러 등록
        self.page.on_resize = self.on_resize

    def build(self):
        self.main_column = ft.Column(
            controls=[
                self.tabs_button,
                self.tabs_content
            ],
            expand=True,
            spacing=5,
            scroll=ft.ScrollMode.AUTO,
            width=self.window_width
        )

        return ft.Container(
            content=self.main_column,
            padding=ft.padding.only(left=20, right=30),
            margin=ft.margin.only(bottom=20)
        )

    def create_tabs(self):
        """tabs 버튼을 생성합니다."""
        keys = self.metadata_controller.model.metadata.keys()
        self.tabs_button.controls.clear()
        for index, key in enumerate(keys):
            button = ft.FilledButton(
                content=ft.Text(key),
                on_click=lambda e, idx=index: self.switch_tab(idx),
                style=ft.ButtonStyle(
                    padding=10,
                    bgcolor=ft.colors.LIGHT_BLUE_50 if index == self.active_index else None
                )
            )
            self.tabs_button.controls.append(button)
        self.switch_tab(self.active_index)
        self.tabs_button.update()

    def switch_tab(self, index):
        """tab을 전환합니다."""
        self.active_index = index
        keys = list(self.metadata_controller.model.metadata.keys())  # MetadataController를 통해 키를 가져옴
        key = keys[index]
        self.load_data(key)

    def load_data(self, key):
        """데이터를 로드하고 UI를 업데이트합니다."""
        data = self.metadata_controller.get_first_5_rows(key)  # MetadataController를 통해 데이터 로드
        self.tabs_content.content = self.create_data_table(data)
        self.update_tab_buttons()
        self.tabs_content.update()

    def update_tab_buttons(self):
        for idx, button in enumerate(self.tabs_button.controls):
            button.style.bgcolor = ft.colors.LIGHT_BLUE_50 if idx == self.active_index else None
        if self.tabs_button.page:
            self.tabs_button.update()

    def create_data_table(self, df):
        """DataFrame을 데이터 테이블로 변환합니다."""
        return ft.Row([
            ft.DataTable(
                columns=[ft.DataColumn(ft.Text(col)) for col in df.columns],
                rows=[
                    ft.DataRow(
                        cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]
                    ) for row in df.head(5).values
                ]
            )
        ],
            expand=True,
            width=self.window_width,
            scroll=ft.ScrollMode.ALWAYS)

    def on_resize(self, e):
        """창 크기 변경 시 호출되는 이벤트 핸들러."""
        self.window_width = self.page.window_width
        self.main_column.width = self.window_width
        self.page.update()  # UI 업데이트

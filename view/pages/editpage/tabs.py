import flet as ft
import asyncio

class Tabs:
    def __init__(self, page, file_data):
        self.page = page
        self.file_data = file_data
        self.tabs_button = ft.Row(scroll=ft.ScrollMode.ALWAYS,width=1000)
        self.tabs_content = ft.Container()
        self.active_index = 0

    def build(self):
        return ft.Container (
            content =  ft.Column(
                controls=[
                    self.tabs_button,
                    self.tabs_content
                ],
                expand=True,
                spacing=5,
                scroll=ft.ScrollMode.AUTO,
                width=1000
            ),
            padding= ft.padding.only(left=20),
            margin= ft.margin.only(bottom=50)
        ) 
       
    def create_tabs(self):
        keys = list(self.file_data.keys())
        self.tabs_button.controls.clear()  # 불필요한 버튼 추가 방지
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
        self.active_index = index
        key = list(self.file_data.keys())[index]
        self.load_data_async(key)
    
    def load_data_async(self, key):
        """데이터를 로드하고 UI를 업데이트합니다."""
        data = self.load_data(key)  # 데이터 로드
        self.tabs_content.content = self.create_data_table(data)
        self.update_tab_buttons()
        self.tabs_content.update()
    
    def load_data(self, key):
        """동기적으로 데이터를 로드하는 함수입니다."""
        # 데이터가 이미 메모리에 로드되어 있으므로 비동기 작업이 필요하지 않습니다.
        return self.file_data[key]

    def update_tab_buttons(self):
        for idx, button in enumerate(self.tabs_button.controls):
            button.style.bgcolor = ft.colors.LIGHT_BLUE_50 if idx == self.active_index else None
        # self.tabs_button이 이미 페이지에 추가된 이후에만 update를 호출
        if self.tabs_button.page:
            self.tabs_button.update()
    
    def create_data_table(self, df):
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
                width=1000,
                scroll=ft.ScrollMode.ALWAYS)

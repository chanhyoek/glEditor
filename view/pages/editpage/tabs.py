import flet as ft

class Tabs:
    def __init__(self, page, file_data):
        self.page = page
        self.file_data = file_data
        self.tabs_button = ft.Row(scroll=ft.ScrollMode.ALWAYS,width=2000)
        self.tabs_content = ft.Container()
        self.active_index = 0

    def build(self):
        # create_tabs를 호출하기 전에 이 컨트롤이 페이지에 추가되어야 함
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
        self.tabs_content.content = self.create_data_table(self.file_data[key])
        self.update_tab_buttons()
        self.tabs_content.update()

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
        

import flet as ft

class SperateDFView:
    def __init__(self, page, checkbox_manager):
        self.page = page
        self.checkbox_manager = checkbox_manager
        self.selected_column = None
        self.controller = None  
        
        # Dropdown 초기화
        self.dropdown = ft.Dropdown(
            options=[],  # 나중에 컨트롤러에서 설정
            width=800,
            on_change=lambda e: self.on_dropdown_change(e.control.value)
        )

        # 기타 UI 요소 초기화
        self.unique_value_checkboxes = ft.Row(controls=[], scroll=ft.ScrollMode.AUTO)
        self.search_field = ft.TextField(label="찾고 싶은 항목을 입력하세요", width=450)

    def build(self):
        self.extension_panel = ft.ExpansionPanel(
            header=ft.Checkbox(
                label="고유값으로 데이터 분리하기: 데이터를 특정열의 고유 값을 기준으로 분리합니다.",
                value=False,
                on_change=self.on_checkbox_change
            ),
            content=ft.Column(
                controls=[
                    ft.Text("Hi!"),
                    self.create_dropdown_row(),
                    self.create_search_unique_value_checkboxes(),
                    self.unique_value_checkboxes,
                    self.select_save_options(),
                ]
            )
        )
        

        self.container = ft.Container(
            content=ft.Column([
                ft.ExpansionPanelList(
                    controls=[self.extension_panel]
                )
            ])
        )

        return self.container
    
    def create_dropdown_row(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.dropdown
                ]
            )
        )

    def update_dropdown_options(self, options):
        self.dropdown.options = options
        self.dropdown.update()

    def on_checkbox_change(self, value):
        self.extension_panel.expanded = value
        self.extension_panel.update()

    def on_dropdown_change(self, value):
        self.selected_column = value
        if self.controller:
            self.controller.handle_dropdown_change(value)

    def create_search_unique_value_checkboxes(self):
        return ft.Row(
            controls=[
                self.search_field,
                ft.CupertinoButton(content=ft.Text("Search"), on_click=self.on_search_click),
                ft.CupertinoButton(text="전체선택", on_click=lambda e: self.checkbox_manager.select_all_checkboxes(), icon=ft.icons.CHECK_ROUNDED),
                ft.CupertinoButton(text="전체해제", on_click=lambda e: self.checkbox_manager.unselect_all_checkboxes(), icon=ft.icons.TAB_UNSELECTED_ROUNDED),
            ]
        )

    def on_search_click(self, e):
        # 검색어 처리도 컨트롤러에서 담당할 수 있음
        pass

    def select_save_options(self):
        self.radio_group = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="one_file", label="한 파일에 여러 시트로 만들기"),
                    ft.Radio(value="multi_files", label="여러 파일로 만들기"),
                ]
            )
        )
        
        return ft.Row(
            controls=[
                ft.Text("저장 옵션"),
                self.radio_group
            ]
        )

    def update_checkboxes_with_unique_values(self, split_data):
        # split_data를 기반으로 체크박스 업데이트 로직을 추가합니다.
        checkboxes = []
        for key in split_data:
            checkboxes.append(
                ft.Checkbox(label=key, value=False)
            )
        self.unique_value_checkboxes.controls = checkboxes
        self.unique_value_checkboxes.update()
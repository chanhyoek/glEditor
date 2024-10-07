import flet as ft
from view.components.selected_items_display import SelectedItemsDisplay
from view.components.SearchField import SearchField
from view.components.checkboxes_factory import create_checkbox_manager
from model.eventHandler import Event
from controller.meta_data_controller import MetadataController

class Tabs:
    def __init__(self, 
                 page, 
                 metadata_controller:MetadataController,
                 error_handler):
        self.page = page
        self.metadata_controller = metadata_controller
        self.tabs_button = ft.Row(scroll=ft.ScrollMode.ALWAYS)
        self.tabs_content = ft.Container()
        self.active_index = 0
        self.error_handler = error_handler

        # 선택된 항목을 표시하는 컴포넌트
        self.selected_items_display = SelectedItemsDisplay(
            page=self.page,
            controller=self.metadata_controller,
            height=20, 
            mode='keys',
        )

        # 고유 값 체크박스 컨테이너s
        self.keys_checkboxes = ft.Column(
            controls=[], scroll=ft.ScrollMode.AUTO
        )

        # SearchField 컴포넌트 초기화
        self.search_component = SearchField(
            on_search=self.search_unique_value,
            on_select_all=lambda e: self.select_all_keys(),
            on_unselect_all=lambda e:self.unselect_all_keys(),
            width=400,
        )

        # 팩토리 메서드를 통해 적절한 CheckboxManager 생성
        self.checkbox_manager = create_checkbox_manager(
            mode='keys',
            page=self.page,
            container=self.keys_checkboxes,
            error_handler=error_handler,
            controller=metadata_controller
        )
        # 옵저버 등록
        metadata_controller.add_observer(self.checkbox_manager)
        metadata_controller.add_observer(self.selected_items_display)

        self.isSperate = ft.Checkbox(
            label="특정 시트만 편집하기: 원하는 데이터만 선택하여 편집합니다.",
            value=False,
            on_change=lambda e: self.on_checkbox_change(e.control.value),
        )

    def on_checkbox_change(self, value):
        """체크박스 변경 시 콘텐츠의 가시성을 업데이트합니다."""
        
        if self.content.visible == False:
            self.metadata_controller.select_all_keys()
        
        self.content.visible = value
        self.page.update()

    def build(self):
        self.main_column = ft.Column(
            controls=[
                self.tabs_button,
                self.tabs_content,
                self.create_extension_panel(),
                self.create_content(),
                
            ],
            expand=True,
            spacing=5,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.Container(
            content=self.main_column,
            padding=ft.padding.only(left=20, right=20),
            margin=ft.margin.only(bottom=20)
        )
    
    def create_extension_panel(self):
        """check박스로 구성된 extension panel을 만듭니다."""
        self.extension_panel = ft.Container(content=self.isSperate)
        return self.extension_panel

    def create_content(self):
        """UI 콘텐츠를 생성하고 빌드합니다."""

        self.checkbox_manager.build()

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.search_component.build(),  # SearchField 컴포넌트
                    self.selected_items_display.build(),  # 선택된 항목 표시 컴포넌트
                    ft.Container(self.keys_checkboxes),  # 빌드된 CheckboxManager 추가
                ]
            ),
            visible=False,
        )
        return self.content

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
                    bgcolor=ft.colors.LIGHT_BLUE_700 if index == self.active_index else ft.colors.LIGHT_BLUE_400
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
            button.style.bgcolor = ft.colors.LIGHT_BLUE_700 if idx == self.active_index else ft.colors.LIGHT_BLUE_400
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
            scroll=ft.ScrollMode.ALWAYS)

    def search_unique_value(self, search_term:str) -> None:
        """검색어로 체크박스 필터링하고 UI를 업데이트합니다."""
        self.metadata_controller.search_value(search_term)

    def select_all_keys(self):
        """전체선택"""
        self.metadata_controller.select_all_keys()

    def unselect_all_keys(self):
        """전체선택 해제"""
        self.metadata_controller.unselect_all_keys()

    def update_checkboxes_with_unique_values(self, selected_column):
        """선택된 열에 대한 고유 값을 사용하여 체크박스를 업데이트합니다."""
        self.checkbox_manager.create_checkboxes_container(column_name=selected_column, batch_size=50)

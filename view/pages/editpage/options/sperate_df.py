import flet as ft
from ....components.checkboxes_factory import create_checkbox_manager
from ....components.SearchField import SearchField
from ....components.selected_items_display import SelectedItemsDisplay
from ....components.selectable_dropdown import SelectableDropdown
from controller.columns_controller import ColumnsController
from model.eventHandler import Event

class SperateDFOption:
    def __init__(self, page, columns_controller, unique_values_controller, error_handler, window_width):
        self.page = page
        self.columns_controller = columns_controller
        self.unique_value_controller = unique_values_controller

        # 선택된 항목을 표시하는 컴포넌트
        self.selected_items_display = SelectedItemsDisplay(
            controller=self.columns_controller,
            width=window_width, height=20, mode='unique_values'
        )

        # 고유 값 체크박스 컨테이너
        self.unique_value_checkboxes = ft.Column(
            controls=[], visible=False, scroll=ft.ScrollMode.AUTO, width=window_width
        )

        # 팩토리 메서드를 통해 적절한 CheckboxManager 생성
        self.checkbox_manager = create_checkbox_manager(
            mode='unique_values',
            page=self.page,
            container=self.unique_value_checkboxes,
            error_handler=error_handler,
            controller=unique_values_controller
        )

        # SelectableDropdown 인스턴스 생성
        self.dropdown = SelectableDropdown(controller=self.columns_controller)
        self.dropdown.set_on_change(self.on_column_selection_changed)  # 외부 핸들러 연결

        self.isSperate = ft.Checkbox(
            label="데이터 필터링: 특정 열의 데이터를 가져와 원하는 값만 선택합니다.",
            value=False,
            on_change=lambda e: self.on_checkbox_change(e.control.value),
        )

        self.radio_group = ft.RadioGroup(content=None)

        # SearchField 컴포넌트 초기화
        self.search_component = SearchField(
            on_search=self.search_unique_value,
            on_select_all=self.select_all_columns,
            on_unselect_all=self.unselect_all_columns,
            width=400,
        )

        self.page.on_resize = self.on_resize

        # 리스너 연결
        # self.checkbox_manager.add_event_listener(self.handle_checkbox_change)
        # self.columns_controller.add_listener(self.update_selected_list_display)

    def build(self):
        
        self.checkbox_manager.build()
        
        self.container = ft.Container(
            content=ft.Column(
                controls=[self.create_extension_panel(), self.create_content()]
            )
        )

        self.page.add(self.container)
        self.dropdown.update_dropdown()
        self.update_selected_list_display()

        return self.container

    def on_checkbox_change(self, value):
        """체크박스 변경 시 콘텐츠의 가시성을 업데이트합니다."""
        self.content.visible = value
        self.page.update()

    def create_extension_panel(self):
        """check박스로 구성된 extension panel을 만듭니다."""
        self.extension_panel = ft.Container(content=self.isSperate)
        return self.extension_panel

    def create_content(self):
        """UI 콘텐츠를 생성하고 빌드합니다."""
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([ft.Text("열 선택"), self.dropdown]),
                    self.search_component.build(),  # SearchField 컴포넌트
                    self.selected_items_display,  # 선택된 항목 표시 컴포넌트
                    ft.Container(self.unique_value_checkboxes),  # 빌드된 CheckboxManager 추가
                    self.select_save_options(),
                ]
            ),
            visible=False,
        )
        return self.content

    def on_column_selection_changed(self, e):
        """열 선택이 변경되었을 때 CheckboxManager 업데이트."""
        selected_column = self.dropdown.get_selected_value()
        print(f"selected_column: {selected_column}")  # 디버깅용 출력
        if selected_column:
            self.checkbox_manager.create_checkboxes_container(column_name=selected_column, batch_size=50)
            self.unique_value_checkboxes.visible = True  # 가시성을 True로 설정
            self.update_checkboxes_with_unique_values(selected_column)
            self.page.update()

    def search_unique_value(self, search_term):
        """검색어로 체크박스 필터링하고 UI를 업데이트합니다."""
        self.checkbox_manager.search_unique_value(search_term)
        self.checkbox_manager.build()
        self.update_selected_list_display()

    def select_all_columns(self):
        """전체선택"""
        self.checkbox_manager.select_all_checkboxes(callback=self.handle_checkbox_change)
        self.update_selected_list_display()

    def unselect_all_columns(self):
        """전체선택 해제"""
        self.checkbox_manager.unselect_all_checkboxes(callback=self.handle_checkbox_change)
        self.update_selected_list_display()

    def update_checkboxes_with_unique_values(self, selected_column):
        """선택된 열에 대한 고유 값을 사용하여 체크박스를 업데이트합니다."""
        self.checkbox_manager.create_checkboxes_container(column_name=selected_column, batch_size=50)
        self.unique_value_checkboxes.update()

    def select_save_options(self):
        """저장 옵션을 선택합니다."""
        self.radio_group.content = ft.Row(
            controls=[
                ft.Radio(value="mono_file", label="한 파일 한 시트로 만들기"),
                ft.Radio(value="multi_sheets", label="한 파일에 여러 시트로 만들기"),
                ft.Radio(value="multi_files", label="여러 파일로 만들기"),
            ]
        )

        return ft.Row(controls=[ft.Text("저장 옵션"), self.radio_group])

    def get_selected_save_option(self):
        """저장 옵션을 선택합니다."""
        return self.radio_group.value if self.radio_group else None

    def update_selected_list_display(self):
        """UI에 선택된 항목을 표시합니다."""
        self.selected_items_display.update_display()

    def handle_checkbox_change(self, e=None):
        """체크박스 변경 시 선택된 리스트를 업데이트"""
        self.update_selected_list_display()

    def on_resize(self, e):
        """창 크기 변경 시 호출되는 이벤트 핸들러."""
        self.window_width = self.page.window_width
        self.selected_items_display.width = self.window_width
        self.unique_value_checkboxes.width = self.window_width
        self.page.update()

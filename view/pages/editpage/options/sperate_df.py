import flet as ft
from model.data_manipulator import DataManipulator
from ....components.checkboxes import CheckboxManager
from ....components.SearchField import SearchField


class SperateDFOption:
    def __init__(self, page, meta_data, error_handler, window_width):
        self.page = page
        self.meta_data = meta_data
        self.selected_list_display = ft.Row(
            controls=[], scroll=ft.ScrollMode.AUTO, width=window_width, visible=False
        )
        self.unique_value_checkboxes = ft.Column(
            controls=[], visible=False, scroll=ft.ScrollMode.AUTO, width=window_width
        )
        self.checkbox_manager = CheckboxManager(
            page, self.unique_value_checkboxes, error_handler
        )
        self.data_manipulator = DataManipulator()

        self.dropdown = ft.Dropdown(
            width=600,
            on_change=lambda e: self.update_checkboxes_with_unique_values(
                e.control.value
            ),
        )

        self.isSperate = ft.Checkbox(
            label="데이터 필터링: 특정 열의 데이터를 가져와 원하는 값만 선택합니다.",
            value=False,
            on_change=lambda e: self.on_checkbox_change(e.control.value),
        )

        self.radio_group = ft.RadioGroup(content=None)

        # SearchField 컴포넌트 초기화
        self.search_component = SearchField(
            on_search=self.search_unique_value,
            on_select_all=lambda e: self.select_all_columns(),
            on_unselect_all=lambda e: self.unselect_all_columns(),
            width=400,
        )

        self.page.on_resize = self.on_resize

    def build(self, selected_labels):
        self.container = ft.Container(
            content=ft.Column(
                controls=[self.create_extension_panel(), self.create_content()]
            )
        )

        self.page.add(self.container)
        self.update_dropdown(selected_labels)

        return self.container

    def on_checkbox_change(self, value):
        self.content.visible = value
        self.content.update()

    def create_extension_panel(self):
        self.extension_panel = ft.Container(content=self.isSperate)
        return self.extension_panel

    def create_content(self):
        # 초기 선택된 리스트를 표시

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([ft.Text("열 선택"), self.dropdown]),
                    self.search_component.build(),  # search Field
                    self.selected_list_display,  # 선택된 항목 표시
                    self.unique_value_checkboxes,  # 고유값 체크박스로 반환하기
                    self.select_save_options(),
                ]
            ),
            visible=False,
        )
        return self.content

    # def register_checkbox_event_handlers(self) -> None:
    #     """체크박스의 이벤트 핸들러를 한 번만 등록합니다."""
    #     for checkbox in self.checkbox_manager.checkboxes:
    #         checkbox.on_change = self.handle_checkbox_change

    def on_column_selection_changed(self, selected_labels):
        """열 선택이 변경되었을 때 Dropdown을 업데이트"""
        self.update_dropdown(selected_labels)

    def update_dropdown(self, selected_labels):
        """Dropdown의 옵션을 업데이트"""
        self.dropdown.options = [
            ft.dropdown.Option(text=label) for label in selected_labels
        ]
        self.dropdown.update()  # UI 업데이트

    def search_unique_value(self, search_term):
        """검색어로 체크박스 필터링"""
        self.checkbox_manager.search_unique_value(search_term)
        self.update_selected_list_displayy()

    def select_all_columns(self) -> None:
        """전체선택"""
        self.checkbox_manager.select_all_checkboxes(
            callback=self.handle_checkbox_change
        )
        self.update_selected_list_display()

    def unselect_all_columns(self) -> None:
        """전체선택 해제"""
        self.checkbox_manager.unselect_all_checkboxes(
            callback=self.handle_checkbox_change
        )
        self.update_selected_list_display()

    def update_checkboxes_with_unique_values(self, selected_column):
        unique_values = sorted(self.meta_data.get_all_unique_values(selected_column))
        self.checkbox_manager.update_checkboxes_with_unique_values(unique_values)
        # self.register_checkbox_event_handlers()
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
        return self.radio_group.value if self.radio_group else None

    def update_selected_list_display(self) -> None:
        """UI에 선택된 항목을 표시합니다."""
        selected_texts = self.checkbox_manager.get_selected_checkbox_labels_as_text()
        self.selected_list_display.controls.clear()
        self.selected_list_display.controls.append(ft.Text("선택한 열 : "))
        self.selected_list_display.controls.extend(selected_texts)
        self.page.update()

    def handle_checkbox_change(self, e=None):
        """체크박스 변경 시 선택된 리스트를 업데이트"""
        self.update_selected_list_display()

    def on_resize(self, e):
        """창 크기 변경 시 호출되는 이벤트 핸들러."""
        # 새로운 창 너비를 가져와서 업데이트
        self.window_width = self.page.window_width
        self.selected_list_display.width = self.window_width
        self.unique_value_checkboxes.width = self.window_width
        self.page.update()  # UI 업데이트

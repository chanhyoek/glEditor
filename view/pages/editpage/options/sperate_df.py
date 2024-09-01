import flet as ft
from model.data_manipulator import DataManipulator
from ....components.checkboxes import CheckboxManager
from ....components.SearchField import SearchField
from model.eventHandler import Event

class SperateDFOption:
    def __init__(self, page, file_data):
        self.page = page
        self.file_data = file_data
        self.selected_values = ft.Row(controls=[], scroll=ft.ScrollMode.AUTO, width=1000, visible=False)
        self.unique_value_checkboxes = ft.Column(controls=[], visible=False, scroll=ft.ScrollMode.AUTO, width=1000)
        self.checkbox_manager = CheckboxManager(page, self.unique_value_checkboxes)
        self.data_manipulator = DataManipulator()
        self.all_set_data = None

        self.dropdown = ft.Dropdown(
            width=600,
            on_change=lambda e: self.update_checkboxes_with_unique_values(e.control.value)
        )

        self.isSperate = ft.Checkbox(
            label="데이터 필터링: 특정 열의 데이터를 가져와 원하는 값만 선택합니다.",
            value=False,
            on_change=lambda e: self.on_checkbox_change(e.control.value)
        )
        
        self.radio_group = None  # 라디오 그룹을 저장할 변수 초기화

        # SearchField 컴포넌트 초기화
        self.search_component = SearchField(
            on_search=self.search_unique_value,
            on_select_all=lambda e: self.select_all_columns(),
            on_unselect_all=lambda e: self.unselect_all_columns(),
            width=400
        )

    def build(self, selected_labels):
        self.container = ft.Container(
            content=ft.Column(
                controls=[
                    self.create_extension_panel(),
                    self.create_content()
                ]
            )
        )
        
        self.page.add(self.container)
        self.update_dropdown(selected_labels)
        
        return self.container 

    def on_checkbox_change(self, value):
        self.content.visible = value
        self.content.update()
        
    def create_extension_panel(self):        
        self.extension_panel = ft.Container(
            content=self.isSperate
        )
        return self.extension_panel

    def create_content(self):
        self.content = ft.Container(
            content=ft.Column(
                controls=[ 
                    ft.Row([ft.Text("열 선택"), self.dropdown]),
                    self.search_component.build(),  # SearchField를 사용
                    self.selected_values,
                    self.unique_value_checkboxes,
                    self.select_save_options()
                ]
            ),
            visible=False
        )
        return self.content
    
    def register_checkbox_event_handlers(self) -> None:
        """체크박스의 이벤트 핸들러를 한 번만 등록합니다."""
        for checkbox in self.checkbox_manager.checkboxes:
            checkbox.on_change = self.handle_checkbox_change
    
    def on_column_selection_changed(self, selected_labels):
        """열 선택이 변경되었을 때 Dropdown을 업데이트"""
        self.update_dropdown(selected_labels)

    def update_dropdown(self, selected_labels):
        """Dropdown의 옵션을 업데이트"""
        self.dropdown.options = [ft.dropdown.Option(text=label) for label in selected_labels]
        self.dropdown.update()  # UI 업데이트
    
    def search_unique_value(self, search_term):
        """검색어로 체크박스 필터링"""
        self.checkbox_manager.search_unique_value(search_term)
        self.update_selected_checkboxes_display()
    
    def select_all_columns(self) -> None:
        self.checkbox_manager.select_all_checkboxes(callback=self.handle_checkbox_change)
        self.update_selected_checkboxes_display()
        
    def unselect_all_columns(self) -> None:
        self.checkbox_manager.unselect_all_checkboxes(callback=self.handle_checkbox_change)
        self.update_selected_checkboxes_display()
    
    
    def update_checkboxes_with_unique_values(self, selected_column):
        if self.all_set_data is None: 
            common_headers = self.data_manipulator.get_common_headers(self.file_data)
            self.all_set_data = self.data_manipulator.concat_dataframes_with_common_headers(list(self.file_data.values()), common_headers)
        
        self.data_manipulator.load_dataframe(self.all_set_data)
        unique_values = sorted(self.data_manipulator.get_unique_values(selected_column))
        self.checkbox_manager.update_checkboxes_with_unique_values(unique_values)
        self.register_checkbox_event_handlers()  # 이벤트 핸들러 등록
        self.unique_value_checkboxes.update()
    
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

    def get_selected_save_option(self):
        return self.radio_group.value if self.radio_group else None

    def update_selected_checkboxes_display(self):
        """선택된 체크박스를 업데이트하여 UI에 표시"""
        selected_texts = self.checkbox_manager.get_selected_checkbox_labels_as_text()
        self.selected_values.controls.clear()
        self.selected_values.controls.append(ft.Text("선택한 열 : "))
        self.selected_values.controls.extend(selected_texts)
        self.page.update()
    
    def handle_checkbox_change(self, e=None):
        """체크박스 변경 시 선택된 리스트를 업데이트"""
        self.update_selected_checkboxes_display()

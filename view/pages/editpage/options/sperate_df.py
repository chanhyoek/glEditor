# main.py (또는 EditDataPage에서)
from model.data_manipulator import DataManipulator
from ....components.checkboxes import CheckboxManager
from ....components.SearchField import SearchField
import flet as ft

class SperateDFOption:
    def __init__(self, page, file_data):
        self.page = page
        self.file_data = file_data
        self.unique_value_checkboxes = ft.Column(controls=[], visible=False, scroll=ft.ScrollMode.AUTO, width=1000)
        self.checkbox_manager = CheckboxManager(page, self.unique_value_checkboxes)
        self.data_manipulator = DataManipulator()

        self.dropdown = ft.Dropdown(
            width=600,
            on_change=lambda e: self.update_checkboxes_with_unique_values(e.control.value)
        )

        # 데이터 준비
        self.all_set_data = None
        self.common_headers = self.data_manipulator.get_common_headers(self.file_data)
        self.all_set_data = self.data_manipulator.concat_dataframes_with_common_headers(list(self.file_data.values()), self.common_headers)
        
        self.isSperate = ft.Checkbox(
                label="데이터 필터링: 특정 열의 데이터를 가져와 원하는 값만 선택합니다.",
                value=False,
                on_change=lambda e: self.on_checkbox_change(e.control.value)
            )
        
        self.radio_group = None  # 라디오 그룹을 저장할 변수 초기화
        
                # SearchField 컴포넌트 초기화
        self.search_component = SearchField(
            on_search=self.search_unique_value,
            on_select_all=lambda e: self.checkbox_manager.select_all_checkboxes(),
            on_unselect_all=lambda e: self.checkbox_manager.unselect_all_checkboxes(),
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
            content= self.isSperate   
        )
        
        return self.extension_panel

    def create_content(self):
        self.content = ft.Container(
            content=ft.Column(
                controls=[ 
                    ft.Row([ft.Text("열 선택"), self.dropdown]),
                    self.search_component.build(),  # SearchField를 사용
                    self.unique_value_checkboxes,
                    self.select_save_options()
                ]
            ),
            visible=False
        )
        
        return self.content
    
    def on_column_selection_changed(self, selected_labels):
        """열 선택이 변경되었을 때 Dropdown을 업데이트"""
        self.update_dropdown(selected_labels)

    def update_dropdown(self, selected_labels):
        """Dropdown의 옵션을 업데이트"""
        self.dropdown.options = [ft.dropdown.Option(text=label) for label in selected_labels]
        self.dropdown.update()  # UI 업데이트
    
    def search_unique_value(self, search_term):
        self.checkbox_manager.search_unique_value(search_term)
    
    def update_checkboxes_with_unique_values(self, selected_column):
        self.data_manipulator.load_dataframe(self.all_set_data)
        unique_values = sorted(self.data_manipulator.get_unique_values(selected_column))
        self.checkbox_manager.update_checkboxes_with_unique_values(unique_values)
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

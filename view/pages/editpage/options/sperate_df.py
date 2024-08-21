# main.py (또는 EditDataPage에서)
from model.data_manipulator import DataManipulator
from .subview.sperate_df_view import SperateDFView
from ....components.checkboxes import CheckboxManager
import flet as ft

class SperateDFOption:
    def __init__(self, page, file_data):
        self.page = page
        self.file_data = file_data
        self.unique_value_checkboxes = ft.Column(controls=[], visible=False, scroll=ft.ScrollMode.AUTO, width=1000)
        self.checkbox_manager = CheckboxManager(page, self.unique_value_checkboxes)
        self.data_manipulator = DataManipulator()

        self.search_field = ft.TextField(hint_text="Search...", width=600)
        self.all_set_data = None
        self.common_headers = self.data_manipulator.get_common_headers(self.file_data)
        self.all_set_data = self.data_manipulator.concat_dataframes_with_common_headers(list(self.file_data.values()), self.common_headers)
        
        self.isSperate = ft.Checkbox(
                label="고유값으로 데이터 분리하기: 데이터를 특정열의 고유 값을 기준으로 분리합니다.",
                value=False,
                on_change=lambda e: self.on_checkbox_change(e.control.value)
            )
        
        self.radio_group = None  # 라디오 그룹을 저장할 변수 초기화

    def build(self):
        print("Sperate_df_option")
        
        self.container = ft.Container(
            content=ft.Column(
                controls=[
                    self.create_extension_panel(),
                    self.create_content()
                ]
            )
        )
        
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
                    ft.Row([ft.Text("열 선택"), self.create_dropdown_row()]),
                    self.create_search_unique_value_checkboxes(),
                    self.unique_value_checkboxes,
                    self.select_save_options()  # 저장 옵션을 포함
                ]
            ),
            visible=False
        )
        
        return self.content
    
    def create_dropdown_row(self):
        self.dropdown = ft.Dropdown(
            options=self.generate_options(),
            width=800,
            on_change=lambda e: self.update_checkboxes_with_unique_values(e.control.value)
        )
        return self.dropdown
    
    def generate_options(self):
        checkboxes = self.checkbox_manager.create_checkboxes_for_columns(self.file_data)
        selected_checkboxes = (checkbox for checkbox in checkboxes.controls if checkbox.value)
        options = [ft.dropdown.Option(text=checkbox.label) for checkbox in selected_checkboxes]
        return options

    def create_search_unique_value_checkboxes(self):
        self.search_unique_value_checkboxes = ft.Row(
            controls=[
                self.search_field,
                ft.CupertinoButton(content=ft.Text("Search"), on_click=lambda e: self.search_unique_value(self.search_field.value)),
                ft.CupertinoButton(content=ft.Text("전체선택"), on_click=lambda e: self.checkbox_manager.select_all_checkboxes()),
                ft.CupertinoButton(content=ft.Text("전체해제"), on_click=lambda e: self.checkbox_manager.unselect_all_checkboxes()),
            ]
        )
        
        return self.search_unique_value_checkboxes
    
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
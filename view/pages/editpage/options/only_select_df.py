import flet as ft

class OnlySelectedDFOption:
    def __init__(self, page):
        self.page = page
        self.is_selected_df = False

    def build(self):
        self.only_selected_df = ft.Checkbox(
                    label="현재 화면에 표시된 시트의 데이터만 편집합니다.",
                    value=False,
                    on_change=lambda e: self.set_only_selected_df(e.control.value)
            )
        
        return self.only_selected_df
    
    def set_only_selected_df(self, value):
        self.is_selected_df = value
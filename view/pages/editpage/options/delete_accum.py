import flet as ft

class DeleteAccumsOption:
    def __init__(self, page):
        self.page = page
        self.remove_accumlated_values = False

    def build(self):
        self.delete_accum_options = ft.Checkbox(
                    label="누적값제거 : 누계, 월계, 합계 등의 값이 포함되어 있는 행을 삭제합니다.",
                    value=False,
                    on_change=lambda e: self.set_accumulated_values(e.control.value)
            )
        
        return self.delete_accum_options
    
    def set_accumulated_values(self, value):
        self.remove_accumlated_values = value
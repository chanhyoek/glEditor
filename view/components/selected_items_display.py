import flet as ft
from typing import List
from controller.columns_controller import ColumnsController
from controller.unique_values_controller import UniqueValuesController
from controller.meta_data_controller import MetadataController
from typing import Union

class SelectedItemsDisplay(ft.UserControl):
    def __init__(self, 
                 page:ft.Page, 
                 height: int, 
                 controller: Union[ColumnsController,UniqueValuesController, MetadataController], 
                 mode:str, 
                 column_name=None ):
        super().__init__()
        self.page = page
        self.height = height
        self.controller = controller  
        self.mode = mode
        self._column_name = column_name

        self.row = ft.Row(
            controls=[],
            height=self.height,
            width= 1000,
            scroll=ft.ScrollMode.AUTO
        )
        
    @property
    def column_name(self):
        return self._column_name

    @column_name.setter
    def column_name(self, column_name):
        self._column_name = column_name 

    def build(self) -> ft.Row:
        """선택된 항목을 표시할 Row 컴포넌트를 생성합니다."""
        self.update_row_conentent()
        return self.row

    def _create_text_controls(self, items: List[str]) -> List[ft.Text]:
        """선택된 항목의 텍스트 컨트롤을 생성합니다."""
        return [ft.Text(label, size=16, color=ft.colors.LIGHT_BLUE) for label in items]

    def get_labels(self) -> List[str]:
        """현재 모드에 따라 적절한 데이터를 가져옵니다."""
        if self.mode == 'columns':
            # columns 모드인 경우 선택된 열의 이름을 가져옵니다.
            return self.controller.get_selected_columns()
        elif self.mode == 'unique_values':
            # unique_value 모드인 경우 특정 열의 선택된 고유값을 가져옵니다.
            return self.controller.get_selected_unique_values(self.column_name)
        elif self.mode == 'keys':
            return self.controller.get_selected_key()
        else:
            return []

    def update_display(self) -> None:
        """선택된 항목을 업데이트합니다."""
        self.update_row_conentent()
        self.row.update()

    def update_observer(self):
        self.update_display()  # 선택된 항목을 새로 갱신
    
    def update_row_conentent(self)-> None:
        selected_items = self.get_labels()
        self.row.controls.clear()  
        self.row.controls = [
            ft.Text("선택한 항목 : ", size=16),
            *self._create_text_controls(selected_items)
        ]

        
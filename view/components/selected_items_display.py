import flet as ft
from typing import List
from controller.columns_controller import ColumnsController

class SelectedItemsDisplay(ft.UserControl):
    def __init__(self, width: int, height: int, controller: ColumnsController, mode, column_name=None):
        super().__init__()
        self.width = width
        self.height = height
        self.controller = controller  # 하나의 컨트롤러 주입
        self.mode = mode
        self.column_name = column_name
        # self.controller.add_listener(self.update_display)  # 상태 변경 리스너 추가

        # 인스턴스 변수를 초기화
        self.row = ft.Row(
            controls=[],
            width=self.width,
            height=self.height,
            scroll=ft.ScrollMode.AUTO
        )

    def build(self) -> ft.Row:
        """선택된 항목을 표시할 Row 컴포넌트를 생성합니다."""
        self.row.controls = [
            ft.Text("선택한 항목 : "),
            *self._create_text_controls(self.get_labels())
        ]
        return self.row

    def _create_text_controls(self, items: List[str]) -> List[ft.Text]:
        """선택된 항목의 텍스트 컨트롤을 생성합니다."""
        return [ft.Text(label, size=16, color=ft.colors.LIGHT_BLUE_400) for label in items]

    def get_labels(self) -> List[str]:
        """현재 모드에 따라 적절한 데이터를 가져옵니다."""
        if self.mode == 'columns':
            # columns 모드인 경우 선택된 열의 이름을 가져옵니다.
            return self.controller.get_selected_columns()
        elif self.mode == 'unique_value':
            # unique_value 모드인 경우 특정 열의 선택된 고유값을 가져옵니다.
            return self.controller.get_selected_unique_values(self.column_name)
        else:
            return []

    def update_display(self) -> None:
        """선택된 항목을 업데이트합니다."""
        if self.page is None:  # 페이지에 추가되지 않은 경우, 아무 작업도 수행하지 않음
            return

        self.row.controls.clear()  
        self.row.controls.append(ft.Text("선택한 항목 : "))
        self.row.controls.extend(self._create_text_controls(self.get_labels()))
        self.update()  # 페이지에 추가된 후에만 업데이트 호출

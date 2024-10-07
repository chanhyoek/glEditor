import flet as ft
from typing import List
from controller.columns_controller import ColumnsController

class SelectableDropdown(ft.UserControl):
    def __init__(self, page, controller: ColumnsController, width: int = 700):
        super().__init__()
        self.controller = controller
        self.page = page
        self.width = width
        self.selected_value = None  # 선택된 값을 저장할 속성
        self.external_on_change = None  # 외부 이벤트 핸들러
        self.dropdown = ft.Dropdown(width=self.width, on_change=self._handle_change, options=[])  # 드롭다운 초기화

    def build(self) -> ft.Dropdown:
        """Dropdown 컴포넌트를 생성합니다."""
        self.update_dropdown_content()
        return self.dropdown

    def get_selected_options(self) -> List[ft.dropdown.Option]:
        """is_select가 True인 열 이름만 옵션으로 반환합니다."""
        selected_columns = self.controller.get_selected_columns()
        return [ft.dropdown.Option(text=col) for col in selected_columns]

    def update_dropdown(self) -> None:
        """Dropdown 옵션을 업데이트합니다."""
        self.update_dropdown_content()
        # 드롭다운이 변경되었음을 Flet에 알림
        self.dropdown.update()
        self.page.update()  # 페이지 전체를 새로고침

    def _handle_change(self, event):
        """Dropdown 선택이 변경되었을 때의 내부 핸들러입니다."""
        self.set_selected_value(event.control.value)
        # 외부 핸들러가 있는 경우 호출
        if self.external_on_change:
            self.external_on_change(event)

    def set_selected_value(self, value: str) -> None:
        """선택된 Dropdown 값을 설정합니다."""
        self.selected_value = value

    def get_selected_value(self) -> str:
        """선택된 Dropdown 값을 반환합니다."""
        return self.selected_value

    def set_on_change(self, handler) -> None:
        """외부 변경 핸들러를 설정합니다."""
        self.external_on_change = handler

    def update_observer(self):
        """ColumnsController로부터 알림을 받으면 호출되는 메서드."""
        self.update_dropdown()  # 드롭다운 옵션 새로고침

    def update_dropdown_content(self) -> None:
        """Dropdown의 옵션을 새로고침합니다."""
        # 기존 옵션을 모두 제거하고, 새로운 옵션을 추가합니다.
        self.dropdown.options.clear()
        new_options = self.get_selected_options()
        self.dropdown.options.extend(new_options)
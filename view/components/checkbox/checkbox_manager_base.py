from abc import ABC, abstractmethod
import flet as ft

class CheckboxManagerBase(ft.UserControl, ABC):
    def __init__(self, page, container, error_handler):
        super().__init__()
        self.page = page
        self.container = container
        self.error_handler = error_handler
        self.checkboxes = []

    @abstractmethod
    def create_checkboxes_container(self, key: str, batch_size=10):
        """체크박스 컨테이너를 생성합니다."""
        pass

    @abstractmethod
    def _on_checkbox_change(self, value):
        """체크박스 값 변경 시 호출되는 콜백 함수입니다."""
        pass

    def select_all_checkboxes(self):
        """모든 체크박스를 선택합니다."""
        self._set_all_checkboxes_value(True)

    def unselect_all_checkboxes(self):
        """모든 체크박스를 선택 해제합니다."""
        self._set_all_checkboxes_value(False)

    def _set_all_checkboxes_value(self, value):
        """모든 체크박스의 값을 설정합니다."""
        for checkbox in self.checkboxes:
            checkbox.value = value
            self._update_selection_state(checkbox.label, value)
        self.page.update()

    @abstractmethod
    def _update_selection_state(self, label, value):
        """선택 상태를 업데이트하는 추상 메서드입니다."""
        pass

    def register_checkbox_event_handlers(self, handler):
        """모든 체크박스에 대해 이벤트 핸들러를 등록합니다."""
        for checkbox in self.checkboxes:
            checkbox.on_change = handler

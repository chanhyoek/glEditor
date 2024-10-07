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
        pass

    @abstractmethod
    def _on_checkbox_change(self, value):
        pass

    @abstractmethod
    def update_observer(self):
        pass

    def select_all_checkboxes(self):
        """모든 체크박스를 선택합니다."""
        self._set_all_checkboxes_value(True)

    def unselect_all_checkboxes(self):
        """모든 체크박스를 선택 해제합니다."""
        self._set_all_checkboxes_value(False)

    def _set_all_checkboxes_value(self, value):
        """컨테이너 내 모든 체크박스의 값을 설정합니다."""
        self._recursive_set_checkbox_value(self.container, value)
        self.page.update()

    def _recursive_set_checkbox_value(self, control, value):
        """재귀적으로 컨트롤을 탐색하며 모든 체크박스의 값을 설정합니다."""
        if isinstance(control, ft.Checkbox):
            control.value = value
            self._update_selection_state(control.label, value)

        if hasattr(control, 'controls') and control.controls:
            for child in control.controls:
                self._recursive_set_checkbox_value(child, value)

    @abstractmethod
    def _update_selection_state(self, label, value):
        pass

    def register_checkbox_event_handlers(self, handler):
        for checkbox in self.checkboxes:
            checkbox.on_change = handler

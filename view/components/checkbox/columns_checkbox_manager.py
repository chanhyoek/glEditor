from .checkbox_manager_base import CheckboxManagerBase
from ..Paginator import Paginator
import flet as ft

class ColumnsCheckboxManager(CheckboxManagerBase):
    def __init__(self, page, container, error_handler, controller):
        super().__init__(page, container, error_handler)
        self.event_listeners = []
        self.columns_controller = controller
        self.paginator = None 

        # Checkbox와 Pagination을 분리한 컨테이너 설정
        self.checkbox_container = ft.Row(spacing=5, scroll=ft.ScrollMode.AUTO)
        self.pagination_row = ft.Row(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER)

    def build(self):
        """Flet UserControl의 빌드 메서드, 컨트롤을 반환합니다."""
        self.create_checkboxes_container()
        return self.container

    def create_checkboxes_container(self, batch_size=50):
        """열 이름에 대한 체크박스 컨테이너를 생성합니다."""
        self.container.controls.clear()
        self.checkbox_container.controls.clear()
        self.pagination_row.controls.clear()

        columns_data = self.columns_controller.get_all_columns_properties()
        labels = [(data['col_name'], data['is_all_dup'], data['is_select']) for data in columns_data]
        
        # Paginator 생성
        self.paginator = Paginator(
            total_items=len(labels),
            items_per_page=batch_size,
            on_page_change_callback=lambda: self._refresh_checkboxes(labels)
        )

        self._refresh_checkboxes(labels)
        self._refresh_pagination_controls()
        self.page.update()

    def _refresh_checkboxes(self, labels):
        """현재 페이지의 체크박스를 다시 생성하고 컨테이너에 추가합니다."""
        self.checkbox_container.controls.clear()  # 체크박스만 초기화

        # 현재 페이지에 해당하는 항목 가져오기
        paginated_values = self.paginator.get_current_page_items(labels)

        # 체크박스를 위한 Row 그룹 생성 (최대 5개의 Row)
        col = ft.Column(spacing=5)
        for i in range(0, len(paginated_values), 12):  # 10개씩 나누어 Row 생성
            checkbox_row_container = ft.Container(
                border=ft.border.all(1, ft.colors.LIGHT_BLUE_400), 
                border_radius=ft.border_radius.all(10),
                padding=10
            )
            row = ft.Row(spacing=5)
            for label, is_all_dup, is_selected in paginated_values[i:i + 12]:
                fill_color = ft.colors.BLUE if is_all_dup else ft.colors.WHITE
                checkbox = ft.Checkbox(
                    label=label,
                    value=is_selected,
                    fill_color=fill_color
                )
                checkbox.on_change = lambda e, v=label: self._on_checkbox_change(e, v)
                row.controls.append(checkbox)
            col.controls.append(row)
    
        checkbox_row_container.content = col
        self.checkbox_container.controls.append(checkbox_row_container)
        
        # Checkbox 컨테이너를 메인 컨테이너에 추가
        if self.checkbox_container not in self.container.controls:
            self.container.controls.append(self.checkbox_container)
        self.page.update()

    def _refresh_pagination_controls(self):
        """Pagination 컨트롤을 업데이트합니다."""
        self.pagination_row.controls.clear()
        self.paginator.add_pagination_controls(self.pagination_row)  # 페이지네이션 UI 추가

        # Pagination Row를 메인 컨테이너에 추가
        if self.pagination_row not in self.container.controls:
            self.container.controls.append(self.pagination_row)

    def _on_checkbox_change(self, event, value):
        """체크박스 값 변경 시 호출되는 콜백 함수입니다."""
        new_state = event.control.value  # 이벤트에서 새로운 상태 가져오기
        self.columns_controller.update_column_selection(value, new_state)  # 선택 상태 업데이트

    def _update_selection_state(self, label, value):
        """열 이름에 대한 선택 상태를 업데이트합니다."""
        self.columns_controller.update_column_selection(label, value)
        self.page.update()
        # self.notify_listeners()  # UI 업데이트를 위해 모든 리스너에게 알림

    # def notify_listeners(self):
    #     """이벤트 리스너들에게 상태 변경을 알립니다."""
    #     for listener in self.event_listeners:
    #         listener()

    # def add_event_listener(self, listener):
    #     """이벤트 리스너를 추가합니다."""
    #     self.event_listeners.append(listener)

    def _update_selection_state(self, label, value):
        """열 이름에 대한 선택 상태를 업데이트합니다."""
        self.columns_controller.update_column_selection(label, value)
        self.page.update()

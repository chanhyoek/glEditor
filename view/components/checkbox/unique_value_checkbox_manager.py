from .checkbox_manager_base import CheckboxManagerBase
from ..Paginator import Paginator
import flet as ft

class UniqueValuesCheckboxManager(CheckboxManagerBase):
    def __init__(self, page, container, error_handler, controller):
        super().__init__(page, container, error_handler)
        self.event_listeners = []  # 이벤트 리스너 목록
        self.unique_values_controller = controller
        self.paginator = None  # Paginator 인스턴스 초기화
        self.column_name = None

        # Checkbox와 Pagination을 분리한 컨테이너 설정
        self.checkbox_container = ft.Row(spacing=5, scroll=ft.ScrollMode.AUTO)
        self.pagination_row = ft.Row(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER)

    def build(self):
        """Flet UserControl의 빌드 메서드, 컨트롤을 반환합니다."""
        if self.column_name:
            self.create_checkboxes_container(self.column_name)
        return self.container

    def create_checkboxes_container(self, column_name: str, batch_size=50):
        """고유 값에 대한 체크박스 컨테이너를 생성합니다."""
        self.column_name = column_name  # column_name 저장
        
        self.container.controls.clear()
        self.pagination_row.controls.clear()
        self.checkbox_container.controls.clear()

        unique_values = self.unique_values_controller.get_all_unique_values_properties(self.column_name)
        labels = [(item['value'], item['is_selected']) for item in unique_values]
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

        col = ft.Column(spacing=5)
        if paginated_values:  # paginated_values가 존재할 때만 진행
            checkbox_row_container = ft.Container(
                border=ft.border.all(1, ft.colors.LIGHT_BLUE_400), 
                border_radius=ft.border_radius.all(10),
                padding=10
            )

            for i in range(0, len(paginated_values), 12):  # 10개씩 나누어 Row 생성
                row = ft.Row(spacing=5)
                for label, is_selected in paginated_values[i:i + 12]:
                    checkbox = ft.Checkbox(
                        label=label,
                        value=is_selected,
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
        column_name = self.column_name  
        current_state = next((cb.value for cb in self.checkboxes if cb.label == value), False)
        self.unique_values_controller.update_unique_value_selection(column_name, value, not current_state)
        print(f"Checkbox '{value}' state changed to {not current_state}")

    def _update_selection_state(self, label, value):
        """고유 값에 대한 선택 상태를 업데이트합니다."""
        column_name = self.column_name  # 현재 관리 중인 column_name 사용
        self.unique_values_controller.update_unique_value_selection(column_name, label, value)

    def on_column_selection_changed(self, e):
        """열 선택이 변경되었을 때 CheckboxManager 업데이트."""
        selected_column = self.dropdown.get_selected_value()
        if selected_column:
            self.create_checkboxes_container(column_name=selected_column, batch_size=50)
            self.update_checkboxes_with_unique_values(selected_column)

    # def notify_listeners(self):
    #     """이벤트 리스너들에게 상태 변경을 알립니다."""
    #     for listener in self.event_listeners:
    #         listener()

    # def add_event_listener(self, listener):
    #     """이벤트 리스너를 추가합니다."""
    #     self.event_listeners.append(listener)

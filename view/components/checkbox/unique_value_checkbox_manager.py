from .checkbox_manager_base import CheckboxManagerBase
from controller.unique_values_controller import UniqueValuesController
from ..Paginator import Paginator
import flet as ft

class UniqueValuesCheckboxManager(CheckboxManagerBase):
    def __init__(self, page, container, error_handler, controller:UniqueValuesController):
        super().__init__(page, container, error_handler)
        self.event_listeners = []  # 이벤트 리스너 목록
        self.unique_values_controller = controller
        self.paginator = None  # Paginator 인스턴스 초기화
        self.column_name = None

        self.checkbox_container = ft.Row(spacing=5, scroll=ft.ScrollMode.AUTO)
        self.pagination_row = ft.Row(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER)

    def build(self):
        """Flet UserControl의 빌드 메서드, 컨트롤을 반환합니다."""
        if self.column_name:
            self.create_checkboxes_container(self.column_name)
        return self.container

    def create_checkboxes_container(self, column_name: str, batch_size=50):
        """고유 값에 대한 체크박스 컨테이너를 생성합니다."""
        self.column_name = column_name  
        
        self.container.controls.clear()
        self.pagination_row.controls.clear()
        self.checkbox_container.controls.clear()

        unique_values = self.unique_values_controller.get_all_unique_values_properties(self.column_name)
        labels = [(item['value'], item['is_selected']) for item in unique_values]
        # Paginator 생성
        self.paginator = Paginator(
            items= labels,
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
        paginated_values = self.paginator.get_current_page_items()

        col = ft.Column(spacing=5)
        if paginated_values: 
            checkbox_row_container = ft.Container(
                border_radius=ft.border_radius.all(10),
                padding=10,
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
        new_state = event.control.value
        self.unique_values_controller.update_unique_value_selection(value, new_state)

    def _update_selection_state(self, label, value):
        """고유 값에 대한 선택 상태를 업데이트합니다."""
        column_name = self.column_name  # 현재 관리 중인 column_name 사용
        self.unique_values_controller.update_unique_value_selection(column_name, label, value)

    def update_observer(self):
        """Controller로부터 상태 변경을 통지받으면 호출되는 메서드."""
        if self.column_name:
            unique_values = self.unique_values_controller.get_all_unique_values_properties(self.column_name)
            labels = [(item['value'], item['is_selected']) for item in unique_values]
            self.paginator.set_items(labels)

            # 체크박스를 갱신합니다.
            self._refresh_checkboxes(labels)
            self._refresh_pagination_controls()
            self.page.update()

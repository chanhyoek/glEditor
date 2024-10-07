from abc import ABC
from .checkbox_manager_base import CheckboxManagerBase
import flet as ft
from typing import List
from controller.meta_data_controller import MetadataController
from view.components.Paginator import Paginator

class KeysCheckboxManager(CheckboxManagerBase):
    def __init__(self, page, container, error_handler, controller:MetadataController):
        super().__init__(page, container, error_handler)
        self.metadata_controller = controller
        self.paginator = None
        self.container = container

        self.keys_container = ft.Row(spacing=5, scroll=ft.ScrollMode.AUTO)
        self.pagination_row = ft.Row(scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER)


    def build(self):
        self.create_checkboxes_container()

    def create_checkboxes_container(self, batch_size=30):
        """키에 대한 체크박스 컨테이너를 생성합니다."""
        self.container.controls.clear()
        selected_properties = self.metadata_controller.get_all_keys_selected_properties()

        labels = [(data['key'], data['is_select']) for data in selected_properties]

        self.paginator = Paginator(
            items = labels,
            items_per_page=batch_size,
            on_page_change_callback=lambda: self._refresh_checkboxes(labels)
        )

        self._refresh_checkboxes(labels)
        self._refresh_pagination_controls() 
        self.page.update()

    def _refresh_checkboxes(self, labels):
        """현재 페이지의 체크박스를 다시 생성하고 컨테이너에 추가합니다."""
        self.keys_container.controls.clear()  

        paginated_values = self.paginator.get_current_page_items()
     

        col = ft.Column(spacing=5)
        if paginated_values: 
            keys_row_container = ft.Container(
                border_radius=ft.border_radius.all(10),
                padding=10,
            )

            for i in range(0, len(paginated_values), 12):  # 10개씩 나누어 Row 생성
                row = ft.Row(spacing=5)
                for label, is_select in paginated_values[i:i + 12]:
                    checkbox = ft.Checkbox(
                        label=label,
                        value=is_select,
                    )
                    checkbox.on_change = lambda e, v=label: self._on_checkbox_change(e, v)
                    row.controls.append(checkbox)
                col.controls.append(row)
            
            keys_row_container.content = col
            self.keys_container.controls.append(keys_row_container)

        # Checkbox 컨테이너를 메인 컨테이너에 추가
        if self.keys_container not in self.container.controls:
            self.container.controls.append(self.keys_container)
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
        self.metadata_controller.update_keys_selection(value, new_state)

    def _update_selection_state(self, label, value):
        """고유 값에 대한 선택 상태를 업데이트합니다."""
        pass

    def update_observer(self):
        """Controller로부터 상태 변경을 통지받으면 호출되는 메서드."""
        selected_properties = self.metadata_controller.get_all_keys_selected_properties()
        labels = [(data['key'], data['is_select']) for data in selected_properties]
        self.paginator.set_items(labels)

        self._refresh_checkboxes(labels)
        self._refresh_pagination_controls()
        self.page.update

    


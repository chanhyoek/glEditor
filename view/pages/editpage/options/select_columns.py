import flet as ft
from ....components.checkboxes import CheckboxManager
from ....components.SearchField import SearchField
from model.eventHandler import Event
from typing import List

class SelectColumnsOption:
    def __init__(self, page: ft.Page, meta_data: dict, error_handler, window_width):
        self.page = page
        self.meta_data = meta_data
        self.checkboxes = ft.Row(width=window_width, scroll=ft.ScrollMode.AUTO, height=20)
        self.checkbox_manager = CheckboxManager(page, self.checkboxes, error_handler)
        self.selected_list_display = ft.Row(width=window_width, scroll=ft.ScrollMode.AUTO, height=20)
        self.on_selection_change = Event()

        # 검색 및 선택/해제 컴포넌트 설정
        self.search_component = SearchField(
            on_search=self.search_and_update,
            on_select_all=lambda e: self.select_all_columns(),
            on_unselect_all=lambda e: self.unselect_all_columns(),
            width=400
        )

    def build(self) -> ft.Container:
        """UI 컴포넌트를 구성하고 반환합니다."""
        # 설명 텍스트
        description = ft.Row(
            controls=[
                ft.Text("열 선택하기 : 원하는 열만 선택하세요", size=15),
            ]
        )
        # 체크박스 생성
        self.checkbox_manager.create_checkboxes_for_columns(self.meta_data)

        # 초기 선택된 리스트를 표시
        self.update_selected_list_display()

        # 체크박스 변경 시 이벤트 핸들러 등록
        self.checkbox_manager.register_checkbox_event_handlers(self.handle_checkbox_change)

        self.main_column = ft.Column(
                controls=[
                    description,
                    self.search_component.build(),
                    self.selected_list_display,
                    self.checkboxes
                ],
                expand=True,
            )
        # UI 구성
        return ft.Container(
            content= self.main_column
        )

    def search_and_update(self, search_term: str) -> None:
        """검색 후 체크박스 선택 상태를 업데이트합니다."""
        self.checkbox_manager.search_unique_value(search_term)
        self.refresh_display_and_emit_change()

    def select_all_columns(self) -> None:
        """모든 열을 선택합니다."""
        self.checkbox_manager.select_all_checkboxes()
        self.refresh_display_and_emit_change()

    def unselect_all_columns(self) -> None:
        """모든 열 선택을 해제합니다."""
        self.checkbox_manager.unselect_all_checkboxes()
        self.refresh_display_and_emit_change()

    def refresh_display_and_emit_change(self) -> None:
        """선택된 리스트를 업데이트하고 이벤트를 발행합니다."""
        self.update_selected_list_display()
        self.emit_selection_change()

    def update_selected_list_display(self) -> None:
        """UI에 선택된 항목을 표시합니다."""
        selected_texts = self.checkbox_manager.get_selected_checkbox_labels_as_text()
        self.selected_list_display.controls.clear()
        self.selected_list_display.controls.append(ft.Text("선택한 열 : "))
        self.selected_list_display.controls.extend(selected_texts)
        self.page.update()

    def handle_checkbox_change(self, e) -> None:
        """체크박스 변경 시 선택된 리스트를 업데이트합니다."""
        self.refresh_display_and_emit_change()

    def emit_selection_change(self) -> None:
        """선택된 열이 변경되었을 때 이벤트를 발행합니다."""
        selected_labels = [label for label in self.checkbox_manager.get_selected_checkbox_labels()]
        self.on_selection_change.emit(selected_labels)  # 이벤트 발행

    def on_resize(self, e):
        """창 크기 변경 시 호출되는 이벤트 핸들러."""
        self.window_width = self.page.window_width
        self.main_column.width = self.window_width
        self.page.update() 
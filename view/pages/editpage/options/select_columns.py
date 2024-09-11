import flet as ft
from ....components.checkboxes_factory import create_checkbox_manager
from ....components.SearchField import SearchField
from ....components.selected_items_display import SelectedItemsDisplay
from controller.columns_controller import ColumnsController
from model.eventHandler import Event
from typing import List

class SelectColumnsOption:
    def __init__(self, page: ft.Page, columns_controller: ColumnsController, error_handler, window_width):
        try:
            self.page = page
            self.columns_controller = columns_controller
            self.on_selection_change = Event()
            self.checkboxes = ft.Column(scroll=ft.ScrollMode.AUTO, width=window_width)

            # 선택된 항목 표시 컴포넌트 생성
            self.selected_items_display = SelectedItemsDisplay(
                width=window_width, height=20, mode='columns', controller=columns_controller
            )

            # 팩토리 메서드를 통해 적절한 CheckboxManager 생성
            self.checkbox_manager = create_checkbox_manager(
                mode='columns',  
                page=self.page,
                container=self.checkboxes,
                error_handler=error_handler,
                controller=columns_controller
            )

            # 검색 및 선택/해제 컴포넌트 설정
            self.search_component = SearchField(
                on_search=self.search_and_update,
                on_select_all=lambda e: self.select_all_columns(),
                on_unselect_all=lambda e: self.unselect_all_columns(),
                width=400
            )
        except Exception as e:
            print(f"[ERROR] SelectColumnsOption 초기화 중 오류 발생: {e}")

    def build(self) -> ft.Container:
        """UI 컴포넌트를 구성하고 반환합니다."""

        self.checkbox_manager.build()

        self.main_column = ft.Column(
            controls=[
                self.search_component.build(),
                self.selected_items_display,  
                self.checkboxes,  
            ],
            expand=True,
        )

        self.container = ft.Container(
            content=self.main_column
        )

        self.page.add(self.container)
    
        self.update_selected_list_display()
        
        # UI 구성
        return self.container

    def search_and_update(self, search_term: str) -> None:
        """검색 후 체크박스 선택 상태를 업데이트합니다."""
        self.columns_controller.search_columns(search_term)
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
        """페이지를 새로고침합니다"""
        self.update_selected_list_display()

    def update_selected_list_display(self) -> None:
        """선택된 체크박스를 표시합니다."""
        self.selected_items_display.update_display()

    def on_resize(self, e):
        """창 크기 변경 시 호출되는 이벤트 핸들러."""
        self.window_width = self.page.window_width
        self.main_column.width = self.window_width
        self.selected_items_display.width = self.window_width
        self.page.update()

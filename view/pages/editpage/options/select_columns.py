import flet as ft
from ....components.checkboxes_factory import create_checkbox_manager
from ....components.SearchField import SearchField
from ....components.selected_items_display import SelectedItemsDisplay
from controller.columns_controller import ColumnsController
from model.eventHandler import Event
from typing import List

class SelectColumnsOption:
    def __init__(self, page: ft.Page, columns_controller: ColumnsController, error_handler):
        self.page = page
        self.columns_controller = columns_controller
        self.on_selection_change = Event()
        self.checkboxes = ft.Column(scroll=ft.ScrollMode.AUTO)

        # 선택된 항목 표시 컴포넌트 생성
        self.selected_items_display = SelectedItemsDisplay(
            page = self.page, 
            height=20, 
            mode='columns', 
            controller=columns_controller
        )

        # 팩토리 메서드를 통해 적절한 CheckboxManager 생성
        self.checkbox_manager = create_checkbox_manager(
            mode='columns',  
            page=self.page,
            container=self.checkboxes,
            error_handler=error_handler,
            controller=columns_controller
        )

        # 옵저버 등록
        columns_controller.add_observer(self.checkbox_manager)
        columns_controller.add_observer(self.selected_items_display)

        # 검색 및 선택/해제 컴포넌트 설정
        self.search_component = SearchField(
            on_search=self.search_and_update,
            on_select_all=lambda e: self.select_all_columns(),
            on_unselect_all=lambda e: self.unselect_all_columns(),
            width=400
        )

        
    def build(self) -> ft.Container:
        """UI 컴포넌트를 구성하고 반환합니다."""

        self.checkbox_manager.build()

        self.main_column = ft.Column(
            controls=[
                self.search_component.build(),
                self.selected_items_display.build(),  
                self.checkboxes,  
            ],
            expand=True,
        )

        self.container = ft.Container(
            content=self.main_column
        )

        self.page.add(self.container)
            
        # UI 구성
        return self.container

    def search_and_update(self, search_term: str) -> None:
        """검색 후 체크박스 선택 상태를 업데이트합니다."""
        self.columns_controller.search_columns(search_term)

    def select_all_columns(self) -> None:
        """모든 열을 선택합니다."""
        self.columns_controller.select_all_columns()

    def unselect_all_columns(self) -> None:
        """모든 열 선택을 해제합니다."""
        self.columns_controller.unselect_all_columns()



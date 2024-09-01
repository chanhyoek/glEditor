import flet as ft
from ....components.checkboxes import CheckboxManager
from ....components.SearchField import SearchField
from model.eventHandler import Event
from typing import List

class SelectColumnsOption:
    def __init__(self, page: ft.Page, file_data: dict):
        self.page = page
        self.file_data = file_data
        self.checkboxes = ft.Row(width=1000, scroll=ft.ScrollMode.AUTO)
        self.checkbox_manager = CheckboxManager(page, self.checkboxes)
        self.selected_list_display = ft.Row(width=1000, scroll=ft.ScrollMode.AUTO)
        self.on_selection_change = Event()  # 이벤트 객체 생성

        # 검색 및 선택/해제 컴포넌트 설정
        self.search_component = SearchField(
            on_search= self.search_and_update,
            on_select_all=lambda e: self.select_all_columns(),
            on_unselect_all=lambda e: self.unselect_all_columns(),
            width=400
        )

    def build(self) -> ft.Container:
        # 설명 텍스트
        description = ft.Row(
            controls=[
                ft.Text("열 선택하기 : 원하는 열만 선택하세요", size=15),
            ]
        )

        # 체크박스 생성
        self.checkbox_manager.create_checkboxes_for_columns(self.file_data)
        
        self.update_selected_list_display()

        # 체크박스 변경 시 이벤트 핸들러 연결
        self.register_checkbox_event_handlers()


        # UI 구성
        return ft.Container(
            content=ft.Column(
                controls=[
                    description,
                    self.search_component.build(),
                    self.selected_list_display,
                    self.checkboxes
                ],
                expand=True,
                width=1000
            )
        )

    def register_checkbox_event_handlers(self) -> None:
        """체크박스의 이벤트 핸들러를 한 번만 등록합니다."""
        for checkbox in self.checkbox_manager.checkboxes:
            checkbox.on_change = self.handle_checkbox_change
    
    def search_and_update(self, search_term: str) -> None:
        """검색 후 selectedList를 업데이트"""
        self.checkbox_manager.search_unique_value(search_term)
        self.update_selected_list_display()
        self.emit_selection_change()
        
    def select_all_columns(self) -> None:
        self.checkbox_manager.select_all_checkboxes()
        self.update_selected_list_display()
        self.emit_selection_change()
        
    def unselect_all_columns(self) -> None:
        self.checkbox_manager.unselect_all_checkboxes()
        self.update_selected_list_display()
        self.emit_selection_change()

    def update_selected_list_display(self) -> None:
        """체크박스에 체크된 항목을 selected_list에 반환하여 UI에 표시"""
        selected_texts = self.checkbox_manager.get_selected_checkbox_labels_as_text()
        self.selected_list_display.controls.clear()  # 기존 선택된 리스트 클리어
        self.selected_list_display.controls.append(ft.Text("선택한 열 : "))
        self.selected_list_display.controls.extend(selected_texts)  # 새로운 선택된 리스트 추가
        self.page.update()  # UI 업데이트

    def handle_checkbox_change(self, e) -> None:
        """선택된 리스트를 업데이트하고 이벤트를 발행"""
        self.update_selected_list_display()
        self.emit_selection_change()
        
    def emit_selection_change(self) -> None:
        """선택된 열이 변경되었을 때 이벤트를 발생시킴"""
        selected_labels = self.get_selected_labels()
        self.on_selection_change.emit(selected_labels)  # 이벤트 발행
    
    def get_selected_labels(self) -> List[str]:
        """선택된 체크박스의 라벨을 반환"""
        return [checkbox.label for checkbox in self.checkbox_manager.checkboxes if checkbox.value]

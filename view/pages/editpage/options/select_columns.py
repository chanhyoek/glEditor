import flet as ft
from ....components.checkboxes import CheckboxManager

class SelectColumnsOption:
    def __init__(self, page, file_data):
        self.page = page
        self.file_data = file_data
        self.checkboxes = ft.Row(width=2000, scroll=ft.ScrollMode.AUTO)
        self.checkbox_manager = CheckboxManager(page, self.checkboxes)

    def build(self):
        print("SelectColumnsOption")
        # 설명 텍스트
        description = ft.Row(
            controls = [
                ft.Text("열 선택하기 : 원하는 열만 선택하세요", size=15),
                ft.CupertinoButton(content=ft.Text("전체선택", size=15), on_click=lambda e: self.checkbox_manager.select_all_checkboxes()),
                ft.CupertinoButton(content=ft.Text("전체해제", size=15), on_click=lambda e: self.checkbox_manager.unselect_all_checkboxes())
                ]
        )
        # 체크박스 생성 (file_data에서 열 이름을 가져와서 생성)
        self.checkbox_manager.create_checkboxes_for_columns(self.file_data)
    
        # 구성 요소들을 하나의 Column에 넣어 반환
        return ft.Container(
            content=ft.Column(
                controls=[
                    description,
                    self.checkboxes  # 체크박스 리스트 추가
                ],
                expand=True,
                spacing=10,
                width=1000
            )
        )

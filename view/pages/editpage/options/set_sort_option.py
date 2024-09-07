# main.py (또는 EditDataPage에서)
from model.data_manipulator import DataManipulator
import flet as ft

class SortOptionsContainer:
    def __init__(self, page, meta_data, header):
        self.page = page
        self.meta_data = meta_data
        self.data_manipulator = DataManipulator()        
        self.container_list = ft.Column()  # 복사된 컨테이너들을 저장할 Column
        self.header = header
        self.sort_option_checkbox = ft.Checkbox(
            label="정렬 옵션: 원하는 열을 선택하여 정렬합니다",
            value=False,
            on_change= lambda e: self.toggle_content_visibility(e.control.value)
        )
        self.content_visible = False  # 내부 컨텐츠 표시 여부

    def build(self, header):
        
        self.header = header
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([
                        self.sort_option_checkbox,
                        self.create_btn(),
                    ]),
                    self.create_content()
                ],
                spacing= 15
            )
        )

    def create_btn(self):
        self.btn_container =  ft.Container(
                content = ft.Row([
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD, 
                        on_click=lambda e: self.add_sort_option_container(),
                        mini=True
                    ),
                    ft.FloatingActionButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e: self.delete_sort_option_container(),
                        mini=True
                    )
                ]),visible=False
        )
        
        return self.btn_container
    
    def create_content(self):
        
        self.container_list.controls.append(self.create_sort_option_container())
        
        self.content = ft.Container(
            content = ft. Column(
                controls= [
                    self.container_list,
                ]
            ),
            visible= False
        )
        
        return self.content
    
    def toggle_content_visibility(self, value):
        self.btn_container.visible = value
        self.content.visible = value
        self.btn_container.update()
        self.content.update()

    def add_sort_option_container(self):
        # 새로운 정렬 옵션 컨테이너를 생성하여 리스트에 추가
        new_container = self.create_sort_option_container()
        self.container_list.controls.append(new_container)
        self.container_list.update()
        self.page.update()  # 페이지 전체를 업데이트하여 변경 사항 반영

    def delete_sort_option_container(self):
        self.container_list.controls.pop()
        self.container_list.update()
    
    def create_sort_option_container(self):
        # 드롭다운, 오름차순 및 내림차순 체크박스를 포함하는 컨테이너 생성
        dropdown = ft.Dropdown(
            options=self.generate_options(),
            width=600
        )

        radio_group = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="Ascending", label="오름차순"),
                    ft.Radio(value="Descending", label="내림차순"),
                ]
            )
        )
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column([dropdown]),
                    ft.Column([
                        radio_group
                    ])
                    
                ]
            )
        )

    def generate_options(self):
        # 열 이름을 가져와 드롭다운 옵션으로 생성
        options = [ft.dropdown.Option(col) for col in self.header]
        return options
    
    def on_column_selection_changed(self, selected_labels):
        # 모든 드롭다운에서 옵션을 업데이트
        self.header = selected_labels
        self.update_dropdwon()
    
    def update_dropdwon(self):
        for container in self.container_list.controls:
            dropdown = container.content.controls[0].controls[0]  # 드롭다운 참조
            dropdown.options = [ft.dropdown.Option(label) for label in self.header]
            dropdown.update()
    
    def get_sort_options(self):
        sort_options = []
        for container in self.container_list.controls:
            dropdown = container.content.controls[0].controls[0]  # 드롭다운 참조
            radio_group = container.content.controls[1].controls[0]  # 라디오 그룹 참조
            if dropdown.value and radio_group.value:
                sort_options.append((dropdown.value, radio_group.value == "Ascending"))
        return sort_options
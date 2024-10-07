import flet as ft
from ....components.selectable_dropdown import SelectableDropdown  # SelectableDropdown 클래스 임포트
from controller.columns_controller import ColumnsController

class SortOptionsContainer:
    def __init__(self, page, columns_controller:ColumnsController):
        self.page = page
        self.columns_controller = columns_controller
        self.container_list = ft.Column()  # 복사된 컨테이너들을 저장할 Column
        self.sort_option_checkbox = ft.Checkbox(
            label="정렬 옵션: 원하는 열을 선택하여 정렬합니다",
            value=False,
            on_change=lambda e: self.toggle_content_visibility(e.control.value)
        )
        self.content_visible = False 

    def build(self):
        """
        초기 UI 구조를 생성하여 반환합니다.
        :return: 컨테이너 객체
        """

        # 선택된 열 정보를 가져옴
        self.header = self.columns_controller.get_selected_columns()

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([
                        self.sort_option_checkbox,
                        self.create_btn(),
                    ]),
                    self.create_content()
                ],
                spacing=15
            )
        )

    def create_btn(self):
        """
        추가/삭제 버튼을 생성합니다.
        :return: 버튼이 포함된 컨테이너 객체
        """
        self.btn_container = ft.Container(
            content=ft.Row([
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
            ]),
        visible=False
        )
        return self.btn_container
    
    def create_content(self):
        """
        정렬 옵션 컨테이너의 초기 콘텐츠를 생성합니다.
        :return: 콘텐츠가 포함된 컨테이너 객체
        """
        self.container_list.controls.append(self.create_sort_option_container())
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.container_list,
                ]
            ),
            visible=False
        )
        return self.content
    
    def toggle_content_visibility(self, value):
        """
        정렬 옵션 컨테이너의 표시 상태를 토글합니다.
        :param value: 체크박스의 현재 값 (True/False)
        """
        self.btn_container.visible = value
        self.content.visible = value
        self.btn_container.update()
        self.content.update()

    def add_sort_option_container(self):
        """
        새로운 정렬 옵션 컨테이너를 추가합니다.
        """
        new_container = self.create_sort_option_container()
        self.container_list.controls.append(new_container)
        self.container_list.update()
        self.page.update()  # 페이지 전체를 업데이트하여 변경 사항 반영

    def delete_sort_option_container(self):
        """
        마지막 정렬 옵션 컨테이너를 제거합니다.
        """
        if self.container_list.controls:
            self.container_list.controls.pop()
            self.container_list.update()

    def create_sort_option_container(self):
        """
        SelectableDropdown 인스턴스를 사용하여 드롭다운을 포함하는 정렬 옵션 컨테이너를 생성합니다.
        :return: 새로 생성된 정렬 옵션 컨테이너 객체
        """
        # SelectableDropdown 인스턴스 생성
        dropdown = SelectableDropdown(
            page=self.page,
            controller=self.columns_controller,
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
        
        self.columns_controller.add_observer(dropdown)
        
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column([dropdown.build()]),
                    ft.Column([radio_group])
                ]
            )
        )

    def get_sort_options(self):
        """
        현재 설정된 정렬 옵션을 반환합니다.
        :return: 정렬 옵션 리스트 (드롭다운 값, 오름차순 여부)
        """
        sort_options = []

        for container in self.container_list.controls:
            try:
                dropdown = container.content.controls[0].controls[0]
                ascending_checkbox = container.content.controls[0].controls[1]

                selected_value = dropdown.get_selected_value() 
                is_ascending = ascending_checkbox.value 

                sort_options.append((selected_value,is_ascending))

            except (IndexError, AttributeError):
                # If any component is missing, use default values
                continue

        return sort_options

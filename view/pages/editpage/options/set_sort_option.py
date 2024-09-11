import flet as ft

class SortOptionsContainer:
    def __init__(self, page, columns_controller):
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
        print("[DEBUG] 추가/삭제 버튼 생성 중...")
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
        print("[DEBUG] 추가/삭제 버튼 생성 완료.")
        return self.btn_container
    
    def create_content(self):
        """
        정렬 옵션 컨테이너의 초기 콘텐츠를 생성합니다.
        :return: 콘텐츠가 포함된 컨테이너 객체
        """
        print("[DEBUG] 정렬 옵션 초기 콘텐츠 생성 중...")
        self.container_list.controls.append(self.create_sort_option_container())
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.container_list,
                ]
            ),
            visible=False
        )
        print("[DEBUG] 정렬 옵션 초기 콘텐츠 생성 완료.")
        return self.content
    
    def toggle_content_visibility(self, value):
        """
        정렬 옵션 컨테이너의 표시 상태를 토글합니다.
        :param value: 체크박스의 현재 값 (True/False)
        """
        print(f"[DEBUG] 정렬 옵션 토글: {value}")
        self.btn_container.visible = value
        self.content.visible = value
        self.btn_container.update()
        self.content.update()

    def add_sort_option_container(self):
        """
        새로운 정렬 옵션 컨테이너를 추가합니다.
        """
        print("[DEBUG] 정렬 옵션 컨테이너 추가 중...")
        new_container = self.create_sort_option_container()
        self.container_list.controls.append(new_container)
        self.container_list.update()
        self.page.update()  # 페이지 전체를 업데이트하여 변경 사항 반영
        print("[DEBUG] 정렬 옵션 컨테이너 추가 완료.")

    def delete_sort_option_container(self):
        """
        마지막 정렬 옵션 컨테이너를 제거합니다.
        """
        print("[DEBUG] 정렬 옵션 컨테이너 제거 중...")
        if self.container_list.controls:
            self.container_list.controls.pop()
            self.container_list.update()
            print("[DEBUG] 마지막 정렬 옵션 컨테이너 제거 완료.")

    def create_sort_option_container(self):
        """
        드롭다운과 라디오 버튼을 포함하는 정렬 옵션 컨테이너를 생성합니다.
        :return: 새로 생성된 정렬 옵션 컨테이너 객체
        """
        print("[DEBUG] 정렬 옵션 컨테이너 생성 중...")
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
        
        print("[DEBUG] 정렬 옵션 컨테이너 생성 완료.")
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column([dropdown]),
                    ft.Column([radio_group])
                ]
            )
        )

    def generate_options(self):
        """
        선택된 열 이름으로 드롭다운 옵션을 생성합니다.
        :return: 드롭다운 옵션 리스트
        """
        print("[DEBUG] 드롭다운 옵션 생성 중...")
        selected_columns = self.columns_controller.get_selected_columns()  # 선택된 열 이름만 가져옴
        options = [ft.dropdown.Option(col) for col in selected_columns]
        print(f"[DEBUG] 생성된 드롭다운 옵션: {options}")
        return options
    
    def on_column_selection_changed(self, selected_labels):
        """
        열 선택이 변경될 때 드롭다운의 옵션을 업데이트합니다.
        :param selected_labels: 선택된 열 이름 리스트
        """
        print(f"[DEBUG] 열 선택 변경 감지: {selected_labels}")
        self.header = selected_labels
        self.update_dropdown()

    def update_dropdown(self):
        """
        모든 드롭다운의 옵션을 업데이트합니다.
        """
        print("[DEBUG] 드롭다운 옵션 업데이트 중...")
        selected_columns = self.columns_controller.get_selected_columns()  # 선택된 열 이름만 가져옴
        for container in self.container_list.controls:
            dropdown = container.content.controls[0].controls[0]  # 드롭다운 참조
            dropdown.options = [ft.dropdown.Option(label) for label in selected_columns]
            dropdown.update()
        print("[DEBUG] 드롭다운 옵션 업데이트 완료.")
    
    def get_sort_options(self):
        """
        현재 설정된 정렬 옵션을 반환합니다.
        :return: 정렬 옵션 리스트 (드롭다운 값, 오름차순 여부)
        """
        sort_options = []
        for container in self.container_list.controls:
            dropdown = container.content

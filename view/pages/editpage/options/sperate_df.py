import flet as ft
from ....components.checkboxes_factory import create_checkbox_manager
from ....components.SearchField import SearchField
from ....components.selected_items_display import SelectedItemsDisplay
from ....components.selectable_dropdown import SelectableDropdown
from controller.columns_controller import ColumnsController
from controller.unique_values_controller import UniqueValuesController
from model.eventHandler import Event

class SperateDFOption:
    def __init__(self, 
                 page:ft.Page, 
                 columns_controller:ColumnsController, 
                 unique_values_controller:UniqueValuesController, 
                 error_handler):
        self.page = page
        self.columns_controller = columns_controller
        self.unique_value_controller = unique_values_controller

        # 선택된 항목을 표시하는 컴포넌트
        self.selected_items_display = SelectedItemsDisplay(
            page=self.page,
            controller=self.unique_value_controller,
            height=20, 
            mode='unique_values',
        )

        # 고유 값 체크박스 컨테이너
        self.unique_value_checkboxes = ft.Column(
            controls=[], visible=False, scroll=ft.ScrollMode.AUTO
        )

        # 팩토리 메서드를 통해 적절한 CheckboxManager 생성
        self.checkbox_manager = create_checkbox_manager(
            mode='unique_values',
            page=self.page,
            container=self.unique_value_checkboxes,
            error_handler=error_handler,
            controller=unique_values_controller
        )
        # 옵저버 등록
        unique_values_controller.add_observer(self.checkbox_manager)
        unique_values_controller.add_observer(self.selected_items_display)

        self.isSperate = ft.Checkbox(
            label="데이터 필터링: 특정 열의 데이터를 가져와 원하는 값만 선택합니다.",
            value=False,
            on_change=lambda e: self.on_checkbox_change(e.control.value),
        )

        self.radio_group = ft.RadioGroup(content=None)

        # SearchField 컴포넌트 초기화
        self.search_component = SearchField(
            on_search=self.search_unique_value,
            on_select_all=lambda e: self.select_all_columns(),
            on_unselect_all=lambda e:self.unselect_all_columns(),
            width=400,
        )

        # self.page.on_resize = self.on_resize
    def build(self):
        
        self.checkbox_manager.build()
        
        self.container = ft.Container(
            content=ft.Column(
                controls=[self.create_extension_panel(), self.create_content()]
            )
        )

        self.page.add(self.container)
        return self.container

    def on_checkbox_change(self, value):
        """체크박스 변경 시 콘텐츠의 가시성을 업데이트합니다."""
        self.content.visible = value
        if self.content.visible == True:
            self.dropdown.update_dropdown()
        self.page.update()

    def create_extension_panel(self):
        """check박스로 구성된 extension panel을 만듭니다."""
        self.extension_panel = ft.Container(content=self.isSperate)
        return self.extension_panel

    def create_content(self):
        """UI 콘텐츠를 생성하고 빌드합니다."""
        # SelectableDropdown 인스턴스 생성
        self.dropdown = SelectableDropdown(page=self.page, controller=self.columns_controller)
        self.dropdown.set_on_change(self.on_column_selection_changed)  # 외부 핸들러 연결
        
        self.columns_controller.add_observer(self.dropdown)

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(controls= [self.dropdown.build()]),
                    self.search_component.build(),  # SearchField 컴포넌트
                    self.selected_items_display.build(),  # 선택된 항목 표시 컴포넌트
                    ft.Container(self.unique_value_checkboxes),  # 빌드된 CheckboxManager 추가
                    self.select_save_options(),
                ]
            ),
            visible=False,
        )
        return self.content

    def on_column_selection_changed(self, e):
        """dropdown애서 열 선택이 변경되었을 때 CheckboxManager 업데이트."""
        selected_column = self.dropdown.get_selected_value()

        if selected_column:
            self.unique_value_controller.set_column_name(selected_column)

            self.update_checkboxes_with_unique_values(selected_column)
            
            self.selected_items_display.column_name = selected_column
            self.selected_items_display.update_display()

            self.unique_value_checkboxes.visible = True  # 가시성을 True로 설정

            self.page.update()

    def select_save_options(self):
        """저장 옵션을 선택합니다."""
        self.radio_group.content = ft.Row(
            controls=[
                ft.Radio(value="mono_file", label="한 파일 한 시트로 만들기"),
                ft.Radio(value="multi_sheets", label="한 파일에 여러 시트로 만들기"),
                ft.Radio(value="multi_files", label="여러 파일로 만들기"),
            ]
        )

        return ft.Row(controls=[ft.Text("저장 옵션"), self.radio_group])

    def search_unique_value(self, search_term:str) -> None:
        """검색어로 체크박스 필터링하고 UI를 업데이트합니다."""
        self.unique_value_controller.search_value(search_term)

    def select_all_columns(self):
        """전체선택"""
        self.unique_value_controller.select_all_unique_values()

    def unselect_all_columns(self):
        """전체선택 해제"""
        self.unique_value_controller.unselect_all_unique_values()

    def update_checkboxes_with_unique_values(self, selected_column):
        """선택된 열에 대한 고유 값을 사용하여 체크박스를 업데이트합니다."""
        self.checkbox_manager.create_checkboxes_container(column_name=selected_column, batch_size=50)

    def get_selected_save_option(self):
        """저장 옵션을 선택합니다."""
        return self.radio_group.value if self.radio_group else None


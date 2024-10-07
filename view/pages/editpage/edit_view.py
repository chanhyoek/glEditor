# view/edit_view.py

import flet as ft
from .tabs import Tabs
from .options_view import Options
from .excute_btn import ExcuteBtn
from controller.edit_controller import EditController
from ...components.SnackbarNotifier import SnackbarNotifier
from model.error_handler import ErrorHandler


class EditView:
    def __init__(self, 
                 page, 
                 metadata_controller, 
                 columns_controller, 
                 unique_values_controller ,
                 data_manipulator, 
                 task_manager,
                 initial_width, 
                 tabs_class=None, 
                 options_class=None):
        self.page = page
        self.metadata_controller = metadata_controller  
        self.columns_controller = columns_controller
        self.unique_values_controller = unique_values_controller
        self.data_manipulator = data_manipulator
        self.tabs_class = tabs_class or Tabs
        self.options_class = options_class or Options
        self.task_manager = task_manager
        self.snack_bar = SnackbarNotifier(page)
        self.initial_width = initial_width
        self.error_handler = ErrorHandler(self.page)
        # 필요한 객체를 나중에 초기화하도록 설정
        self.tabs = None
        self.options = None
        self.excute_btn = None

        # 컨트롤러 초기화
        self.controller = None

    def build(self):

        # UI 컴포넌트 초기화
        if self.tabs is None:
            self.tabs = self.tabs_class(self.page, 
                                        self.metadata_controller,
                                        self.error_handler)
        if self.options is None:
            self.options = self.options_class(self.page, 
                                              self.columns_controller, 
                                              self.unique_values_controller, 
                                              self.data_manipulator,
                                              self.error_handler)
        
        # 컨트롤러 인스턴스 생성
        if self.controller is None:
            self.controller = EditController(
                metadata_controller=self.metadata_controller,
                columns_controller = self.columns_controller,
                unique_values_controller = self.unique_values_controller,
                data_manipulator=self.data_manipulator,
                tabs=self.tabs,
                options=self.options,
                on_file_generated_callback=self.on_file_generated,
                task_manager=self.task_manager
            )
        
        if self.excute_btn is None:
            self.excute_btn = ExcuteBtn(
                options=self.options,
                page=self.page,
                snackbar_notifier=self.snack_bar,
                controller=self.controller, 
                task_manager=self.task_manager
            )

        tabs_view = self.tabs.build()
        options_view = self.options.build()
        excute_btn = self.excute_btn.build()

        self.page.add(tabs_view)
        self.page.add(options_view)
        self.page.add(excute_btn)

        header = ft.Container(
            ft.Text(
                    "열선택: 결과물에 포함되기 원하는 열만 선택하세요.", 
                    size=18, 
                    weight="bold"
                    ), 
                    padding=ft.padding.only(left=20)
                    )

        self.tabs.create_tabs()
                
        self.view = ft.Column(
            controls=[
                tabs_view,
                header,
                options_view,
                excute_btn,
            ],
            expand=True,
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START,
        )

        return self.view

    def on_file_generated(self, message: str, error: bool = False):
        """파일 생성이 완료되었을 때 호출되는 콜백."""
        self.snack_bar.show_snackbar(message, error)

    def set_width(self, width):
        """모든 페이지의 하위 요소를 동일한 넓이로 설정합니다."""
        self._set_control_width(self.view.controls, width)
        self.page.update()

    def _set_control_width(self, controls, width):
        """재귀적으로 하위 요소의 넓이를 설정합니다."""
        if not isinstance(controls, list):
            controls = [controls]

        for control in controls:
            # 크기 조정 제외 속성 확인
            if hasattr(control, 'resizeable') and not control.resizeable:
                continue  # 크기 조정하지 않음

            if isinstance(control, (ft.Column, ft.Row)):
                self._set_width_for_layout(control, width)
            elif isinstance(control, ft.Container):
                self._set_width_for_container(control, width)

    def _set_width_for_layout(self, layout_control, width):
        """ft.Columns, ft.Row에 대한 작업"""
        # 크기 조정 제외 속성 확인
        if hasattr(layout_control, 'resizeable') and not layout_control.resizeable:
            return  # 크기 조정하지 않음

        layout_control.width = width
        child_controls = self._get_child_controls(layout_control)
        if child_controls:
            self._set_control_width(child_controls, width)

    def _set_width_for_container(self, container_control, width):
        """ft.container 에 대한 작업"""
        # 크기 조정 제외 속성 확인
        if hasattr(container_control, 'resizeable') and not container_control.resizeable:
            return  # 크기 조정하지 않음

        container_control.width = width
        if container_control.content:
            if hasattr(container_control.content, 'controls'):
                child_controls = self._get_child_controls(container_control.content)
                if child_controls:
                    self._set_control_width(child_controls, width)
            elif hasattr(container_control.content, 'width'):
                # Container 내부의 content가 단일 컨트롤인 경우 width 설정
                container_control.content.width = width

    def _get_child_controls(self, control):
        """하위 요소를 체크"""
        if hasattr(control, 'controls') and control.controls:
            return control.controls
        elif hasattr(control, 'content') and control.content:
            if hasattr(control.content, 'controls'):
                return control.content.controls
            else:
                return [control.content]
        return None
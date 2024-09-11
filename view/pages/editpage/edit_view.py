# view/edit_view.py

import flet as ft
from .tabs import Tabs
from .options_view import Options
from .excute_btn import ExcuteBtn
from controller.edit_controller import EditController
from ...components.SnackbarNotifier import SnackbarNotifier

class EditView:
    def __init__(self, page, metadata_controller, columns_controller, unique_values_controller ,data_manipulator, task_manager, tabs_class=None, options_class=None):
        self.page = page
        self.metadata_controller = metadata_controller  
        self.columns_controller = columns_controller
        self.unique_values_controller = unique_values_controller
        self.data_manipulator = data_manipulator
        self.tabs_class = tabs_class or Tabs
        self.options_class = options_class or Options
        self.task_manager = task_manager
        self.snack_bar = SnackbarNotifier(page)
        
        # 필요한 객체를 나중에 초기화하도록 설정
        self.tabs = None
        self.options = None
        self.excute_btn = None

        # 컨트롤러 초기화
        self.controller = None

    def build(self):
        window_width = self.page.window_width

        # UI 컴포넌트 초기화
        if self.tabs is None:
            self.tabs = self.tabs_class(self.page, self.metadata_controller, window_width)
        if self.options is None:
            self.options = self.options_class(self.page, self.columns_controller, self.unique_values_controller, self.data_manipulator, window_width)
        
        # 컨트롤러 인스턴스 생성
        if self.controller is None:
            self.controller = EditController(
                metadata_controller=self.metadata_controller,  
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

        header = ft.Container(ft.Text("열선택: 결과물에 포함되기 원하는 열만 선택하세요.", size=18, weight="bold"), padding=ft.padding.only(left=20))

        self.tabs.create_tabs()
                
        return ft.Column(
            controls=[
                tabs_view,
                header,
                options_view,
                excute_btn,
            ],
            expand=True,
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.START
        )

    def on_file_generated(self):
        """파일 생성이 완료되었을 때 호출되는 콜백."""
        self.snack_bar.show_snackbar("파일 생성이 완료되었습니다.", success=True)

import flet as ft
from .tabs import Tabs
from .options_view import Options
from .excute_btn import ExcuteBtn
from model.file_generator import FileGenerator
from ...components.SnackbarNotifier import SnackbarNotifier

class EditView:
    def __init__(self, page, meta_data, data_manipulator, tabs_class=None, options_class=None):
        self.page = page
        self.meta_data = meta_data
        self.data_manipulator = data_manipulator
        self.tabs_class = tabs_class or Tabs
        self.options_class = options_class or Options

        self.snack_bar = SnackbarNotifier(page)
    
        # 필요한 객체를 나중에 초기화하도록 설정
        self.tabs = None
        self.file_generator = None
        self.options = None
        self.excute_btn = None

    def build(self):
        
        window_width = self.page.window_width

        if self.tabs is None:
            self.tabs = self.tabs_class(self.page, self.meta_data, window_width)
        if self.file_generator is None:
            self.file_generator = FileGenerator(self.data_manipulator, self.tabs)
        if self.options is None:
            self.options = self.options_class(self.page, self.meta_data, self.data_manipulator, window_width)
        if self.excute_btn is None:
            self.excute_btn = ExcuteBtn(
                options = self.options,
                meta_data=self.meta_data,
                page=self.page,
                tabs=self.tabs,
                file_generator=self.file_generator,
                notifier=self.snack_bar
            )

        tabs_view = self.tabs.build()
        options_view = self.options.build()
        excute_btn = self.excute_btn.build()

        self.page.add(tabs_view)
        self.page.add(options_view)
        self.page.add(excute_btn)

        header = ft.Container(ft.Text("편집옵션", size = 20, weight="bold"),padding=ft.padding.only(left =20))
        
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
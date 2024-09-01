import flet as ft
from .tabs import Tabs
from .options_view import Options
from ..excute_btn import ExcuteBtn
from model.file_generator import FileGenerator
from ...components.SnackbarNotifier import SnackbarNotifier

class EditView:
    def __init__(self, page, file_data, data_manipulator, tabs_class=None, options_class=None):
        self.page = page
        self.file_data = file_data
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
        # Lazy Initialization: 필요한 때에만 객체를 생성합니다.
        if self.tabs is None:
            self.tabs = self.tabs_class(self.page, self.file_data)
        if self.file_generator is None:
            self.file_generator = FileGenerator(self.data_manipulator, self.tabs)
        if self.options is None:
            self.options = self.options_class(self.page, self.file_data, self.data_manipulator)
        if self.excute_btn is None:
            self.excute_btn = ExcuteBtn(
                select_columns=self.options.select_columns_option,
                sperate_df=self.options.sperate_df_option,
                selected_df=self.options.selected_df_option,
                sort_options=self.options.sort_options,
                file_data=self.file_data,
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
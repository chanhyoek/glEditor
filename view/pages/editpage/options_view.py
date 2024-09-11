import flet as ft
from .options.select_columns import SelectColumnsOption
from .options.sperate_df import SperateDFOption
from .options.delete_accum import DeleteAccumsOption
from .options.only_select_df import OnlySelectedDFOption
from .options.set_sort_option import SortOptionsContainer
from model.error_handler import ErrorHandler

class Options:
    def __init__(self, page, columns_controller, unique_values_controller ,data_manipulator, window_width, select_columns_class=None, speratedf_class=None, delete_accums_class=None, selectd_df_class=None, sort_options_class=None):
        self.page = page
        self.columns_controller = columns_controller
        self.unique_values_controller = unique_values_controller
        self.data_manipulator = data_manipulator
        self.error_handler = ErrorHandler(self.page)
        self.window_width = window_width
        
        # 의존성 주입 또는 기본값 설정
        self.select_columns_class = select_columns_class or SelectColumnsOption
        self.speratedf_class = speratedf_class or SperateDFOption
        self.delete_accums_class = delete_accums_class or DeleteAccumsOption
        self.selecteddf_class = selectd_df_class or OnlySelectedDFOption
        self.sort_options_class = sort_options_class or SortOptionsContainer  

        # 지연 초기화
        self.select_columns_option = None
        self.sperate_df_option = None
        self.selected_df_option = None
        self.sort_options = None

    def initialize_options(self):
        """옵션 클래스의 인스턴스를 필요할 때 초기화합니다."""
        if not self.select_columns_option:
            self.select_columns_option = self.select_columns_class(self.page, self.columns_controller, self.error_handler, self.window_width)
        if not self.sperate_df_option:
            self.sperate_df_option = self.speratedf_class(self.page, self.columns_controller, self.unique_values_controller, self.error_handler, self.window_width)
        if not self.selected_df_option:
            self.selected_df_option = self.selecteddf_class(self.page)
        if not self.sort_options:
            self.sort_options = self.sort_options_class(self.page, self.columns_controller)
        
    def refresh_options(self):
        """각 옵션의 현재 상태를 새로고침하여 업데이트합니다."""
        self.select_columns_option = self.select_columns_class(self.page, self.columns_controller)
        self.sperate_df_option = self.speratedf_class(self.page, self.columns_controller)
        self.selected_df_option = self.selecteddf_class(self.page)
        self.sort_options = self.sort_options_class(self.page, self.columns_controller)

    def build(self):
        """UI 빌드를 관리합니다."""
        self.initialize_options()

        select_columns_container = self.select_columns_option.build()
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    select_columns_container,
                    ft.Container(
                        content=ft.Column([
                            ft.Text("선택옵션", size=18, weight="bold"),
                            self.sperate_df_option.build(),
                            self.sort_options.build(),
                            self.selected_df_option.build()
                        ]),
                        margin=ft.margin.only(top=20)
                    )
                ],
                expand=True,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(left=20, right=50),
            margin=ft.margin.only(bottom=20)
        )

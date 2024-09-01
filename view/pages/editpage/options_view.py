import flet as ft
from .options.select_columns import SelectColumnsOption
from .options.sperate_df import SperateDFOption
from .options.delete_accum import DeleteAccumsOption
from .options.only_select_df import OnlySelectedDFOption
from .options.set_sort_option import SortOptionsContainer

class Options:
    def __init__(self, page, file_data, data_manipulator, select_columns_class=None, speratedf_class=None, delete_accums_class=None, selectd_df_class=None, sort_options_class=None):
        self.page = page
        self.file_data = file_data
        self.data_manipulator = data_manipulator
        
        # 의존성 주입 또는 기본값 설정
        self.select_columns_class = select_columns_class or SelectColumnsOption
        self.speratedf_class = speratedf_class or SperateDFOption
        self.delete_accums_class = delete_accums_class or DeleteAccumsOption
        self.selecteddf_class = selectd_df_class or OnlySelectedDFOption
        self.sort_options_class = sort_options_class or SortOptionsContainer  

        # 지연 초기화(Lazy Initialization)
        self.select_columns_option = None
        self.sperate_df_option = None
        self.selected_df_option = None
        self.sort_options = None

    def initialize_options(self):
        """옵션 클래스의 인스턴스를 필요할 때 초기화합니다."""
        if not self.select_columns_option:
            self.select_columns_option = self.select_columns_class(self.page, self.file_data)
        if not self.sperate_df_option:
            self.sperate_df_option = self.speratedf_class(self.page, self.file_data)
        if not self.selected_df_option:
            self.selected_df_option = self.selecteddf_class(self.page)
        if not self.sort_options:
            self.sort_options = self.sort_options_class(self.page, self.file_data, None)

        # 이벤트 구독 관리
        self.manage_subscriptions()

    def manage_subscriptions(self):
        """옵션 클래스 간 이벤트 구독을 관리합니다."""
        # 구독을 한 번만 설정하고, 중복 방지
        if self.select_columns_option and self.sperate_df_option:
            self.select_columns_option.on_selection_change.subscribe(self.sperate_df_option.on_column_selection_changed)
        if self.select_columns_option and self.sort_options:
            self.select_columns_option.on_selection_change.subscribe(self.sort_options.on_column_selection_changed)

    def build(self):
        """UI 빌드를 관리합니다."""

        # 지연 초기화
        self.initialize_options()

        select_columns_container = self.select_columns_option.build()
        initial_selected_labels = self.select_columns_option.get_selected_labels()
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    select_columns_container,
                    ft.Container(
                        content= ft.Column([
                            ft.Text("선택옵션", size=18, weight="bold"),
                            self.sperate_df_option.build(selected_labels=initial_selected_labels),
                            self.sort_options.build(header=initial_selected_labels),
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
            padding=ft.padding.only(left=20),
            margin=ft.margin.only(bottom=50)
        )

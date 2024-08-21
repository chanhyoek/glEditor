import flet as ft
from .options.select_columns import SelectColumnsOption
from .options.sperate_df import SperateDFOption
from .options.delete_accum import DeleteAccumsOption
from .options.only_select_df import OnlySelectedDFOption
from .options.set_sort_option import SortOptionsContainer  # 새로 추가된 클래스 임포트

class Options:
    def __init__(self, page, file_data, data_manipulator, select_columns_class=None, speratedf_class=None, delete_accums_class=None, selectd_df_class=None, sort_options_class=None):
        self.page = page
        self.file_data = file_data
        self.data_manipulator = data_manipulator
        self.select_columns_class = select_columns_class or SelectColumnsOption
        self.speratedf_class = speratedf_class or SperateDFOption
        self.delete_accums_class = delete_accums_class or DeleteAccumsOption
        self.selecteddf_class = selectd_df_class or OnlySelectedDFOption
        self.sort_options_class = sort_options_class or SortOptionsContainer  

        # 각 옵션 클래스의 인스턴스 생성
        self.select_columns_option = self.select_columns_class(page, file_data)
        self.sperate_df_option = self.speratedf_class(page, file_data)
        # self.delete_accums_option = self.delete_accums_class(page)
        self.selected_df_option = self.selecteddf_class(page)
        self.sort_options = self.sort_options_class(page, file_data)  

    def build(self):
        print("Options")
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.select_columns_option.build(),
                    self.sperate_df_option.build(),
                    self.sort_options.build(),
                    # self.delete_accums_option.build(),
                    self.selected_df_option.build(),
                ],
                expand=True,
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(left=20),
            margin=ft.margin.only(bottom=50)
        )
import os
import pandas as pd
import flet as ft
from model.file_generator import FileGenerator
from ..components.SnackbarNotifier import SnackbarNotifier

class ExcuteBtn:
    def __init__(self, select_columns, sperate_df, delete_accums, selected_df, file_generator, notifier, file_data, page, tabs):
        self.select_columns = select_columns
        self.sperate_df = sperate_df
        self.delete_accums = delete_accums
        self.selected_df = selected_df
        self.file_generator = file_generator
        self.notifier = notifier
        self.file_data = file_data
        self.page = page 
        self.tabs = tabs
    
    def build(self):
        self.excute_btn = ft.Container(
            content=ft.ElevatedButton(
                "파일생성하기",
                icon=ft.icons.MERGE_TYPE,
                adaptive=True,
                on_click=lambda e: self.on_create_files_button_click(e),
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN,
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            padding=20
        )
        return self.excute_btn
    
    def set_options(self):
        self.options = {
            'checkboxes': self.select_columns.checkboxes,
            'unique_value_checkboxes': self.sperate_df.unique_value_checkboxes.controls,
            'select_unique_column': self.sperate_df.dropdown.value,
            'sperate_df_values': self.sperate_df.isSperate.value,
            'save_option': self.sperate_df.radio_group.value,
            'remove_accumulated_values': self.delete_accums.remove_accumlated_values,
            'only_selected_df': self.selected_df.only_selected_df
        }
    
    def on_create_files_button_click(self, e):
        self.set_options()
        if self.validate_before_making_files():
            # try:
                selected_columns = self.get_selected_columns()
                self.file_generator.generate(selected_columns, self.file_data, self.options)
                self.notifier.show_snackbar("생성이 완료되었습니다! 다운로드 폴더를 확인해주세요.")
            # except RuntimeError as err:
            #     self.notifier.show_snackbar(f"파일 생성 중 오류가 발생했습니다: {err}", error=True)

    def validate_before_making_files(self):
        if not any(checkbox.value for checkbox in self.options['checkboxes'].controls if isinstance(checkbox, ft.Checkbox)):
            self.notifier.show_snackbar("적어도 하나의 열을 선택해야 합니다.", error=True)
            return False
        
        if self.options['sperate_df_values']:
            if not any(checkbox.value for column in self.options['unique_value_checkboxes'] for checkbox in column.controls if isinstance(checkbox, ft.Checkbox)):
                self.notifier.show_snackbar("데이터를 분리할 고유값을 선택해야 합니다.", error=True)
                return False
            
            if not self.options['save_option']:
                self.notifier.show_snackbar("저장 옵션을 선택해야 합니다.", error=True)
                return False
            
            selected_dropdown_value = self.options['select_unique_column']
            if selected_dropdown_value not in [checkbox.label for checkbox in self.options['checkboxes'].controls if checkbox.value]:
                self.notifier.show_snackbar("데이터의 분리 기준이 되는 열을 포함하여야 합니다.", error=True)
                return False
        
        return True

    def get_selected_columns(self):
        try:
            return [checkbox.label for checkbox in self.options['checkboxes'].controls if checkbox.value]
        except Exception as e:
            self.notifier.show_snackbar(f"Error in get_selected_columns: {e}", error=True)
            return []
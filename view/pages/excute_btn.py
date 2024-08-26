import os
import pandas as pd
import flet as ft
from model.file_generator import FileGenerator
from ..components.SnackbarNotifier import SnackbarNotifier
from ..components.AlertModal import AlertModal

class ExcuteBtn:
    def __init__(self, select_columns, sperate_df, selected_df, sort_options, file_generator, notifier, file_data, page, tabs):
        self.select_columns = select_columns
        self.sperate_df = sperate_df
        self.selected_df = selected_df
        self.file_generator = file_generator
        self.notifier = notifier
        self.file_data = file_data
        self.sort_options = sort_options
        self.page = page 
        self.tabs = tabs
        self.operation_cancelled = False  # 작업 취소 여부 플래그

        # AlertModal 생성
        self.alert_modal = AlertModal(
            page,
            content=[
                ft.ProgressRing(),  # 애니메이션으로 로딩 표시
                ft.Text("파일 생성 중입니다. 잠시만 기다려주세요...", size=15),
            ],
            actions=[
                ft.TextButton(
                    "취소",
                    on_click=self.cancel_operation  # 취소 버튼에 작업 취소 메서드 연결
                )
            ]
        )
    
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
            'only_selected_df': self.selected_df.is_selected_df,
            'sort_options': self.sort_options.get_sort_options()  
        }
    
    def on_create_files_button_click(self, e):
        self.set_options()
        if self.validate_before_making_files():
            self.operation_cancelled = False  # 작업 취소 플래그 초기화
            self.file_generator.cancel_flag = False  # FileGenerator의 취소 플래그 초기화
            self.alert_modal.show()  # AlertModal 표시

            try:
                selected_columns = self.get_selected_columns()
                self.file_generator.generate(selected_columns, self.file_data, self.options)
                if not self.file_generator.cancel_flag:  # 작업이 취소되지 않은 경우에만 완료 메시지 표시
                    self.notifier.show_snackbar("생성이 완료되었습니다! 다운로드 폴더를 확인해주세요.")
            except RuntimeError as err:
                self.notifier.show_snackbar(f"파일 생성 중 오류가 발생했습니다: {err}", error=True)
            finally:
                self.alert_modal.close()  # 작업이 완료되거나 취소되었을 때 알림 창 닫기

    def validate_before_making_files(self):
        # 1. 적어도 하나의 열이 선택되었는지 확인
        if not any(checkbox.value for checkbox in self.options['checkboxes'].controls if isinstance(checkbox, ft.Checkbox)):
            self.notifier.show_snackbar("적어도 하나의 열을 선택해야 합니다.", error=True)
            return False

        # 2. 데이터 분리 옵션이 선택된 경우 추가 검사
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

        # 3. 정렬 옵션 유효성 검사 추가
        if 'sort_options' in self.options:
            for column, ascending in self.options['sort_options']:
                if not column:
                    self.notifier.show_snackbar("모든 정렬 옵션에 대해 열을 선택해야 합니다.", error=True)
                    return False
                if ascending is None:
                    self.notifier.show_snackbar("모든 정렬 옵션에 대해 정렬 방식을 선택해야 합니다.", error=True)
                    return False

        return True

    def get_selected_columns(self):
        try:
            return [checkbox.label for checkbox in self.options['checkboxes'].controls if checkbox.value]
        except Exception as e:
            self.notifier.show_snackbar(f"열을 수집하는데 문제가 발생하였습니다.: {e}", error=True)
            return []

    def cancel_operation(self, e=None):
        self.file_generator.cancel()  # FileGenerator의 작업 취소
        self.notifier.show_snackbar("작업이 취소되었습니다.", error=True)
        self.alert_modal.close()

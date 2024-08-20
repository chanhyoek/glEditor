import os
import pandas as pd
import flet as ft
from model.excel_data_parser import ExcelDataParser
from datetime import datetime

class FileGenerator:
    def __init__(self, data_manipulator, tabs):
        self.parser = ExcelDataParser()
        self.data_manipulator = data_manipulator
        self.tabs = tabs  

    def generate(self, selected_columns, file_data, options):
        try:
            # 활성화된 탭의 인덱스를 가져옴
            active_tab_index = self.tabs.active_index
            
            # 활성화된 탭의 인덱스를 기반으로 해당하는 DataFrame을 선택
            merged_df = self.merge_data(file_data, selected_columns, options['only_selected_df'], active_tab_index)
            all_dfs = self.split_data_if_required(merged_df, options['sperate_df_values'], options['unique_value_checkboxes'], options['select_unique_column'])
            self.save_data(all_dfs, options['save_option'])
        except Exception as e:
            raise RuntimeError(f"Error during file generation: {e}")

    def merge_data(self, file_data, selected_columns, only_selected_df, active_tab_index=None):
        all_dfs = []
        keys = list(file_data.keys())
        
        # 모든 파일의 데이터를 필터링하여 병합
        for key, data in file_data.items():
            self.data_manipulator.load_dataframe(data)
            for col in selected_columns:
                if col not in data.columns:
                    data[col] = pd.NA
            filtered_df = self.data_manipulator.select_columns(selected_columns)
            filtered_df["원본파일명"] = key
            all_dfs.append(filtered_df)

        # only_selected_df가 True일 때 활성화된 탭의 인덱스에 해당하는 DataFrame을 반환
        if only_selected_df and active_tab_index is not None:
            if 0 <= active_tab_index < len(all_dfs):
                return all_dfs[active_tab_index]
            else:
                raise IndexError(f"Active tab index {active_tab_index} is out of range.")
        
        # 그렇지 않은 경우, 모든 데이터프레임을 병합하여 반환
        return pd.concat(all_dfs, ignore_index=True)

    def split_data_if_required(self, merged_df, sperate_df_values, unique_value_checkboxes, select_unique_column):
        if sperate_df_values:
            selected_values = []

            # 각 컨테이너(Row 또는 Column)를 순회
            for container in unique_value_checkboxes:
                if isinstance(container, (ft.Row, ft.Column)):
                    # 컨테이너 내의 체크박스를 순회
                    for checkbox in container.controls:
                        if isinstance(checkbox, ft.Checkbox) and checkbox.value:
                            selected_values.append(checkbox.label)
            
            # 데이터프레임 로드 및 분리 작업 수행
            self.data_manipulator.load_dataframe(merged_df)
            return self.data_manipulator.split_dataframe_by_values(select_unique_column, selected_values)

        # 분리가 필요 없는 경우, 병합된 데이터프레임 반환
        return [merged_df]

    def save_data(self, all_dfs, save_option):
        output_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        if save_option == "one_file":
            output_file_path = self._generate_output_path("merged_file", output_folder)
            self.parser.create_file_with_multiple_sheets(all_dfs, output_file_path)
        elif save_option == "multi_files":
            self.parser.create_multiple_files(all_dfs, output_folder)
        else:
            output_file_path = self._generate_output_path("merged_file", output_folder)
            self.parser.create_single_file(all_dfs[0], output_file_path)

    def _generate_output_path(self, base_name, output_folder, extension=".xlsx"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{base_name}_{timestamp}{extension}"
        return os.path.join(output_folder, file_name)
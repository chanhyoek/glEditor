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
            active_tab_index = self.tabs.active_index
            
            merged_df = self.merge_data(file_data, selected_columns, options['only_selected_df'],active_tab_index)
            
            if 'sort_options' in options and options['sort_options']:
                merged_df = self.sort_dataframe(merged_df, options['sort_options'])

            # if 'remove_accumulated_values' in options and options['remove_accumulated_values'] == True:
            #     merged_df = self.delete_accum_dataframe(merged_df)
            
            all_dfs = self.split_data_if_required(merged_df, options['sperate_df_values'], options['unique_value_checkboxes'], options['select_unique_column'])
            self.save_data(all_dfs, options['save_option'])
        except Exception as e:
            raise RuntimeError(f"Error during file generation: {e}")
        
    def sort_dataframe(self, df, sort_options):
        # sort_options는 [(열 이름, 오름차순 여부)] 형태의 리스트
        sort_columns = [col for col, _ in sort_options]
        ascending_list = [asc for _, asc in sort_options]
        return df.sort_values(by=sort_columns, ascending=ascending_list)
    
    def delete_accum_dataframe(self, df):
        print("start")
        return self.data_manipulator.filter_accumulated_values(df)
    
    def merge_data(self, file_data, selected_columns, is_selected_df, active_tab_index=None):
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
        
        if is_selected_df:
            if active_tab_index is not None and 0 <= active_tab_index < len(all_dfs):
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
            output_file_path = self._generate_output_path("편집후파일", output_folder)
            self.parser.create_file_with_multiple_sheets(all_dfs, output_file_path)
        elif save_option == "multi_files":
            self.parser.create_multiple_files(all_dfs, output_folder)
        else:
            output_file_path = self._generate_output_path("편집후파일", output_folder)
            self.parser.create_single_file(all_dfs[0], output_file_path)

    def _generate_output_path(self, base_name, output_folder, extension=".xlsx"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{base_name}_{timestamp}{extension}"
        return os.path.join(output_folder, file_name)
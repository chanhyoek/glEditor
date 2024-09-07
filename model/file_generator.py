import os
import pandas as pd
import flet as ft
from .excel_data_parser import ExcelDataParser
from datetime import datetime

class FileGenerator:
    def __init__(self, data_manipulator, tabs):
        self.parser = ExcelDataParser()
        self.data_manipulator = data_manipulator
        self.tabs = tabs  


    async def get_file_data(self, meta_data):
        file_data = {}
        for file_path in meta_data.get_all_file_path():
            single_data = await self.parser.get_single_data(file_path)
            file_data.update(single_data)        
        return file_data

    async def generate(self, selected_columns, meta_data, options):
        try:
            print("파일생성을 시작합니다.")
            active_tab_index = self.tabs.active_index
            
            file_data = await self.get_file_data(meta_data)

            # 데이터 병합
            merged_df = self.merge_data(file_data, selected_columns, options['only_selected_df'], active_tab_index)

            # # 작업 중지 확인
            # if is_cancelled():
            #     print("작업이 취소되었습니다. 병합 중단.")
            #     return
            
            # 데이터 정렬
            if 'sort_options' in options and options['sort_options']:
                merged_df = self.sort_dataframe(merged_df, options['sort_options'])
                
            
            # 작업 중지 확인
            # if is_cancelled():
            #     print("작업이 취소되었습니다. 정렬 중단.")
            #     return

            # 데이터 분리 및 저장
            all_dfs = self.split_data_if_required(merged_df, options['sperate_df_values'], options['unique_value_checkboxes'], options['select_unique_column'])
            
            # 작업 중지 확인
            # if is_cancelled():
            #     print("작업이 취소되었습니다. 저장 중단.")
            #     return

            self.save_data(all_dfs, options['save_option'])
        except Exception as e:
            raise RuntimeError(f"파일 생성 중 오류가 발생했습니다: {e}")
        
    def sort_dataframe(self, df, sort_options):
        sort_columns = [col for col, _ in sort_options]
        ascending_list = [asc for _, asc in sort_options]
        print(sort_columns, ascending_list)
        return df.sort_values(by=sort_columns, ascending=ascending_list)
    
    def delete_accum_dataframe(self, df):
        return self.data_manipulator.filter_accumulated_values(df)
    
    def merge_data(self, file_data, selected_columns, is_selected_df, active_tab_index=None):
        all_dfs = []

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
        
        return pd.concat(all_dfs, ignore_index=True)

    def split_data_if_required(self, merged_df, sperate_df_values, unique_value_checkboxes, select_unique_column):
        if sperate_df_values == True:
            selected_values = []
            
            for text in unique_value_checkboxes:
                if isinstance(text, ft.Text):
                    selected_values.append(text.value)
            
            self.data_manipulator.load_dataframe(merged_df)
            return self.data_manipulator.split_dataframe_by_values(select_unique_column, selected_values)
        
        return [merged_df]

    def save_data(self, all_dfs, save_option):
        output_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        output_file_path = self._generate_output_path("편집후파일", output_folder)
        if save_option == "multi_sheets":
            self.parser.create_file_with_multiple_sheets(all_dfs, output_file_path)
        elif save_option == "multi_files":
            self.parser.create_multiple_files(all_dfs, output_folder)
        elif save_option == "mono_file":
            self.parser.create_file_with_onesheets(all_dfs, output_file_path)
        else:
            self.parser.create_single_file(all_dfs[0], output_file_path)

    def _generate_output_path(self, base_name, output_folder, extension=".xlsx"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{base_name}_{timestamp}{extension}"
        return os.path.join(output_folder, file_name)


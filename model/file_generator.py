import os
import pandas as pd
from .excel_data_parser import ExcelDataParser
from datetime import datetime
from controller.columns_controller import ColumnsController
from controller.meta_data_controller import MetadataController
from .data_manipulator import DataManipulator
from controller.unique_values_controller import UniqueValuesController
from view.components.AlertModal import AlertModal

class FileGenerator:
    def __init__(self, 
                 data_manipulator:DataManipulator, 
                 columns_controller:ColumnsController, 
                 unique_value_controller:UniqueValuesController,
                 tabs):
        self.parser = ExcelDataParser()
        self.data_manipulator = data_manipulator
        self.columns_controller = columns_controller 
        self.unique_value_controller = unique_value_controller
        self.tabs = tabs  


    async def get_file_data(self, metadata_controller: MetadataController):
        
        self.metadata_controller = metadata_controller

        file_data = {}
        
        # 메타데이터 컨트롤러가 제공하는 모든 파일 경로를 반복합니다.
        for file_path in self.metadata_controller.get_all_file_paths():
            # 각 파일에 대해 데이터를 비동기적으로 가져옵니다.
            single_data = await self.parser.get_single_data(file_path)
            
            # 가져온 데이터를 반복하여 file_data 딕셔너리에 추가합니다.
            for key, df in single_data.items():
                if key not in file_data:
                    file_data[key] = df
                else:
                    # 선택 사항: 중복 키가 존재하는 경우 처리(예: 병합 또는 덮어쓰기)
                    pass
            
        return file_data

    async def generate(self, meta_data, options, alert_modal:AlertModal):
        
        self.alert_modal = alert_modal
        
        try:
            active_tab_index = self.tabs.active_index
            
            if self.alert_modal:
                self.alert_modal.update_content_text("파일 데이터를 불러오는 중...")

            file_data = await self.get_file_data(meta_data)


            if self.alert_modal:
                self.alert_modal.update_content_text("데이터 병합 중...")

            # 데이터 병합
            merged_df = self.merge_data(file_data)

            
            if self.alert_modal:
                self.alert_modal.update_content_text("데이터 정렬 중...")
            
            # 데이터 정렬
            if 'sort_options' in options and options['sort_options']:
                merged_df = self.sort_dataframe(merged_df, options['sort_options'])
                
            
            if self.alert_modal:
                self.alert_modal.update_content_text("데이터 분리 중...")
            # 데이터 분리 및 저장
            all_dfs = self.split_data_if_required(merged_df, options['sperate_df_values'])
            
            if self.alert_modal:
                self.alert_modal.update_content_text("데이터 저장 중...")

            self.save_data(all_dfs, options['save_option'])
        except Exception as e:
            raise RuntimeError(f"{e}")
        
    def sort_dataframe(self, df, sort_options):
        sort_columns = [col for col, _ in sort_options]
        ascending_list = [asc for _, asc in sort_options]
        return df.sort_values(by=sort_columns, ascending=ascending_list)
    
    def delete_accum_dataframe(self, df):
        return self.data_manipulator.filter_accumulated_values(df)
    
    def merge_data(self, file_data):
        """
        여러 파일 데이터를 메타데이터에서 is_select가 True인 항목만 병합하는 함수입니다.
        """
        all_dfs = []

        # 선택된 열 정보 가져오기
        selected_columns = self.columns_controller.get_selected_columns()

        # 선택된 키만 가져오기
        selected_keys = self.metadata_controller.get_selected_key()

        for key, data in file_data.items():
            # 메타데이터에서 is_select가 True인 항목만 처리
            if key in selected_keys:
                self.data_manipulator.load_dataframe(data)

                # 선택된 열이 데이터에 없을 경우 NA 값으로 추가
                for col in selected_columns:
                    if col not in data.columns:
                        data[col] = pd.NA

                # 선택된 열만 필터링
                filtered_df = self.data_manipulator.select_columns(selected_columns)
                filtered_df["원본파일명"] = key
                all_dfs.append(filtered_df)

        # 모든 데이터프레임을 하나로 병합
        return pd.concat(all_dfs, ignore_index=True)

    def split_data_if_required(self, merged_df, sperate_df_values,):
        if sperate_df_values == True:

            select_unique_column = self.unique_value_controller.get_column_name()
            selected_values = self.unique_value_controller.get_selected_unique_values(select_unique_column)
            
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


import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import Dict, List, Union
import os

class ExcelDataParser:
    def __init__(self):
        self.dataframes: Dict[str, Union[pd.DataFrame, Dict[str, pd.DataFrame]]] = {}
        self.MAX_ROWS_PER_SHEET = 1048576  # 엑셀의 최대 행 수

    def is_excel_file(self, file_path: str) -> bool:
        return file_path.lower().endswith(('.xlsx', '.xls', '.xlsb', '.XLSX', '.XLS', '.XLSB'))

    def is_csv_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.csv')

    async def read_excel(self, file_path: str) -> Dict[str, pd.DataFrame]:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            def read_excel_file():
                if file_path.lower().endswith('.xls'):
                    return pd.read_excel(file_path, sheet_name=None, engine='xlrd')
                elif file_path.lower().endswith('.xlsb'):
                    return pd.read_excel(file_path, sheet_name=None, engine='pyxlsb')
                else:
                    return pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            sheets = await loop.run_in_executor(executor, read_excel_file)
            return sheets
        
    async def read_csv(self, file_path: str) -> pd.DataFrame:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            def read_csv_chunks():
                chunks = pd.read_csv(file_path, chunksize=10000)
                return pd.concat(chunks, ignore_index=True)
            df = await loop.run_in_executor(executor, read_csv_chunks)
            return df

    async def get_single_data(self, file_path: str) -> Dict[str, pd.DataFrame]:
        result = {}
        try:
            file_name = os.path.basename(file_path).split('.')[0]
            if self.is_excel_file(file_path):
                sheets = await self.read_excel(file_path)
                for sheet_name, df in sheets.items():
                    result[f"{file_name}_{sheet_name}"] = df
            elif self.is_csv_file(file_path):
                df = await self.read_csv(file_path)
                result[file_name] = df
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            raise e
        return result

    async def get_multiple_data(self, file_paths: List[str]) -> Dict[str, pd.DataFrame]:
        tasks = [self.get_single_data(file_path) for file_path in file_paths]
        try:
            results = await asyncio.gather(*tasks)
            combined_results = {}
            for result in results:
                combined_results.update(result)
            self.dataframes = combined_results
            return self.dataframes
        except Exception as e:
            raise e

    def create_single_file(self, df: pd.DataFrame, output_path: str) -> None:
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            num_sheets = -(-len(df) // self.MAX_ROWS_PER_SHEET)  # 시트 수 계산
            for i in range(num_sheets):
                start_row = i * self.MAX_ROWS_PER_SHEET
                end_row = min((i + 1) * self.MAX_ROWS_PER_SHEET, len(df))  # 최종 행은 데이터프레임의 길이를 초과하지 않도록 함
                split_df = df.iloc[start_row:end_row]  # iloc를 사용하여 정확한 슬라이싱
                sheet_name = f"Sheet_{i+1}" if num_sheets > 1 else "Sheet1"
                split_df.to_excel(writer, sheet_name=sheet_name, index=False)

    def create_multiple_files(self, dfs: Dict[str, pd.DataFrame], output_folder: str) -> None:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
        for file_name, df in dfs.items():
            output_path = os.path.join(output_folder, f"{file_name}.xlsx")
            self.create_single_file(df, output_path)

    def create_file_with_multiple_sheets(self, dfs: Dict[str, pd.DataFrame], output_path: str) -> None:
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            for sheet_name, df in dfs.items():
                num_sheets = -(-len(df) // self.MAX_ROWS_PER_SHEET)  # 시트 수 계산
                for i in range(num_sheets):
                    start_row = i * self.MAX_ROWS_PER_SHEET
                    end_row = min((i + 1) * self.MAX_ROWS_PER_SHEET, len(df))  # 최종 행은 데이터프레임의 길이를 초과하지 않도록 함
                    split_df = df.iloc[start_row:end_row]  # iloc를 사용하여 정확한 슬라이싱
                    split_sheet_name = f"{sheet_name}_{i+1}" if num_sheets > 1 else sheet_name
                    split_df.to_excel(writer, sheet_name=split_sheet_name, index=False)
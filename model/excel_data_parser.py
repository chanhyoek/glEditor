import pandas as pd
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Union
import os

class ExcelDataParser:
    def __init__(self):
        self.dataframes: Dict[str, Union[pd.DataFrame, Dict[str, pd.DataFrame]]] = {}

    def is_excel_file(self, file_path: str) -> bool:
        return file_path.lower().endswith(('.xlsx', '.xls', '.XLSX', '.XLS'))

    def is_csv_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.csv')

    async def read_excel(self, file_path: str) -> Dict[str, pd.DataFrame]:
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            def read_excel_file():
                if file_path.lower().endswith('.xls'):
                    return pd.read_excel(file_path, sheet_name=None, engine='xlrd')
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
                print(f"Reading Excel file: {file_path}")
                sheets = await self.read_excel(file_path)
                for sheet_name, df in sheets.items():
                    result[f"{file_name}_{sheet_name}"] = df
            elif self.is_csv_file(file_path):
                print(f"Reading CSV file: {file_path}")
                df = await self.read_csv(file_path)
                result[file_name] = df
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
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
            print(f"Error in get_multiple_data: {e}")
            raise e

    def create_single_file(self, df: pd.DataFrame, output_path: str) -> None:
        df.to_excel(output_path, index=False)

    def create_multiple_files(self, dfs: Dict[str, pd.DataFrame], output_folder: str) -> None:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    
        for file_name, df in dfs.items():
            output_path = os.path.join(output_folder, f"{file_name}.xlsx")
            df.to_excel(output_path, index=False)

    def create_file_with_multiple_sheets(self, dfs: Dict[str, pd.DataFrame], output_path: str) -> None:
        with pd.ExcelWriter(output_path) as writer:
            for sheet_name, df in dfs.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

import pandas as pd
import asyncio
from concurrent.futures import ProcessPoolExecutor
import os
import chardet
from typing import Dict, List


class ExcelDataParser:
    def __init__(self):
        self.dataframes: Dict[str, pd.DataFrame] = {}
        self.MAX_ROWS_PER_SHEET = 1048576
        self.LARGE_FILE_THRESHOLD = 100 * 1024 * 1024  # 100MB 이상을 큰 파일로 간주

    async def get_single_data(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """단일 파일을 처리하고 데이터를 반환합니다."""
        try:
            return await self.read_file(file_path)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return {}
    
    async def read_file(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """파일 크기에 따라 적절한 방식으로 파일을 읽습니다."""
        if await self.is_large_file(file_path):
            return await self.read_large_file(file_path)
        else:
            return self.read_small_file(file_path)

    async def is_large_file(self, file_path: str) -> bool:
        """파일 크기를 확인하여 큰 파일인지 여부를 반환합니다."""
        return os.path.getsize(file_path) > self.LARGE_FILE_THRESHOLD

    async def read_large_file(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """큰 파일을 병렬로 처리합니다."""
        loop = asyncio.get_running_loop()
        with ProcessPoolExecutor() as executor:
            if file_path.lower().endswith('.csv'):
                df = await loop.run_in_executor(executor, self.read_csv_file, file_path)
                return {os.path.splitext(os.path.basename(file_path))[0]: df}
            else:
                sheets = await loop.run_in_executor(executor, self.read_excel_file, file_path)
                return {f"{os.path.splitext(os.path.basename(file_path))[0]}_{sheet}": df for sheet, df in sheets.items()}

    def read_small_file(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """작은 파일을 동기적으로 읽어 처리합니다."""
        if file_path.lower().endswith('.csv'):
            encoding = self.detect_encoding(file_path)
            df = pd.read_csv(file_path, encoding=encoding)
            return {os.path.splitext(os.path.basename(file_path))[0]: df}
        else:
            sheets = pd.read_excel(file_path, sheet_name=None)
            return {f"{os.path.splitext(os.path.basename(file_path))[0]}_{sheet}": df for sheet, df in sheets.items()}

    def read_excel_file(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """Excel 파일을 동기적으로 읽어들이는 함수입니다."""
        file_extension = file_path.lower().split('.')[-1]
        engine = {'xls': 'xlrd', 'xlsb': 'pyxlsb'}.get(file_extension, 'openpyxl')
        return pd.read_excel(file_path, sheet_name=None, engine=engine)

    @staticmethod
    def detect_encoding(file_path: str) -> str:
        """파일의 인코딩 방식을 감지하여 반환합니다."""
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read(10000)) 
            encoding = result['encoding']
            return encoding

    def read_csv_file(self, file_path: str) -> pd.DataFrame:
        """CSV 파일을 동기적으로 읽어들이는 함수 (인코딩 자동 감지 포함)."""
        try:
            encoding = self.detect_encoding(file_path)
            chunks = pd.read_csv(file_path, chunksize=10000, encoding=encoding)
            df = pd.concat(chunks, ignore_index=True)
            return df
        except UnicodeDecodeError:
            print(f"디코딩 오류 발생: {file_path}, 인코딩: {encoding}")
            return pd.DataFrame()
        except pd.errors.EmptyDataError:
            print(f"{file_path}에 데이터가 없습니다.")
            return pd.DataFrame() 
        except pd.errors.ParserError as e:
            print(f"{file_path}에서 구문 분석 오류 발생: {e}")
            return pd.DataFrame() 
        except Exception as e:
            print(f"CSV 파일 {file_path} 읽기 중 오류 발생: {e}")
            return pd.DataFrame()

    def create_single_file(self, df: pd.DataFrame, output_path: str) -> None:
        """단일 시트로 구성된 하나의 파일을 만듭니다."""
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            num_sheets = -(-len(df) // self.MAX_ROWS_PER_SHEET)
            for i in range(num_sheets):
                start_row = i * self.MAX_ROWS_PER_SHEET
                end_row = min((i + 1) * self.MAX_ROWS_PER_SHEET, len(df))
                split_df = df.iloc[start_row:end_row]
                sheet_name = f"Sheet_{i+1}" if num_sheets > 1 else "Sheet1"
                split_df.to_excel(writer, sheet_name=sheet_name, index=False)

    def create_multiple_files(self, dfs: Dict[str, pd.DataFrame], output_folder: str) -> None:
        """단일 시트로 구성된 여러개의 파일을 생성합니다."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for file_name, df in dfs.items():
            output_path = os.path.join(output_folder, f"{file_name}.xlsx")
            self.create_single_file(df, output_path)

    def create_file_with_multiple_sheets(self, dfs: Dict[str, pd.DataFrame], output_path: str) -> None:
        """다중시트로 구성된 여러개의 파일을 생성합니다."""      
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            for sheet_name, df in dfs.items():
                num_sheets = -(-len(df) // self.MAX_ROWS_PER_SHEET)
                for i in range(num_sheets):
                    start_row = i * self.MAX_ROWS_PER_SHEET
                    end_row = min((i + 1) * self.MAX_ROWS_PER_SHEET, len(df))
                    split_df = df.iloc[start_row:end_row]
                    split_sheet_name = f"{sheet_name}_{i+1}" if num_sheets > 1 else sheet_name
                    split_df.to_excel(writer, sheet_name=split_sheet_name, index=False)

    def create_file_with_onesheets(self, dfs: Dict[str, pd.DataFrame], output_path: str) -> None:
        merged_df = pd.concat(dfs.values(), ignore_index=True)
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            num_sheets = -(-len(merged_df) // self.MAX_ROWS_PER_SHEET)  # 필요한 시트 수 계산 (올림)
            for i in range(num_sheets):
                start_row = i * self.MAX_ROWS_PER_SHEET
                end_row = min((i + 1) * self.MAX_ROWS_PER_SHEET, len(merged_df))
                split_df = merged_df.iloc[start_row:end_row]
                sheet_name = f"sheet{i + 1}"
                split_df.to_excel(writer, sheet_name=sheet_name, index=False)

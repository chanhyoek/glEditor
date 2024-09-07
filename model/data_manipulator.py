import pandas as pd
from typing import List, Dict

class DataManipulator:
    def __init__(self):
        self.df = None
        self.keywords = ["합계", "누계", "월계", "일계"]
        self.all_set_data = None
        self.all_header = None

    def load_dataframe(self, df: pd.DataFrame) -> None:
        self.df = df

    def get_header(self) -> List[str]:
        if self.df is not None:
            return self.df.columns.tolist()
        else:
            raise ValueError("Dataframe is not loaded")
        
    def get_common_headers(self, file_data: Dict[str, pd.DataFrame]) -> List[str]:
        common_headers = set(next(iter(file_data.values())).columns)
        for df in file_data.values():
            common_headers.intersection_update(df.columns)
        return list(common_headers)

    def initialize_data(self, file_data: Dict[str, pd.DataFrame]) -> None:
        """
        파일 데이터를 초기화합니다.
        - 모든 데이터프레임에 "원본파일명" 열을 추가하고, 공통되지 않은 열은 NaN으로 채웁니다.
        - 모든 데이터를 병합하여 all_set_data로 저장합니다.
        - 병합된 데이터에서 헤더를 추출하여 all_header로 저장합니다.
        """
        # 공통 헤더 추출
        common_headers = self.get_common_headers(file_data)
        
        # 각 데이터프레임에 "원본파일명" 열 추가 및 공통되지 않은 열 NaN 처리
        dfs = []
        for file_name, df in file_data.items():
            df['원본파일명'] = file_name
            for col in common_headers:
                if col not in df.columns:
                    df[col] = pd.NA
            dfs.append(df[common_headers + ['원본파일명']])
        
        # 모든 데이터프레임을 병합하여 all_set_data로 저장
        self.all_set_data = pd.concat(dfs, ignore_index=True)
        
        # 병합된 데이터에서 헤더를 추출하여 all_header로 저장
        self.all_header = self.all_set_data.columns.tolist()

    def get_unique_values(self, column_name: str) -> List[str]:
        if self.df is not None and column_name in self.df.columns:
            return self.df[column_name].astype(str).unique().tolist()
        else:
            raise ValueError("Invalid column name or dataframe is not loaded")

    def concat_dataframes(self, dfs: List[pd.DataFrame], headers: List[str]) -> pd.DataFrame:
        for df in dfs:
            df.columns = headers
        return pd.concat(dfs, ignore_index=True)
    
    def concat_dataframes_with_common_headers(self, dfs: List[pd.DataFrame], common_headers: List[str]) -> pd.DataFrame:
        filtered_dfs = [df[common_headers] for df in dfs]
        return pd.concat(filtered_dfs, ignore_index=True)

    def split_dataframe(self, column_name: str) -> Dict[str, pd.DataFrame]:
        if self.df is not None and column_name in self.df.columns:
            unique_values = self.df[column_name].unique()
            return {str(value): self.df[self.df[column_name] == value].reset_index(drop=True) for value in unique_values}
        else:
            raise ValueError("Invalid column name or dataframe is not loaded")
    
    def select_columns(self, columns: List[str]) -> pd.DataFrame:
        if self.df is not None:
            missing_columns = [col for col in columns if col not in self.df.columns]
            if missing_columns:
                raise ValueError(f"Columns {missing_columns} are not in the dataframe")
            return self.df[columns]
        else:
            raise ValueError("Dataframe is not loaded")
    
    def filter_accumulated_values(self, df: pd.DataFrame, keywords: List[str]) -> pd.DataFrame:
        # 데이터프레임의 각 셀에서 공백을 제거하고 필터링
        return df[~df.apply(lambda row: any(keyword in str(cell).replace(" ", "") for cell in row for keyword in self.keywords), axis=1)]

    def remove_accumulated_values(self) -> pd.DataFrame:
        if self.df is not None:
            return self.filter_accumulated_values(self.df, self.keywords)
        else:
            raise ValueError("데이터가 로드되지 않았습니다.")

    def split_dataframe_by_values(self, column_name: str, values: List[str]) -> Dict[str, pd.DataFrame]:
        if self.df is not None and column_name in self.df.columns:
            split_dfs = {value: self.df[self.df[column_name] == value].reset_index(drop=True) for value in values}
            return split_dfs
        else:
            raise ValueError("유효하지 않은 열이름이거나, 데이터가 로드되지 않았습니다.")

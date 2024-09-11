from model.meta_data_model import MetadataModel
from typing import List, Dict, Union 
import pandas as pd

class MetadataController:
    def __init__(self, model: MetadataModel):
        self.model = model

    def generate_metadata(self, file_path: str, data: Dict[str, pd.DataFrame]) -> None:
        """파일의 메타데이터를 생성하고 모델에 저장합니다."""
        for key, df in data.items():
            headers = [
                {"col_name": col, "is_select": False}  # 초기화 시 선택 상태는 False로 설정
                for col in df.columns
            ]
            first_5_rows = df.head(5)
            unique_values = {
                col: {value: False for value in df[col].dropna().unique().tolist()}  # 모든 고유 값의 선택 상태 초기화
                for col in df.columns
            }
            
            self.model.set_metadata(key, file_path, headers, first_5_rows, unique_values)

    def update_column_selection(self, key: str, column_name: str, is_select: bool) -> None:
        """지정된 열의 선택 상태를 업데이트합니다."""
        metadata = self.model.get_metadata(key)
        headers = metadata.get("headers", [])

        # 열 선택 상태 업데이트
        for header in headers:
            if header["col_name"] == column_name:
                header["is_select"] = is_select
                break

        # 업데이트된 헤더 정보를 다시 설정
        self.model.set_metadata(
            key,
            metadata["file_path"],
            headers,
            metadata["first_5_rows"],
            metadata["unique_values"]
        )

    def update_unique_value_selection(self, key: str, column_name: str, value_name: str, is_selected: bool) -> None:
        """특정 열 값의 선택 상태를 업데이트합니다."""
        metadata = self.model.get_metadata(key)
        unique_values = metadata.get("unique_values", {})

        # 고유 값 선택 상태 업데이트
        if column_name in unique_values:
            unique_values[column_name][value_name] = is_selected

        # 업데이트된 고유 값 정보를 다시 설정
        self.model.set_metadata(
            key,
            metadata["file_path"],
            metadata["headers"],
            metadata["first_5_rows"],
            unique_values
        )

    def get_first_5_rows(self, key: str) -> pd.DataFrame:
        """지정된 시트의 첫 5행을 반환합니다."""
        return self.model.get_metadata(key).get("first_5_rows", pd.DataFrame())
    
    def get_all_columns_properties(self) -> List[Dict[str, Union[str, bool]]]:
        """모든 열의 이름과 속성을 반환합니다."""
        return self.aggregator.get_all_columns_properties()

    def get_headers(self, key: str) -> List[Dict[str, Union[str, bool]]]:
        """지정된 시트의 헤더를 반환합니다."""
        return self.model.get_metadata(key).get("headers", [])

    def get_unique_values(self, key: str, column_name: str) -> Dict[str, bool]:
        """지정된 시트의 특정 열에 대한 고유 값을 반환합니다."""
        return self.model.get_metadata(key).get("unique_values", {}).get(column_name, {})
    
    def get_file_path(self, key: str) -> str:
        """지정된 키에 대한 파일 경로를 반환합니다."""
        return self.model.get_metadata(key).get("file_path", "")

    def reset_metadata(self) -> None:
        """모델의 메타데이터를 초기화합니다."""
        self.model.reset_metadata()

    def get_selected_headers(self, key: str) -> List[str]:
        """선택된 (is_select=True) 헤더만 반환합니다."""
        headers = self.get_headers(key)
        return [header['col_name'] for header in headers if header.get('is_select', False)]

    def get_selected_unique_values(self, key: str, column_name: str) -> List[Union[str, int, float]]:
        """선택된 (is_select=True) 고유 값만 반환합니다."""
        unique_values = self.get_unique_values(key, column_name)
        return [value for value, is_selected in unique_values.items() if is_selected]

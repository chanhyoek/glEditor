from typing import List, Union, Dict
from model.unique_values_model import UniqueValues
import pandas as pd

class UniqueValuesController:
    def __init__(self, unique_values: UniqueValues):
        self.unique_values = unique_values

    def initialize_unique_values(self, data: Dict[str, pd.DataFrame]) -> None:
        """파일 데이터를 받아 고유값을 초기화합니다."""
        self.unique_values.remove_all_data()

        # 모든 파일의 데이터를 순회
        for _, df in data.items():
            # 각 열의 고유 값을 초기화
            for column_name in df.columns:
                # 열의 데이터 타입을 검사하여 날짜 타입이면 변환
                if pd.api.types.is_datetime64_any_dtype(df[column_name]):
                    # 날짜 타입일 경우 to_datetime으로 변환 (오류 발생 시 원래 데이터 유지)
                    try:
                        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
                    except Exception as e:
                        print(f"[ERROR] 날짜 변환 중 오류 발생: {e}")

                # 고유값 리스트 생성
                unique_values = df[column_name].dropna().unique().tolist()
                self.unique_values.initialize_unique_values(column_name, unique_values)

    def update_unique_value_selection(self, column_name: str, value: Union[str, int, float, pd.Timestamp], is_selected: bool) -> None:
        """고유값의 선택 상태를 업데이트합니다."""
        self.unique_values.update_unique_value_selection(column_name, value, is_selected)
    
    def get_selected_unique_values(self, column_name: str) -> List[Union[str, int, float, pd.Timestamp]]:
        """선택된 고유값을 반환합니다."""
        return self.unique_values.get_selected_unique_values(column_name)

    def get_all_unique_values_properties(self, column_name: str) -> List[Union[str, int, float, pd.Timestamp]]:
        """모든 고유값을 반환합니다."""
        return self.unique_values.get_all_unique_values_properties(column_name)

    def delete_unique_value(self, column_name: str, value: Union[str, int, float, pd.Timestamp]) -> None:
        """특정 열의 고유값을 삭제합니다."""
        self.unique_values.delete_unique_value(column_name, value)

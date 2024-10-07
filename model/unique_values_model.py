from typing import Dict, List, Union
import pandas as pd

class UniqueValues:
    def __init__(self):
        # 고유값을 키로 사용하여 검색 속도 향상
        self.unique_values_data: Dict[str, Dict[Union[str, int, float, pd.Timestamp], Dict[str, Union[str, int, float, pd.Timestamp, bool]]]] = {}

    def initialize_unique_values(self, column_name: str, unique_values: List[Union[str, int, float, pd.Timestamp]]) -> None:
        """고유값 데이터를 초기화합니다."""
        if column_name not in self.unique_values_data:
            self.unique_values_data[column_name] = {value: {'value': value, 'is_selected': True} for value in unique_values}
        else:
            # 기존 데이터에 추가되지 않은 고유값만 추가
            existing_values = set(self.unique_values_data[column_name].keys())
            new_values = {value: {'value': value, 'is_selected': True} for value in unique_values if value not in existing_values}
            self.unique_values_data[column_name].update(new_values)

            # 타입별로 정렬
            self.unique_values_data[column_name] = dict(sorted(
                self.unique_values_data[column_name].items(),
                key=lambda x: (isinstance(x[1]['value'], str),
                               isinstance(x[1]['value'], (int, float)),
                               isinstance(x[1]['value'], pd.Timestamp),
                               x[1]['value'])
            ))

    def update_unique_value_selection(self, column_name: str, value: Union[str, int, float, pd.Timestamp], is_selected: bool) -> None:
        """고유값의 선택 상태를 업데이트합니다."""
        if column_name in self.unique_values_data and value in self.unique_values_data[column_name]:
            self.unique_values_data[column_name][value]['is_selected'] = is_selected

    def get_selected_unique_values(self, column_name: str) -> List[Union[str, int, float, pd.Timestamp]]:
        """선택된 고유값만 반환합니다."""
        if column_name in self.unique_values_data:
            return [item['value'] for item in self.unique_values_data[column_name].values() if item.get('is_selected', True)]
        return []

    def get_all_unique_values_properties(self, column_name: str) -> List[Dict[str, Union[str, int, float, pd.Timestamp, bool]]]:
        """모든 고유값의 속성을 반환합니다."""
        if column_name in self.unique_values_data:
            return list(self.unique_values_data[column_name].values())
        return []

    def delete_unique_value(self, column_name: str, value: Union[str, int, float, pd.Timestamp]) -> None:
        """특정 열의 고유값을 삭제합니다."""
        if column_name in self.unique_values_data and value in self.unique_values_data[column_name]:
            del self.unique_values_data[column_name][value]

    def get_all_data(self) -> Dict[str, List[Dict[str, Union[str, int, float, pd.Timestamp, bool]]]]:
        """모든 고유값 데이터를 반환합니다."""
        return {column_name: list(values.values()) for column_name, values in self.unique_values_data.items()}
    
    def update_all_selection_states(self, column_name: str, is_selected: bool) -> None:
        """특정 열의 모든 고유값의 선택 상태를 업데이트합니다."""
        if column_name in self.unique_values_data:
            for value in self.unique_values_data[column_name]:
                self.unique_values_data[column_name][value]['is_selected'] = is_selected

    def remove_all_data(self):
        self.unique_values_data.clear()
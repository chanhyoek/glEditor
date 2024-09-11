# column_data_manager.py
from typing import Dict, List, Union

class Columns:
    def __init__(self):
        self.column_data: Dict[str, Dict[str, Union[bool, List[Dict[str, Union[str, bool]]]]]] = {}

    def initialize_column_data(self, column_name: str, is_all_dup: bool, is_select: bool = False) -> None:
        """열 데이터를 초기화합니다."""
        if column_name not in self.column_data:
            self.column_data[column_name] = {
                'is_all_dup': is_all_dup,
                'is_select': is_select
            }

    def update_column_selection(self, column_name: str, is_select: bool) -> None:
        """열의 선택 상태를 업데이트합니다."""
        if column_name in self.column_data:
            self.column_data[column_name]['is_select'] = is_select

    def get_selected_columns(self) -> List[str]:
        """선택된 열을 반환합니다."""
        return [col_name for col_name, data in self.column_data.items() if data.get('is_select', False)]

    def get_all_columns_properties(self) -> List[Dict[str, Union[str, bool]]]:
        """모든 열의 속성을 반환합니다."""
        return [{'col_name': col_name, **data} for col_name, data in self.column_data.items()]

    def remove_all_data(self):
        self.column_data.clear()
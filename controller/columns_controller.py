# column_data_controller.py
from typing import List, Union, Dict
from model.columns_model import Columns

class ColumnsController:
    def __init__(self, columns: Columns):
        self.columns = columns

    def initialize_columns(self, metadata_controller) -> None:
        """MetadataController를 통해 모든 열 데이터를 초기화합니다."""
        self.columns.remove_all_data()
        
        all_keys = list(metadata_controller.model.metadata.keys())
        column_tracker = {}

        for key in all_keys:
            headers = metadata_controller.get_headers(key)
            for header in headers:
                col_name = header['col_name']
                if col_name not in column_tracker:
                    column_tracker[col_name] = {'count': 1, 'is_select': False}
                else:
                    column_tracker[col_name]['count'] += 1
         # 열 정보 초기화
        for col_name, data in column_tracker.items():
            is_all_dup = data['count'] == len(all_keys)  # 모든 파일에 공통이면 True
            self.columns.initialize_column_data(col_name, is_all_dup, is_all_dup)

    def update_column_selection(self, col_name: str, is_select: bool) -> None:
        """열의 선택 상태를 업데이트합니다."""
        self.columns.update_column_selection(col_name, is_select)

    def get_selected_columns(self) -> List[str]:
        """선택된 열을 반환합니다."""
        return self.columns.get_selected_columns()

    def get_all_columns_properties(self) -> List[Dict[str, Union[str, bool]]]:
        """모든 열의 속성을 반환합니다."""
        return self.columns.get_all_columns_properties()

    def search_columns(self, search_term: str) -> None:
        """검색어와 일치하는 열이나 고유 값을 선택 상태로 업데이트합니다."""
        for column in self.get_all_columns_properties():
            if search_term.lower() in column['col_name'].lower():
                self.update_column_selection(column['col_name'], True)
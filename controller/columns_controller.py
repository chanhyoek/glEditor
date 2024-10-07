# column_data_controller.py
from typing import List, Union, Dict
from model.columns_model import Columns

class ColumnsController:
    def __init__(self, columns: Columns):
        self.columns = columns
        self.observers = []

    def initialize_columns(self, metadata_controller) -> None:
        """MetadataController를 통해 모든 열 데이터를 초기화합니다."""
        
        # 모든 메타데이터 키 가져오기
        all_keys = list(metadata_controller.model.metadata.keys())
        column_tracker = {}

        for key in all_keys:
            headers = metadata_controller.get_headers(key)

            for col_name in headers:
                # 열 이름을 기준으로 초기화
                if col_name not in column_tracker:
                    column_tracker[col_name] = {'count': 1}
                else:
                    column_tracker[col_name]['count'] += 1

        # 열 정보 초기화
        for col_name, data in column_tracker.items():
            is_all_dup = data['count'] == len(all_keys)  # 모든 파일에 공통이면 True
            is_select = is_all_dup  # 모든 파일에 열이 중복되는 경우에만 True
            self.columns.initialize_column_data(col_name, is_all_dup, is_select)

    def add_observer(self, observer):
        """옵저버를 추가합니다."""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """옵저버를 제거합니다."""
        self.observers.remove(observer)

    def remove_all_observers(self):
        """옵저버를 모두 제거합니다."""
        self.observers.clear()

    def notify_observers(self):
        """모든 옵저버에게 상태 변경을 알립니다."""
        for observer in self.observers:
            observer.update_observer()

    def update_column_selection(self, col_name: str, is_select: bool) -> None:
        """단일 열의 선택 상태를 업데이트하고 옵저버에게 알림을 보냅니다."""
        self.columns.update_column_selection(col_name, is_select)
        self.notify_observers()  # 옵저버에게 알림

    def select_all_columns(self):
        """모든 열을 선택합니다."""
        self.columns.select_all_columns()
        self.notify_observers()

    def unselect_all_columns(self):
        """모든 열 선택을 해제합니다."""
        self.columns.unselect_all_columns()
        self.notify_observers()

    def get_all_columns_properties(self) -> List[Dict[str, Union[str, bool]]]:
        """모든 열의 속성 목록을 반환합니다."""
        return self.columns.get_all_columns_properties()
    
    def get_selected_columns(self):
        """선택된 열을 반환합니다."""
        return self.columns.get_selected_columns()

    def search_columns(self, search_term: str) -> None:
        """검색어와 일치하는 열이나 고유 값을 선택 상태로 업데이트합니다."""
        for column in self.get_all_columns_properties():
            if search_term.lower() in column['col_name'].lower():
                self.update_column_selection(column['col_name'], True)

    def reset_columns(self):
        """모든 열 데이터를 초기화합니다."""
        self.columns.remove_all_data()
        self.observers.clear()

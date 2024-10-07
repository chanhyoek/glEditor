from model.meta_data_model import MetadataModel
from typing import List, Dict, Union
import pandas as pd

class MetadataController:
    def __init__(self, model: MetadataModel):
        self.model:MetadataModel = model
        self.observers = []

    def generate_metadata(self, file_path: str, data: Dict[str, pd.DataFrame]) -> None:
        """Generate metadata for the file and store it in the model."""

        for key, df in data.items():
            headers = [col for col in df.columns]  
            is_select = True  # Set is_select as True by default
            first_5_rows = df.head(5)
            self.model.set_metadata(key, file_path, is_select, headers, first_5_rows)

    def get_first_5_rows(self, key: str) -> pd.DataFrame:
        """Return the first 5 rows of the specified sheet."""
        return self.model.get_metadata(key).get("first_5_rows", pd.DataFrame())

    def get_headers(self, key: str) -> List[str]:
        """Return headers for the specified sheet."""
        return self.model.get_metadata(key).get("headers", [])

    def get_file_path(self, key: str) -> str:
        """Return the file path for the specified key."""
        return self.model.get_metadata(key).get("file_path", "")

    def get_all_file_paths(self) -> List[str]:
        """Return all file paths."""
        file_paths = []
        for key in self.model.metadata:
            file_path = self.get_file_path(key)
            if file_path:
                file_paths.append(file_path)
        return file_paths

    def update_keys_selection(self, key: str, is_select: bool) -> None:
        """Update the is_select property for a specific key."""
        self.model.update_selected_key(key, is_select)
        self.notify_observers()
    
    def select_all_keys(self):
        """모든 열을 선택합니다."""
        self.model.select_all_keys()
        self.notify_observers()

    def unselect_all_keys(self):
        """모든 열 선택을 해제합니다."""
        self.model.unselect_all_keys()
        self.notify_observers()

    def get_all_keys_selected_properties(self) -> List[Dict[str, bool]]:
        """Return all keys and their is_select properties."""
        return self.model.get_all_keys_properties()

    def get_selected_key(self) -> List[str]:
        return self.model.get_selected_keys()

    def reset_metadata(self) -> None:
        """Reset metadata in the model."""
        self.model.reset_metadata()
        self.observers.clear()

    def add_observer(self, observer):
        """옵저버를 추가합니다."""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """옵저버를 제거합니다."""
        self.observers.remove(observer)

    def remove_all_observer(self):
        self.observers.clear()

    def notify_observers(self):
        """모든 옵저버에게 상태 변경을 알립니다."""
        for observer in self.observers:
            observer.update_observer()

    def search_columns(self, search_term: str) -> None:
        """검색어와 일치하는 열이나 고유 값을 선택 상태로 업데이트합니다."""
        for key in self.get_all_keys_selected_properties():
            if search_term.lower() in key['key'].lower():
                self.update_keys_selection(key['key'], True)


from typing import Dict, List, Union
import pandas as pd

class MetadataModel:
    def __init__(self):
        # Initialize metadata storage
        self.metadata: Dict[str, Dict[str, Union[
            str, 
            pd.DataFrame,
            bool, 
            List[str],  # headers: only includes column names
        ]]] = {}

    def set_metadata(
        self, 
        key: str, 
        file_path: str,
        is_select: bool, 
        headers: List[str], 
        first_5_rows: pd.DataFrame
    ) -> None:
        """Set metadata"""

        self.metadata[key] = {
            "file_path": file_path,
            "is_select": is_select,
            "first_5_rows": first_5_rows,
            "headers": headers,
        }

    def get_metadata(self, key: str) -> Dict[str, Union[
        str, 
        pd.DataFrame, 
        bool,
        List[str]
    ]]:
        """Return metadata for the specified key"""
        return self.metadata.get(key, {})

    def update_selected_key(self, key: str, is_select: bool) -> None:
        """Update the is_select attribute for the specified key"""
        if key in self.metadata:
            self.metadata[key]['is_select'] = is_select

    def select_all_keys(self):
        for key in self.metadata:
            self.metadata[key]['is_select'] = True

    def unselect_all_keys(self):
        for key in self.metadata:
            self.metadata[key]['is_select'] = False

    def get_all_keys_properties(self) -> List[Dict[str, bool]]:
        """Return all keys and their is_select properties"""
        all_keys_properties = []
        for key, meta in self.metadata.items():
            # 새로운 형식으로 데이터 구조 변경
            key_property = {'key': key, 'is_select': meta.get('is_select', False)}
            all_keys_properties.append(key_property)
        return all_keys_properties
    
    def get_selected_keys(self) -> List[str]:
        return [key for key, data in self.metadata.items() if data.get('is_select', False)]

    def reset_metadata(self) -> None:
        """Reset metadata"""
        self.metadata.clear()
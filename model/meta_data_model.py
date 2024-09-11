from typing import Dict, List, Union
import pandas as pd

class MetadataModel:
    def __init__(self):
        # 메타데이터 저장을 위한 초기화
        self.metadata: Dict[str, Dict[str, Union[
            str, 
            pd.DataFrame, 
            List[Dict[str, Union[str, bool]]],  # headers: 열 이름과 선택 상태(is_select)만 포함
            Dict[str, Dict[str, bool]]  # unique_values: 열 이름별 값과 선택 여부 포함
        ]]] = {}

    def set_metadata(
        self, 
        key: str, 
        file_path: str, 
        headers: List[Dict[str, Union[str, bool]]], 
        first_5_rows: pd.DataFrame, 
        unique_values: Dict[str, Dict[str, bool]]
    ) -> None:
        """메타데이터 설정"""
        self.metadata[key] = {
            "file_path": file_path,
            "first_5_rows": first_5_rows,
            "headers": headers,
            "unique_values": unique_values
        }

    def get_metadata(self, key: str) -> Dict[str, Union[
        str, 
        pd.DataFrame, 
        List[Dict[str, Union[str, bool]]], 
        Dict[str, Dict[str, bool]]
    ]]:
        """지정된 키에 대한 메타데이터 반환"""
        return self.metadata.get(key, {})

    def reset_metadata(self) -> None:
        """메타데이터 초기화"""
        self.metadata.clear()

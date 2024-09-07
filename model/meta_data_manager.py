from typing import Dict, List, Union
import pandas as pd

class MetadataManager:
    def __init__(self):
         self.metadata: Dict[str, Dict[str, Union[str, pd.DataFrame, List[str], Dict[str, List[Union[str, int, float]]]]]] = {}

    def generate_metadata(self, file_path: str, data: Dict[str, pd.DataFrame]) -> None:
        """파일의 메타데이터를 생성합니다 (헤더, 첫 5행, 열별 고유 값)."""
        for key, df in data.items():
            # 헤더와 처음 5행 저장
            self.metadata[key] = {
                "file_path": file_path,
                "first_5_rows": df.head(5),
                "headers": df.columns.tolist(),
                "unique_values": {col: df[col].dropna().unique().tolist() for col in df.columns}
            }

    def get_first_5_rows(self, key: str) -> pd.DataFrame:
        """지정된 시트의 첫 5행을 반환합니다."""
        return self.metadata.get(key, {}).get("first_5_rows", pd.DataFrame())

    def get_headers(self, key: str) -> List[str]:
        """지정된 시트의 헤더를 반환합니다."""
        return self.metadata.get(key, {}).get("headers", [])

    def get_unique_values(self, key: str, column_name: str) -> List[Union[str, int, float]]:
        """지정된 시트의 특정 열에 대한 고유 값을 반환합니다."""
        return self.metadata.get(key, {}).get("unique_values", {}).get(column_name, [])

    def get_path(self, key: str) -> str:
        """지정된 키에 대한 파일 경로를 반환합니다."""
        return self.metadata.get(key, {}).get("file_path", "")

    def get_all_keys(self) -> List[str]:
        """모든 키 값을 리스트로 반환합니다."""
        return list(self.metadata.keys())

    def reset_metadata(self) -> None:
        """메타데이터를 초기화합니다."""
        self.metadata.clear()
    
    def get_all_headers(self) -> List[str]:
        """모든 시트의 헤더를 중복 없이 리스트로 반환합니다."""
        all_headers = []  # 중복을 피하기 위해 set 사용
        for key in self.metadata.keys():
            headers = self.get_headers(key)
            all_headers.extend(headers)  

        return all_headers  # 리스트로 변환하여 반환
    
    def get_all_unique_values(self, column_name: str) -> List[Union[str, int, float]]:
        """특정 열(column_name)에 대해 모든 시트에서 중복 없이 고유 값을 반환합니다."""
        all_unique_values = set()  # 중복을 피하기 위해 set 사용
        for key in self.metadata.keys():
            unique_values = self.get_unique_values(key, column_name)
            all_unique_values.update(unique_values)  # set에 고유 값 추가

        return list(all_unique_values)  # 리스트로 변환하여 반환
    
    def get_all_file_path(self) -> List[str]:
        """모든 파일 경로를 리스트로 반환합니다."""
        all_file_path = []
        for key in self.metadata.keys():
            path = self.get_path(key)
            all_file_path.append(path)

        return all_file_path
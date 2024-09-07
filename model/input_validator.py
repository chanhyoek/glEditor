import flet as ft

class InputValidator:
    def __init__(self, options):
        self.options = options

    def validate_checkbox_selection(self):
        """적어도 하나의 열이 선택되었는지 확인"""
        if not any(checkbox.value for checkbox in self.options['checkboxes'] if isinstance(checkbox, ft.Text)):
            return "적어도 하나의 열을 선택해야 합니다."
        else:
            print(f"열을 선택: {list(checkbox.value for checkbox in self.options['checkboxes'] if isinstance(checkbox, ft.Text))}")
        return None

    def validate_unique_value_selection(self):
        """데이터 분리 옵션이 선택된 경우 추가 검사"""
        if self.options['sperate_df_values']:
            # 고유값 체크박스 검증
            if not any(checkbox.value for checkbox in self.options['unique_value_checkboxes'] if isinstance(checkbox, ft.Text)):
                return "데이터를 분리할 고유값을 선택해야 합니다."
            else:
                print(self.options['unique_value_checkboxes'])
            # 저장 옵션 검증
            
            if not self.options['save_option']:
                return "저장 옵션을 선택해야 합니다."
            else:
                print(self.options['save_option'])
        
        return None

    def validate_sort_options(self):
        """정렬 옵션 유효성 검사"""
        if 'sort_options' in self.options:
            for column, ascending in self.options['sort_options']:
                if not column:
                    return "모든 정렬 옵션에 대해 열을 선택해야 합니다."
                if ascending is None:
                    return "모든 정렬 옵션에 대해 정렬 방식을 선택해야 합니다."
        return None

    def validate(self):
        """모든 유효성 검사 실행"""
        # 체크박스 선택 유효성 검사
        error_message = self.validate_checkbox_selection()
        if error_message:
            return error_message

        # 고유값 선택 유효성 검사
        error_message = self.validate_unique_value_selection()
        if error_message:
            return error_message

        # 정렬 옵션 유효성 검사
        error_message = self.validate_sort_options()
        if error_message:
            return error_message

        return None  # 모든 검사가 통과된 경우

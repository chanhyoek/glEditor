import flet as ft

class InputValidator:
    def __init__(self, options, unique_values_controller, columns_controller):
        self.options = options
        self.unique_values_controller = unique_values_controller
        self.columns_controller = columns_controller

    def validate_checkbox_selection(self):
        """Validate that at least one column is selected."""
        selected_columns = self.columns_controller.get_selected_columns()
        if not selected_columns:
            return "적어도 하나의 열을 선택해야 합니다."
        else:
            print(f"Selected columns: {selected_columns}")
        return None

    def validate_unique_value_selection(self):
        """Perform additional checks if the data separation option is selected."""
        if self.options.get('sperate_df_values'):
            # Validate unique value selection
            column_name = self.unique_values_controller.get_column_name()
            if not column_name:
                return "데이터를 분리할 고유값을 선택해야 합니다."
            else:
                print(f"Selected unique column: {column_name}")
                print(f"Unique value checkboxes: {self.options.get('unique_value_checkboxes')}")

            # Validate save option
            save_option = self.options.get('save_option')
            if not save_option:
                return "저장 옵션을 선택해야 합니다."
            else:
                print(f"Save option: {save_option}")
        
        return None

    def validate_sort_options(self):
        """Validate sort options."""
        sort_options = self.options.get('sort_options')
        for column, ascending in sort_options:
            print(column, ascending)
            if not column:
                return "모든 정렬 옵션에 대해 열을 선택해야 합니다."
            if not ascending:
                return "모든 정렬 옵션에 대해 정렬 방식을 선택해야 합니다."
        return None

    def validate(self):
        """Run all validation checks."""
        # Validate checkbox selection
        error_message = self.validate_checkbox_selection()
        if error_message:
            return error_message

        # Validate unique value selection
        error_message = self.validate_unique_value_selection()
        if error_message:
            return error_message

        # Validate sort options
        error_message = self.validate_sort_options()
        if error_message:
            return error_message

        return None  # All validations passed

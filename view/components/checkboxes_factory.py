# checkbox_manager_factory.py

from .checkbox.columns_checkbox_manager import ColumnsCheckboxManager
from .checkbox.unique_value_checkbox_manager import UniqueValuesCheckboxManager

def create_checkbox_manager(mode, *args, **kwargs):
    """CheckboxManager의 팩토리를 생성하는 메서드."""
    if mode == 'columns':
        return ColumnsCheckboxManager(*args, **kwargs)
    elif mode == 'unique_values':
        return UniqueValuesCheckboxManager(*args, **kwargs)
    else:
        raise ValueError("Invalid mode specified for CheckboxManager creation.")
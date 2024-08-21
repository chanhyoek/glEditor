import flet as ft
from collections import Counter

import flet as ft
from collections import Counter

class CheckboxManager:
    def __init__(self, page, container):
        self.page = page
        self.container = container  # 외부에서 주입받은 컨테이너
        self.checkboxes = []  # 체크박스 리스트 초기화

    def create_checkboxes(self, labels, select_all=False, color="white", selected_color="blue"):
        self.container.controls.clear()  # 컨테이너의 기존 컨트롤들을 제거
        self.checkboxes = []  # 체크박스 리스트 초기화

        for label, selected in labels:
            checkbox = ft.Checkbox(
                label=label,
                value=select_all or selected,
                fill_color=selected_color if selected else color,
            )
            self.container.controls.append(checkbox)  # 컨테이너에 체크박스를 추가
            self.checkboxes.append(checkbox)  # 체크박스 리스트에 추가

        return self.container

    def create_checkboxes_for_columns(self, file_data):
        all_columns = []
        for data in file_data.values():
            all_columns.extend(data.columns)

        column_counts = Counter(all_columns)
        max_count = max(column_counts.values())

        labels = [(col, col_count == max_count) for col, col_count in column_counts.items()]
        return self.create_checkboxes(labels)

    def create_checkboxes_for_unique_values(self, df, column):
        unique_values = sorted(df[column].unique())
        labels = [(value, False) for value in unique_values]
        return self.create_checkboxes(labels)

    def update_checkboxes_with_unique_values(self, unique_values, batch_size=12):
        """Updates the container with checkboxes for each unique value, batching them in groups."""
        self.container.controls.clear()
        self.checkboxes.clear()
        
        temp_column_controls = []
        
        for i, value in enumerate(unique_values):
            checkbox = ft.Checkbox(label=value, value=True)
            temp_column_controls.append(checkbox)
            
            if (i + 1) % batch_size == 0:
                column = ft.Row(controls=temp_column_controls, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                self.container.controls.append(column)
                temp_column_controls = []
        
        if temp_column_controls:
            column = ft.Row(controls=temp_column_controls, scroll=ft.ScrollMode.AUTO,alignment=ft.MainAxisAlignment.START)
            self.container.controls.append(column)

        # 업데이트된 체크박스들을 체크박스 리스트에 저장
        self.checkboxes = [ctrl for ctrl in self.container.controls if isinstance(ctrl, ft.Checkbox)]
        self.container.visible = True
        return self.container

    def select_all_checkboxes(self):
        """Selects all checkboxes."""
        self._set_all_checkboxes_value(True)
    
    def unselect_all_checkboxes(self):
        """Unselects all checkboxes."""
        self._set_all_checkboxes_value(False)
    
    def _set_all_checkboxes_value(self, value):
        """Sets the value for all checkboxes."""
        for control in self.container.controls:
            if isinstance(control, ft.Checkbox):
                control.value = value
            elif isinstance(control, (ft.Row, ft.Column)):
                self._set_all_checkboxes_value_for_container(control, value)
        self.page.update()  # UI 업데이트

    def _set_all_checkboxes_value_for_container(self, container, value):
        """Recursively sets the value for checkboxes inside a container."""
        for control in container.controls:
            if isinstance(control, ft.Checkbox):
                control.value = value
            elif isinstance(control, (ft.Row, ft.Column)):
                self._set_all_checkboxes_value_for_container(control, value)

    def search_unique_value(self, search_term: str):
        """Searches and selects checkboxes matching the search term."""
        self._search_and_select_checkboxes(self.container, search_term.lower())
        self.page.update()

    def _search_and_select_checkboxes(self, container, search_term: str):
        """Recursively searches for checkboxes matching the search term and selects them."""
        for control in container.controls:
            if isinstance(control, ft.Checkbox):
                if search_term in control.label.lower():
                    control.value = True
            elif isinstance(control, (ft.Row, ft.Column)):
                self._search_and_select_checkboxes(control, search_term)

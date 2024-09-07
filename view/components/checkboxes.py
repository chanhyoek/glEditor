import flet as ft
from collections import Counter

class CheckboxManager:
    def __init__(self, page, container, error_handler):
        self.page = page
        self.container = container
        self.checkboxes = []
        self.error_handler = error_handler

    def create_checkboxes(self, labels, select_all=False, color="white", selected_color="blue"):
        """주어진 레이블로 체크박스 생성 후 컨테이너에 추가합니다."""
        self.container.controls.clear()
        self.checkboxes.clear()

        for label, selected in labels:
            checkbox = ft.Checkbox(
                label=label,
                value=select_all or selected,
                fill_color=selected_color if selected else color,
            )
            self.container.controls.append(checkbox)
            self.checkboxes.append(checkbox)

        return self.container

    def create_checkboxes_for_columns(self, meta_data):
        """메타데이터에서 모든 열 이름을 가져와 가장 빈도가 높은 열을 기본 선택으로 체크박스를 생성합니다."""
        all_columns = meta_data.get_all_headers()
        column_counts = Counter(all_columns)
        max_count = max(column_counts.values())
        labels = [(col, count == max_count) for col, count in column_counts.items()]
        return self.create_checkboxes(labels)

    def create_checkboxes_for_unique_values(self, df, column):
        """데이터프레임의 특정 열에서 고유한 값들에 대해 체크박스를 생성합니다."""
        unique_values = sorted(df[column].unique())
        labels = [(value, False) for value in unique_values]
        return self.create_checkboxes(labels)

    def update_checkboxes_with_unique_values(self, unique_values, batch_size=12):
        """고유 값들에 대한 체크박스를 업데이트하고, 배치 단위로 표시합니다."""
        if len(unique_values) > 240:
            self.error_handler.show_error("해당 열의 고유값이 너무 큽니다. 다른 열을 선택해 주세요")
            return

        self._create_batches(unique_values, batch_size)
        self.container.visible = True
        return self.container

    def _create_batches(self, values, batch_size):
        """값들을 배치 단위로 나누어 컨테이너에 추가합니다."""
        self.container.controls.clear()
        self.checkboxes.clear()
        temp_column_controls = []

        for i, value in enumerate(values):
            checkbox = ft.Checkbox(label=value, value=True)
            temp_column_controls.append(checkbox)

            if (i + 1) % batch_size == 0:
                self._add_row_to_container(temp_column_controls)
                temp_column_controls = []

        if temp_column_controls:
            self._add_row_to_container(temp_column_controls)

    def _add_row_to_container(self, controls):
        """체크박스들을 포함한 행을 컨테이너에 추가합니다."""
        row = ft.Row(controls=controls, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.container.controls.append(row)

    def group_values_by_alphabet(self, unique_values):
        """알파벳 순서대로 고유 값을 그룹화합니다."""
        grouped = {}
        for value in unique_values:
            first_letter = value[0].upper()
            grouped.setdefault(first_letter, []).append(value)
        return dict(sorted(grouped.items()))

    def create_checkbox_rows(self, values, batch_size):
        """체크박스를 생성하고 주어진 값들을 배치합니다."""
        rows = []
        temp_row_controls = []

        for i, value in enumerate(values):
            checkbox = ft.Checkbox(label=value, value=True)
            temp_row_controls.append(checkbox)

            if (i + 1) % batch_size == 0:
                rows.append(self._create_row(temp_row_controls))
                temp_row_controls = []

        if temp_row_controls:
            rows.append(self._create_row(temp_row_controls))

        return ft.Column(controls=rows, scroll=ft.ScrollMode.AUTO)

    def _create_row(self, controls):
        """체크박스를 포함한 행을 생성합니다."""
        return ft.Row(controls=controls, alignment=ft.MainAxisAlignment.START)

    def select_all_checkboxes(self, callback=None):
        """모든 체크박스를 선택합니다."""
        self._set_all_checkboxes_value(True)
        if callback:
            callback(None)

    def unselect_all_checkboxes(self, callback=None):
        """모든 체크박스를 선택 해제합니다."""
        self._set_all_checkboxes_value(False)
        if callback:
            callback(None)

    def _set_all_checkboxes_value(self, value):
        """모든 체크박스의 값을 설정합니다."""
        self._set_all_checkboxes_value_for_container(self.container, value)
        self.page.update()

    def _set_all_checkboxes_value_for_container(self, container, value):
        """컨테이너 내의 모든 체크박스 값을 재귀적으로 설정합니다."""
        for control in container.controls:
            if isinstance(control, ft.Checkbox):
                control.value = value
            elif isinstance(control, (ft.Row, ft.Column)):
                self._set_all_checkboxes_value_for_container(control, value)

    def search_unique_value(self, search_term):
        """검색어와 일치하는 체크박스를 검색하고 선택합니다."""
        self._search_and_select_checkboxes(self.container, search_term.lower())
        self.page.update()

    def _search_and_select_checkboxes(self, container, search_term):
        """검색어와 일치하는 체크박스를 재귀적으로 검색하고 선택합니다."""
        for control in container.controls:
            if isinstance(control, ft.Checkbox) and search_term in control.label.lower():
                control.value = True
            elif isinstance(control, (ft.Row, ft.Column)):
                self._search_and_select_checkboxes(control, search_term)

    def get_selected_checkbox_labels(self):
        """선택된 체크박스의 라벨을 리스트로 반환합니다."""
        return self._get_selected_checkbox_labels_recursive(self.container)

    def _get_selected_checkbox_labels_recursive(self, container):
        """선택된 체크박스를 재귀적으로 찾아 그들의 라벨을 반환하는 헬퍼 메서드입니다."""
        selected_labels = []
        for control in container.controls:
            if isinstance(control, ft.Checkbox) and control.value:
                selected_labels.append(control.label)
            elif isinstance(control, (ft.Row, ft.Column)):
                selected_labels.extend(self._get_selected_checkbox_labels_recursive(control))
        return selected_labels

    def get_selected_checkbox_labels_as_text(self):
        """주어진 라벨 리스트로부터 ft.Text 객체들을 생성하여 반환합니다."""
        labels = self.get_selected_checkbox_labels()
        return [ft.Text(label, size=16, color=ft.colors.LIGHT_BLUE_400) for label in labels]
    
    def register_checkbox_event_handlers(self, handler):
        """모든 체크박스에 대해 이벤트 핸들러를 등록합니다."""
        for checkbox in self.checkboxes:
            checkbox.on_change = handler

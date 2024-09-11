import flet as ft

class Paginator:
    def __init__(self, total_items, items_per_page, on_page_change_callback):
        """페이지네이션을 위한 클래스 초기화."""
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.on_page_change_callback = on_page_change_callback
        self.current_page = 0
        self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page

    def get_current_page_items(self, items):
        """현재 페이지에 해당하는 항목들을 반환합니다."""
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page

        end_index = min(end_index, len(items))

        return items[start_index:end_index]

    def next_page(self):
        """다음 페이지로 이동합니다."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.on_page_change_callback()

    def previous_page(self):
        """이전 페이지로 이동합니다."""
        if self.current_page > 0:
            self.current_page -= 1
            self.on_page_change_callback()

    def go_to_page(self, page_number):
        """지정한 페이지로 이동합니다."""
        if 0 <= page_number < self.total_pages:
            self.current_page = page_number
            self.on_page_change_callback()

    def add_pagination_controls(self, container):
        """페이지네이션 컨트롤(버튼)을 컨테이너에 추가합니다."""
        pagination_controls = []

        pagination_controls.append(self._create_previous_button())

        pagination_controls.extend(self._create_page_buttons())

        pagination_controls.append(self._create_next_button())

        # 페이지네이션 UI를 업데이트할 때마다 초기화된 컨트롤 추가
        container.controls.clear()
        container.controls.extend(pagination_controls)

    def _create_previous_button(self):
        """이전 페이지 버튼 생성."""
        return ft.CupertinoButton(
            text="이전",
            on_click=lambda _: self.previous_page(),
            disabled=self.current_page == 0
        )

    def _create_page_buttons(self):
        """페이지 번호 버튼들을 생성."""
        page_buttons = []
        for i in range(self.total_pages):
            page_buttons.append(ft.CupertinoButton(
                text=str(i + 1),  # 페이지 번호는 1부터 시작
                on_click=lambda _, page=i: self.go_to_page(page),
                color=ft.colors.LIGHT_BLUE_100 if i == self.current_page else ft.colors.WHITE
            ))
        return page_buttons

    def _create_next_button(self):
        """다음 페이지 버튼 생성."""
        return ft.CupertinoButton(
            text="다음",
            on_click=lambda _: self.next_page(),
            disabled=self.current_page >= self.total_pages - 1
        )

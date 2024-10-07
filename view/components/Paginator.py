import flet as ft

class Paginator:
    def __init__(self, items, items_per_page, on_page_change_callback):
        """페이지네이션 클래스 초기화."""
        self.items = items
        self.total_items = len(items)
        self.items_per_page = items_per_page
        self.on_page_change_callback = on_page_change_callback
        self.current_page = 0
        self.pages_per_group = 10  # 한 번에 표시할 페이지 버튼 수
        self.current_page_group = 0
        self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page

    def set_items(self, items):
        """아이템 설정."""
        self.items = items
        self.total_items = len(items)
        self.total_pages = (self.total_items + self.items_per_page - 1) // self.items_per_page
        self.current_page = 0
        self.current_page_group = 0

    def get_current_page_items(self):
        """현재 페이지의 아이템들을 반환합니다."""
        start_index = self.current_page * self.items_per_page
        end_index = min(start_index + self.items_per_page, len(self.items))
        return self.items[start_index:end_index]

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

        # "이전" 버튼 추가
        if self.current_page_group > 0:
            pagination_controls.append(self._create_previous_button())

        # 페이지 번호 버튼 추가
        pagination_controls.extend(self._create_page_buttons())

        # "다음" 버튼 추가
        if (self.current_page_group + 1) * self.pages_per_group < self.total_pages:
            pagination_controls.append(self._create_next_button())

        # 페이지네이션 UI를 업데이트할 때마다 초기화된 컨트롤 추가
        container.controls.clear()
        container.controls.extend(pagination_controls)

    def _create_previous_button(self):
        """이전 페이지 버튼 생성."""
        return ft.CupertinoButton(
            text="이전",
            on_click=lambda _: self._previous_group(),
            disabled=self.current_page_group == 0
        )

    def _create_page_buttons(self):
        """페이지 번호 버튼들을 생성."""
        page_buttons = []
        start_page = self.current_page_group * self.pages_per_group
        end_page = min(start_page + self.pages_per_group, self.total_pages)

        for i in range(start_page, end_page):
            page_buttons.append(ft.CupertinoButton(
                text=str(i + 1),  # 페이지 번호는 1부터 시작
                on_click=lambda _, page=i: self.go_to_page(page),
                color=ft.colors.BLUE if i == self.current_page else ft.colors.LIGHT_BLUE
            ))
        return page_buttons

    def _create_next_button(self):
        """다음 페이지 버튼 생성."""
        return ft.CupertinoButton(
            text="다음",
            on_click=lambda _: self._next_group(),
            disabled=(self.current_page_group + 1) * self.pages_per_group >= self.total_pages
        )

    def _next_group(self):
        """다음 페이지 그룹으로 이동합니다."""
        if (self.current_page_group + 1) * self.pages_per_group < self.total_pages:
            self.current_page_group += 1
            self.add_pagination_controls()

    def _previous_group(self):
        """이전 페이지 그룹으로 이동합니다."""
        if self.current_page_group > 0:
            self.current_page_group -= 1
            self.add_pagination_controls()

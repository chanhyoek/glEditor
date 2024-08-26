import flet as ft

class SearchField:
    def __init__(self, on_search, on_select_all=None, on_unselect_all=None, width=600):
        self.on_search = on_search
        self.on_select_all = on_select_all
        self.on_unselect_all = on_unselect_all
        self.search_field = ft.TextField(hint_text="Search...", width=width, on_submit=self._handle_search)

    def build(self):
        controls = [
            self.search_field,
            ft.CupertinoButton(content=ft.Text("Search"), on_click=self._handle_search)
        ]
        
        if self.on_select_all:
            controls.append(ft.CupertinoButton(content=ft.Text("전체선택"), on_click=self.on_select_all))
        if self.on_unselect_all:
            controls.append(ft.CupertinoButton(content=ft.Text("전체해제"), on_click=self.on_unselect_all))
        
        return ft.Row(controls=controls)

    def _handle_search(self, e):
        search_term = self.search_field.value
        self.on_search(search_term)

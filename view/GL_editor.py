import flet as ft
from .app_layout import AppLayout

class GLEditor:
    def __init__(self, page: ft.Page, task_manager):
        self.page = page
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.on_route_change = self.route_change
        self.task_manager = task_manager
        
    def build(self):
        self.layout = AppLayout(
            self,
            self.page,
            self.task_manager
        )
        return self.layout

    def initialize(self):
        self.page.views.append(
            ft.View(
                "/",
                [self.layout],
                padding=ft.padding.all(0)
            )
        )
        self.page.update()
        self.page.go("/")
    
    def route_change(self, e):
        troute = ft.TemplateRoute(self.page.route)
        if troute.match("/"):
            self.layout.set_homepage_view()
        elif troute.match("/merge"):
            self.layout.set_editpage_view()
        # elif troute.match("/extract"):
        #     self.layout.set_extractpage_view()
        self.page.update()

        
    

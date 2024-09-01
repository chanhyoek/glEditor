import flet as ft
from .components.NavBar import NavBar
from .pages.homepage import HomePage
from .pages.edit_data_page import EditDataPage

class AppLayout(ft.Row):
    def __init__(self, app, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.toggle_nav_rail_button = ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_LEFT, 
            icon_color=ft.colors.BLUE_GREY_400, 
            selected=False,
            selected_icon=ft.icons.ARROW_CIRCLE_RIGHT, 
            on_click=self.toggle_nav_rail
        )
        self.sidebar = NavBar(self, page)
        self.homepage = HomePage(page, self).build()
        self.editpage = EditDataPage(page, self).build()

        self._active_view = None
        self.controls = [self.sidebar, self.toggle_nav_rail_button]
        self.expand = True

    @property
    def active_view(self):
        return self._active_view
 
    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        if len(self.controls) > 2:
            self.controls.pop()
        self.controls.append(self._active_view)
        self.update()

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.update()
    
    def set_homepage_view(self):
        self.active_view = self.homepage
        self.sidebar.nav_rail.selected_index = 0
        self.sidebar.update()
        self.page.update()
    
    def set_editpage_view(self):
        self.active_view = self.editpage
        self.sidebar.nav_rail.selected_index = 1
        self.sidebar.update()
        self.page.update()
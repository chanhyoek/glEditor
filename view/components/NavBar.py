import flet as ft

class NavBar(ft.UserControl):
    def __init__(self, app_layout, page):
        super().__init__()
        self.app_layout = app_layout
        self.page = page
        self.top_nav_items = [
            ft.NavigationRailDestination(
                label_content=ft.Text("HOME", color=ft.colors.LIGHT_BLUE_100),
                label="HOME",
                icon=ft.icons.ADD_HOME_OUTLINED,
                selected_icon=ft.icons.ADD_HOME_OUTLINED
            ),
            ft.NavigationRailDestination(
                label_content=ft.Text("편집하기", color=ft.colors.LIGHT_BLUE_100),
                label="merge",
                icon=ft.icons.CALL_MERGE_ROUNDED,
                selected_icon=ft.icons.CALL_MERGE_ROUNDED
            ),
            # ft.NavigationRailDestination(
            #     label_content=ft.Text("추출하기"),
            #     label="extract",
            #     icon=ft.icons.CALL_SPLIT_ROUNDED,
            #     selected_icon=ft.icons.CALL_SPLIT_ROUNDED
            # ),
        ]
        self.nav_rail = ft.NavigationRail(
            selected_index=None,
            label_type=ft.NavigationRailLabelType.ALL,
            on_change=self.nav_change,
            destinations=self.top_nav_items,
            min_width=220,
            expand=True,
            extended=True
        )
        
    def build(self):
        self.view = ft.Container(
            content=ft.Column([
                ft.Row(
                    [
                        ft.Text("XCELATOR", size=30, weight="bold"),
                        ft.Icon(name=ft.icons.SPEED_SHARP, color = "White", size = 32),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment= ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                    ft.Text("Xcelator로 업무를 쉽고 빠르게")
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment= ft.MainAxisAlignment.CENTER),
                ft.Container(
                    bgcolor=ft.colors.WHITE54,
                    border_radius=ft.border_radius.all(30),
                    alignment=ft.alignment.center_right,
                    width=220,
                    height=1
                ),
                ft.Row([self.nav_rail], height=300, expand=1),  # 여기서 expand를 1로 설정
                ft.Row(
                    controls=[ft.Text("Developed by Tax Core DA | Ver 1.0.0", size=9)],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    expand=0  # 이 행의 비율을 작게 설정
                )
            ],
            spacing=20),
            padding=ft.padding.all(15),
            margin=ft.margin.all(10),
            width=250,
            expand=True,
        )
        return self.view
    
    def nav_change(self, e):
        index = e.control.selected_index
        self.nav_rail.selected_index = index
        if index == 0:
            self.page.route = "/"
            self.app_layout.set_homepage_view()
        elif index == 1:
            self.page.route = "/merge"
            self.app_layout.set_mergepage_view()
        # elif index == 2:
        #     self.page.route = "/extract"
        #     self.app_layout.set_extractpage_view()
        self.page.update()

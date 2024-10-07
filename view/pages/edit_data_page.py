import flet as ft
from .editpage.setup_view import SetupView
from .editpage.edit_view import EditView
from .editpage.tabs import Tabs
from .editpage.options.sperate_df import SperateDFOption
from model.data_manipulator import DataManipulator
from model.error_handler import ErrorHandler

class EditDataPage:
    def __init__(self, page:ft.Page, app_layout, task_manager, edit_view_class=None, tabs_class=None, speratedf_class=None):
        self.page = page
        self.app_layout = app_layout
        self.task_manager = task_manager

        self.current_width = self.page.window_width - 220

        self.setup_view = SetupView(page, task_manager, self.on_file_uploaded, self.current_width)
        self.edit_view_class = edit_view_class or EditView
        self.tabs_class = tabs_class or Tabs
        self.speratedf_class = speratedf_class or SperateDFOption
        self.edit_view = None
        self.data_manipulator = DataManipulator() 
        self.view = ft.Column(controls=[], width=self.current_width)

        self.page.on_resize = self.on_resize

    def build(self):
        self.view.controls.append(self.setup_view.build())
        return self.view

    def get_adjusted_width(self):
        # 요구 사항에 따라 새로운 너비 계산
        return self.page.window_width - 220 if self.page.window_width > 220 else self.page.window_width

    def update_width(self):
        # 페이지와 모든 하위 컴포넌트의 너비 업데이트
        print("페이지 너비 조정")
        new_width = self.get_adjusted_width()
        self.view.width = new_width
        # self.setup_view.set_width(new_width)

        # edit_view가 존재하면 너비 업데이트
        if self.edit_view:
            self.edit_view.set_width(new_width)

        self.page.update()

    def on_file_uploaded(self, metadata_controller, columns_controller, unique_values_controller):
        # 기존 view의 내용을 초기화 (setup_view는 그대로 유지)
        if self.edit_view:
            self.edit_view = None
            self.view.controls = self.view.controls[:-1]  # setup_view만 남기고 edit_view를 제거
        
        # 새로운 EditView 생성, DataManipulator 인스턴스를 전달
        self.edit_view = self.edit_view_class(
            self.page, 
            metadata_controller,  
            columns_controller,
            unique_values_controller,
            self.data_manipulator, 
            self.task_manager,
            tabs_class=self.tabs_class,
            initial_width=self.current_width
        )
        self.view.controls.append(self.edit_view.build())  # 새로운 edit_view 추가

        self.page.update()  # 페이지 업데이트
        return self.view
    
    def on_resize(self, e):
        # 모든 하위 컴포넌트의 너비를 조정하는 리사이즈 로직
        self.update_width()

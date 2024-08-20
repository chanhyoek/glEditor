import flet as ft
from .editpage.setup_view import SetupView
from .editpage.edit_view import EditView
from .editpage.tabs import Tabs
from .editpage.options.sperate_df import SperateDFOption
from model.data_manipulator import DataManipulator

class EditDataPage:
    def __init__(self, page, app_layout, edit_view_class=None, tabs_class=None, speratedf_class=None):
        self.page = page
        self.app_layout = app_layout
        self.setup_view = SetupView(page, self.on_file_uploaded)
        self.edit_view_class = edit_view_class or EditView
        self.tabs_class = tabs_class or Tabs
        self.speratedf_class = speratedf_class or SperateDFOption
        self.edit_view = None
        self.data_manipulator = DataManipulator() 
        self.view = ft.Column(controls=[])

    def build(self):
        self.view.controls.append(self.setup_view.build())
        return self.view

    def on_file_uploaded(self, file_data):
        # 기존 view의 내용을 초기화 (setup_view는 그대로 유지)
        if self.edit_view:
            self.view.controls = self.view.controls[:-1]  # setup_view만 남기고 edit_view를 제거
        
        # 새로운 EditView 생성, DataManipulator 인스턴스를 전달
        self.edit_view = self.edit_view_class(self.page, file_data, self.data_manipulator, tabs_class=self.tabs_class, speratedf_class=self.speratedf_class)
        self.view.controls.append(self.edit_view.build())  # 새로운 edit_view 추가

        self.page.update()  # 페이지 업데이트
        return self.view

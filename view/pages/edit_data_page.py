import flet as ft
from .editpage.setup_view import SetupView
from .editpage.edit_view import EditView
from .editpage.tabs import Tabs
from .editpage.options.sperate_df import SperateDFOption
from model.data_manipulator import DataManipulator
from model.error_handler import ErrorHandler

class EditDataPage:
    def __init__(self, page, app_layout, task_manager, edit_view_class=None, tabs_class=None, speratedf_class=None):
        self.page = page
        self.app_layout = app_layout
        self.task_manager = task_manager
        self.setup_view = SetupView(page, task_manager, self.on_file_uploaded)
        self.edit_view_class = edit_view_class or EditView
        self.tabs_class = tabs_class or Tabs
        self.speratedf_class = speratedf_class or SperateDFOption
        self.edit_view = None
        self.data_manipulator = DataManipulator() 
        self.view = ft.Column(controls=[])

    def build(self):
        self.view.controls.append(self.setup_view.build())
        return self.view

    def on_file_uploaded(self, metadata_controller, columns_controller, unique_values_controller):
        # 기존 view의 내용을 초기화 (setup_view는 그대로 유지)
        print("on_file_uploaded 호출됨")  # 디버그 출력
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
            tabs_class=self.tabs_class
        )
        print("EditView 생성됨")  # 디버그 출력
        self.view.controls.append(self.edit_view.build())  # 새로운 edit_view 추가

        self.page.update()  # 페이지 업데이트
        print("페이지 업데이트 호출됨")  # 디버그 출력
        return self.view

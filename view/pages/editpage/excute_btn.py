# view/excute_btn.py

import asyncio
import flet as ft
from ...components.AlertModal import AlertModal
from services.task_manager import TaskManager

class ExcuteBtn:
    def __init__(self, options, snackbar_notifier ,controller, page, task_manager):
        self.page = page 
        self.options = options
        self.controller = controller
        self.snackbar_notifier = snackbar_notifier
        self.task_manager = task_manager 
    
    def build(self):
        """버튼 UI를 빌드합니다."""
        self.excute_btn = ft.Container(
            content=ft.ElevatedButton(
                "파일생성하기",
                icon=ft.icons.MERGE_TYPE,
                adaptive=True,
                on_click=self.on_create_files_button_click,  # 비동기 함수 호출
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.GREEN,
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            padding=20
        )
        return self.excute_btn

    def on_create_files_button_click(self, e):
        """파일 생성 버튼 클릭 시 호출됩니다."""
        # AlertModal 생성
        self.alert_modal = AlertModal(
            self.page,
            content_text="파일 생성 중입니다. 잠시만 기다려주세요...",
            task_manager=self.task_manager,
            snackbar_notifier=self.snackbar_notifier
        )
        
        self.alert_modal.show()  # AlertModal 표시

        # 파일 생성 작업을 컨트롤러에 요청
        asyncio.run(self.task_manager.run_task(
            self.controller.create_files(),  
            on_complete=self.alert_modal.close,  # 작업 완료 시 모달 닫기
            on_error=lambda msg: self.snackbar_notifier.show_snackbar(f"오류가 발생했습니다: {msg}", error=True)  # 오류 발생 시 알림
        ))

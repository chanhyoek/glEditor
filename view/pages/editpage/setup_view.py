import flet as ft
from model.excel_data_parser import ExcelDataParser

class SetupView:
    def __init__(self, page: ft.Page, on_file_uploaded_callback):
        self.page = page
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)
        self.page.overlay.append(self.file_picker)
        self.on_file_uploaded_callback = on_file_uploaded_callback
        
        # 모달 다이얼로그 생성
        self.modal_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column(
                controls=[
                    ft.ProgressRing(),  # 에니메이션으로 로딩 표시
                    ft.Text("파일 첨부 중입니다. 잠시만 기다려주세요...", size=15),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                height=120,
                width=300
            ),
            actions=[],
        )
    
    def build(self):
        header = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("데이터 가공하기", size=32, weight="bold", color=ft.colors.BLUE),
                    ft.Text("여러 파일의 데이터를 취합 후 원하는 방식대로 편집합니다.", size=16)
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.only(left=20, top=20)
        )
        
        file_upload_button = ft.Container(
            content=ft.ElevatedButton(
                "파일 업로드",
                icon=ft.icons.UPLOAD_FILE,
                on_click=lambda _: self.file_picker.pick_files(allow_multiple=True),
                adaptive=True,
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=ft.colors.BLUE,
                    shape=ft.RoundedRectangleBorder(radius=10),
                )
            ),
            padding=ft.padding.only(left=20)
        )
        
        self.view = ft.Container(
            ft.Row(
                controls=[
                    header,
                    file_upload_button
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.START,
            ),
            height=250,
            width=800,
            expand=0
        )    
        return self.view
    
    async def file_picker_result(self, e):
        # 파일 업로드 모달을 띄우기
        self.page.dialog = self.modal_dialog
        self.modal_dialog.open = True
        self.page.update()
        
        # 파일 데이터를 읽어옴
        try:
            file_paths = [f.path for f in e.files]
            file_data = await ExcelDataParser().get_multiple_data(file_paths)
            self.on_file_uploaded_callback(file_data)
        finally:
            # 파일 업로드 완료 후 모달 닫기
            self.modal_dialog.open = False
            self.page.update()

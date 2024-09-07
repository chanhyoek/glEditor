import asyncio
from functools import wraps

class TaskManager:
    """작업을 관리하는 클래스."""
    def __init__(self):
        self._current_task = None

    def register_task(self, task):
        """현재 실행 중인 작업을 등록합니다."""
        self._current_task = task
        print(f"Task '{task.get_name()}' 등록")

    def unregister_task(self):
        """현재 실행 중인 작업을 등록 해제합니다."""
        if self._current_task:
            print(f"Task '{self._current_task.get_name()}' 해제")
        self._current_task = None

    def cancel_current_task(self):
        """현재 작업을 취소합니다."""
        if self._current_task:
            try:
                self._current_task.cancel()
                print(f"Task '{self._current_task.get_name()}'취소")
            except asyncio.CancelledError:
                print("작업이 이미 취소되었습니다.")
    
    async def run_task(self, coro, on_complete=None, on_error=None):
        """비동기 작업을 실행하고 예외를 처리합니다."""
        try:
            # 비동기 작업 실행
            await coro
        except asyncio.CancelledError:
            print("작업이 취소되었습니다.")
        except Exception as ex:
            print(f"오류가 발생했습니다: {str(ex)}")
            if on_error:
                on_error(str(ex))
        finally:
            # 작업 완료 시 수행할 작업
            if on_complete:
                on_complete()

def manage_task(task_manager_getter):
    """작업을 등록하고 취소하는 데코레이터."""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            task_manager = task_manager_getter(self)  # TaskManager 가져오기
            
            # 현재 작업을 asyncio 태스크로 등록
            task = asyncio.create_task(func(self, *args, **kwargs))
            task_manager.register_task(task)

            try:
                result = await task  # 실제 작업 수행
                return result
            except asyncio.CancelledError:
                print("작업이 취소되었습니다.")
                raise
            finally:
                # 작업 완료 또는 취소 시 등록 해제
                task_manager.unregister_task()

        return wrapper
    return decorator
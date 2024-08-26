class Event:
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        """이벤트를 구독하는 메서드"""
        self.listeners.append(listener)

    def emit(self, *args, **kwargs):
        """이벤트 발생 시 모든 구독자에게 알림"""
        for listener in self.listeners:
            listener(*args, **kwargs)

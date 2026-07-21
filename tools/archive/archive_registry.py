
class ArchiveRegistry:
    def __init__(self):
        self.handlers = {}
    def register(self, ext, handler_class):
        self.handlers[ext] = handler_class()
    def get_handler(self, ext):
        return self.handlers.get(ext)
registry = ArchiveRegistry()

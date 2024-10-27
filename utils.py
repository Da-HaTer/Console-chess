class Logger:
    def __init__(self, debug_mode=False):
        self.mode=debug_mode
    
    def log(self, *values):
        if self.mode:
            print(*values)

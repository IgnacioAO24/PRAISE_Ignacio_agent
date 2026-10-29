from renderers import IRenderer

class ConsoleRenderer(IRenderer):
    
    def __init__(self):
        self.environment_statebuffer = {}
        self.cont = 0
        self.N = 15
        self.last_board = None
    
    def observe(self, statebuffer):
        self.environment_statebuffer = statebuffer
    
    def render(self, force=False, titulo="Tablero actual"):
        state = self.environment_statebuffer.get_state()
        new_state = state is not None
        if new_state:
            self.last_board = state["board"]
            self.cont += 1
        if self.last_board and (force or (new_state and self.cont % self.N == 0)):
            print(f"\n{titulo}:")
            for row in self.last_board:
                print(" ".join(str(v) if v != 0 else '.' for v in row))

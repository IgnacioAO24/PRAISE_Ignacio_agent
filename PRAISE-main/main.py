import os
from SudokuWorld import SudokuEnvironment
from sudokuagent import SudokuAgent
from boards import SudokuRepository
from sudokurenderers import ConsoleRenderer
from statebuffer import StateBuffer
import threading

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def chosen_difficulty():
    options = {"1": "easy", "2": "medium", "3": "hard"}
    mensaje = """choose a difficulty
    1) easy
    2) medium
    3) hard
    """
    difficulty = input(mensaje)
    return options [difficulty]


agent_finished_flag = False
event_render_ready = threading.Event()

def agent_thread(agent):
    global agent_finished_flag
    while not agent.finished:
        agent.print_state()
        event_render_ready.wait(timeout=0.1)
        agent.behave()
        event_render_ready.clear()
    agent_finished_flag = True

def run(agent, env, renderer):
    statebuffer = StateBuffer(agent.id, env)
    renderer.observe(statebuffer)
    renderer.render(force=True, titulo="Tablero inicial")
    while not agent.finished:
        agent.behave()
        renderer.render()
    renderer.render(force=True, titulo="Tablero final")
    
def render_thread(renderer):
    while not agent_finished_flag:
        renderer.render()
        event_render_ready.set()


if __name__ == '__main__':
    clear_terminal()
    print("Sudoku Solver")
    difficulty = chosen_difficulty()
    repository = SudokuRepository()
    board = repository.load_random(difficulty)
    env = SudokuEnvironment(board)
    agent = SudokuAgent(env)
    renderer = ConsoleRenderer()
    #run(agent, env, renderer)
    
    thread_agent = threading.Thread(target=agent_thread, args=(agent,))
    thread_renderer = threading.Thread(target=render_thread, args=(renderer,))

    thread_renderer.start()
    thread_agent.start()

    thread_agent.join()
    thread_renderer.join()

    agent.print_state()
    
    
    #print(repr(difficulty))
    #print(board_path)
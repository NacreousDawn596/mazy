from Maze import *
import shutil

width, height = shutil.get_terminal_size()

def check_moves_iterative() -> None:
    stack = [maze.agent.coords]
    while stack:
        current_coord = stack.pop()
        moves: list = maze.get_moves(current_coord)
        maze.agent.label: str = f"{random.choice(maze.colors)}@{Style.RESET_ALL}" if len(moves) > 1 else maze.agent.label
        for coord in moves:
            maze.move(coord)
            stack.append(coord)
    raise Exception("no possible paths found")

while True:
    maze: Maze = Maze(int(width/2), int(height) - 4)
    maze.log()
    try:
        check_moves_iterative()
    except Exception as e:
        print(e)
    print("new try in 5s", end='')
    for i in range(6):
        time.sleep(1)
        print(f"\rnew try in {5-i}s", end='')
    

import random
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import sys
import time

colorama_init()

class Maze:
    class Agent:
        def __init__(self, label: str, coords: tuple) -> None:
            self.label = label
            self.coords = coords
            
    def __init__(self, width: int, height: int, agent_label: str = "@", enable_colors: bool = True, end_symbol: str = f"{Fore.RED}E{Style.RESET_ALL}", start_symbol: str = "S") -> None:
        self.maze, self.start, self.end, self.end_symbol, self.start_symbol = self.ttg(self.generate_maze, width=width, height=height, end_symbol=end_symbol, start_symbol=start_symbol)
        self.colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.YELLOW]
        self.agent: self.Agent = self.Agent(agent_label if not enable_colors else f"{random.choice(self.colors)}{agent_label}{Style.RESET_ALL}", self.start)
        self.move(self.start)
        
    def ttg(self, func, **args):
        try: result = func(**args)
        except Exception as e: result = self.ttg(func, **args)
        return result

        
    def generate_maze(self, width: int, height: int, end_symbol: str, start_symbol: str) -> tuple:
        maze: list = [['#' for _ in range(width)] for _ in range(height)]

        is_valid = lambda x, y: 0 <= x < width and 0 <= y < height and maze[y][x] == '#'

        def carve_path(x, y):
            directions: list = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny):
                    maze[ny][nx]: str = ' '
                    maze[(y + ny) // 2][(x + nx) // 2] = ' '
                    carve_path(nx, ny)

        start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
        end_x, end_y = random.randrange(1, width, 2), random.randrange(1, height, 2)

        maze[start_y][start_x] = start_symbol
        maze[end_y][end_x] = end_symbol

        carve_path(start_x, start_y)

        maze[start_y][start_x + 1]: str = ' '
        maze[end_y][end_x - 1]: str = ' '

        for i in range(width):
            maze[0][i] = maze[height-1][i] = '#'
        for i in range(height):
            maze[i][0] = maze[i][width-1] = '#'

        return maze, (start_x, start_y), (end_x, end_y), end_symbol, start_symbol

    def log(self) -> None:
        # assuming the max I'll ever set is 100, I'll fix it later
        # TODO: fix this STUPID code
        # print(len(str(len(self.maze) + 1))*' ', ' '.join([str(i // 10) for i in range(0, len(self.maze[0]))]))
        # print(len(str(len(self.maze) + 1))*' ', ' '.join([str(i % 10) for i in range(0, len(self.maze[0]))]))
        # for i, row in zip([str(i).zfill(len(str(len(self.maze) + 1))) for i in range(0, len(self.maze) + 1)], self.maze):
        #     print(i, ' '.join(row))
        # this was old code for debugging, here's a new one:
        print('\033c', end='')
        for row in self.maze:
            print(' '.join(row))
        print("The end coords are: ", self.end)
            
    def get_moves(self, coords: tuple) -> list:
        if any([self.maze[y][x] == self.end_symbol or (x, y) == self.end for x, y in ((coords[0], coords[1] - 1), (coords[0], coords[1] + 1), (coords[0] + 1, coords[1]), (coords[0] - 1, coords[1]))]):
            raise Exception("GOAL REACHED")
        return [(x, y) for x, y in ((coords[0], coords[1] - 1), (coords[0], coords[1] + 1), (coords[0] + 1, coords[1]), (coords[0] - 1, coords[1])) if self.maze[y][x] == ' ']
    
    def move(self, new_coords: tuple) -> None:
        self.agent.coords = new_coords
        self.maze[new_coords[1]][new_coords[0]] = self.agent.label
        self.log()
        sys.stdout.flush()
        time.sleep(0.1) # comment this line to make it as fast as python can, too lazy to rewrite in C or rust :')
        # however I'll try to rewrite later
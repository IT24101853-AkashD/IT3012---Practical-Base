# agent.py
import math
from collections import deque
import heapq

class SearchAgent:
    def __init__(self):
        self.plan = []
        # LAB 4 TASK: Now set to AStar!
        self.active_algo = 'AStar' 

    def sense_and_act(self, percept):
        if not self.plan and percept['all_food']:
            start = tuple(percept['agent_pos'])
            
            closest_food = min(
                percept['all_food'], 
                key=lambda f: abs(f[0] - start[0]) + abs(f[1] - start[1])
            )
            
            walls = set(percept['walls'])
            grid_size = percept['grid_size']

            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start, closest_food, walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, closest_food, walls, grid_size)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, closest_food, walls, grid_size)
            # LAB 4 NEW: A* Execution
            elif self.active_algo == 'AStar':
                self.plan = self.astar_search(start, closest_food, walls, grid_size)

        if self.plan:
            return self.plan.pop(0)
            
        return 'Stay'

    def get_successors(self, pos, walls, grid_size):
        x, y = pos
        moves = {'Up': (x, y + 1), 'Down': (x, y - 1), 'Left': (x - 1, y), 'Right': (x + 1, y)}
        valid_moves = []
        for action, (nx, ny) in moves.items():
            if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1] and (nx, ny) not in walls:
                valid_moves.append((action, (nx, ny)))
        return valid_moves

    # ==========================================
    # LAB 4: HEURISTIC FUNCTIONS
    # ==========================================
    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt((pos[0] - goal[0])**2 + (pos[1] - goal[1])**2)

    # ==========================================
    # LAB 4: A* SEARCH ALGORITHM
    # ==========================================
    def astar_search(self, start, goal, walls, grid_size, heuristic_type='manhattan'):
        count = 0 # Tie-breaker to prevent heapq crashes
        
        # Initial costs
        g_cost = 0
        h_cost = self.manhattan_distance(start, goal) if heuristic_type == 'manhattan' else self.euclidean_distance(start, goal)
        f_cost = g_cost + h_cost
        
        # Tuple format: (f_cost, count, g_cost, current_pos, path_taken)
        frontier = [(f_cost, count, g_cost, start, [])]
        reached = {} 
        
        while frontier:
            f, _, g, curr_pos, path = heapq.heappop(frontier)
            
            if curr_pos == goal:
                return path
                
            if curr_pos not in reached or g <= reached[curr_pos]:
                reached[curr_pos] = g
                
                for action, next_pos in self.get_successors(curr_pos, walls, grid_size):
                    new_g = g + 1
                    
                    if next_pos not in reached or new_g < reached[next_pos]:
                        reached[next_pos] = new_g
                        
                        if heuristic_type == 'manhattan':
                            new_h = self.manhattan_distance(next_pos, goal)
                        else:
                            new_h = self.euclidean_distance(next_pos, goal)
                            
                        new_f = new_g + new_h
                        count += 1
                        heapq.heappush(frontier, (new_f, count, new_g, next_pos, path + [action]))
        return []

    # (BFS, DFS, UCS functions below remain identical to Lab 3)
    def bfs_search(self, start, goal, walls, grid_size):
        frontier = deque([(start, [])])
        reached = {start}
        while frontier:
            curr_pos, path = frontier.popleft()
            if curr_pos == goal: return path
            for action, next_pos in self.get_successors(curr_pos, walls, grid_size):
                if next_pos not in reached:
                    reached.add(next_pos)
                    frontier.append((next_pos, path + [action]))
        return []

    def dfs_search(self, start, goal, walls, grid_size):
        frontier = [(start, [])]
        reached = set()
        while frontier:
            curr_pos, path = frontier.pop()
            if curr_pos == goal: return path
            if curr_pos not in reached:
                reached.add(curr_pos)
                for action, next_pos in self.get_successors(curr_pos, walls, grid_size):
                    if next_pos not in reached:
                        frontier.append((next_pos, path + [action]))
        return []

    def ucs_search(self, start, goal, walls, grid_size):
        count = 0 
        frontier = [(0, count, start, [])] 
        reached = {} 
        while frontier:
            cost, _, curr_pos, path = heapq.heappop(frontier)
            if curr_pos == goal: return path
            if curr_pos not in reached or cost <= reached[curr_pos]:
                reached[curr_pos] = cost
                for action, next_pos in self.get_successors(curr_pos, walls, grid_size):
                    new_cost = cost + 1 
                    if next_pos not in reached or new_cost < reached[next_pos]:
                        reached[next_pos] = new_cost
                        count += 1
                        heapq.heappush(frontier, (new_cost, count, next_pos, path + [action]))
        return []
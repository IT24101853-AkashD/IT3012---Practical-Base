# agent.py
from collections import deque
import heapq

class SearchAgent:
    def __init__(self):
        self.plan = []
        # LAB 3 TASK: Change this to 'DFS' or 'UCS' to observe the different behaviors!
        self.active_algo = 'BFS' 

    def sense_and_act(self, percept):
        # If we don't have a plan, create one!
        if not self.plan and percept['all_food']:
            start = tuple(percept['agent_pos'])
            
            # Find the closest food pellet using Manhattan distance
            closest_food = min(
                percept['all_food'], 
                key=lambda f: abs(f[0] - start[0]) + abs(f[1] - start[1])
            )
            
            walls = set(percept['walls'])
            grid_size = percept['grid_size']

            # Generate the plan based on the active algorithm
            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(start, closest_food, walls, grid_size)
            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(start, closest_food, walls, grid_size)
            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(start, closest_food, walls, grid_size)

        # Execute the plan step-by-step
        if self.plan:
            return self.plan.pop(0)
            
        return 'Stay'

    def get_successors(self, pos, walls, grid_size):
        """Helper function to find valid adjacent moves."""
        x, y = pos
        moves = {'Up': (x, y + 1), 'Down': (x, y - 1), 'Left': (x - 1, y), 'Right': (x + 1, y)}
        valid_moves = []
        
        for action, (nx, ny) in moves.items():
            # Check grid boundaries and walls
            if 0 <= nx < grid_size[0] and 0 <= ny < grid_size[1] and (nx, ny) not in walls:
                valid_moves.append((action, (nx, ny)))
                
        return valid_moves

    def bfs_search(self, start, goal, walls, grid_size):
        """Breadth-First Search using a FIFO queue (deque)"""
        frontier = deque([(start, [])])
        reached = {start}
        
        while frontier:
            curr_pos, path = frontier.popleft()
            
            if curr_pos == goal:
                return path
                
            for action, next_pos in self.get_successors(curr_pos, walls, grid_size):
                if next_pos not in reached:
                    reached.add(next_pos)
                    frontier.append((next_pos, path + [action]))
        return []

    def dfs_search(self, start, goal, walls, grid_size):
        """Depth-First Search using a LIFO stack (list)"""
        frontier = [(start, [])]
        reached = set()
        
        while frontier:
            curr_pos, path = frontier.pop()
            
            if curr_pos == goal:
                return path
                
            if curr_pos not in reached:
                reached.add(curr_pos)
                for action, next_pos in self.get_successors(curr_pos, walls, grid_size):
                    if next_pos not in reached:
                        frontier.append((next_pos, path + [action]))
        return []

    def ucs_search(self, start, goal, walls, grid_size):
        """Uniform-Cost Search using a Priority Queue (heapq)"""
        count = 0 # Tie-breaker for identical costs
        frontier = [(0, count, start, [])] 
        reached = {} # Maps positions to the lowest cost found so far
        
        while frontier:
            cost, _, curr_pos, path = heapq.heappop(frontier)
            
            if curr_pos == goal:
                return path
                
            if curr_pos not in reached or cost <= reached[curr_pos]:
                reached[curr_pos] = cost
                for action, next_pos in self.get_successors(curr_pos, walls, grid_size):
                    new_cost = cost + 1 # Each step has a cost of 1
                    if next_pos not in reached or new_cost < reached[next_pos]:
                        reached[next_pos] = new_cost
                        count += 1
                        heapq.heappush(frontier, (new_cost, count, next_pos, path + [action]))
        return []
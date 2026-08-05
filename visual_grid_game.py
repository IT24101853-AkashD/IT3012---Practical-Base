import random
import tkinter as tk


class VisualGridHuntGame:
    """Pacman style grid environment for Intelligent Systems Lab 2"""

    def __init__(self, width=10, height=10, num_food=10, num_opponents=2, custom_walls=None):

        self.width = width
        self.height = height
        self.agent_pos = [0, 0]

        if custom_walls:
            self.walls = set(custom_walls)
        else:
            self.walls = {(2, 2), (2, 3), (5, 5), (6, 5), (3, 7)}

        self.food_positions = set()

        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)

            if (fx, fy) != (0, 0) and (fx, fy) not in self.walls:
                self.food_positions.add((fx, fy))

        self.opponents = []

        while len(self.opponents) < num_opponents:
            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)

            if (ox, oy) != (0, 0) and (ox, oy) not in self.walls:
                self.opponents.append([ox, oy])

        self.score = 0
        self.steps = 0
        self.collision = False


    # Partial Observable Environment
    def get_percept(self):

        x, y = self.agent_pos

        return {
            "wall_ahead": (x, y + 1) in self.walls,
            "food_here": tuple(self.agent_pos) in self.food_positions
        }


    def execute_action(self, action):

        self.steps += 1

        new_pos = list(self.agent_pos)

        if action == "Up":
            new_pos[1] += 1

        elif action == "Down":
            new_pos[1] -= 1

        elif action == "Left":
            new_pos[0] -= 1

        elif action == "Right":
            new_pos[0] += 1


        if (
            new_pos[0] < 0 or
            new_pos[0] >= self.width or
            new_pos[1] < 0 or
            new_pos[1] >= self.height
        ):
            self.score -= 5

        elif tuple(new_pos) in self.walls:
            self.score -= 5

        else:
            self.agent_pos = new_pos


        if tuple(self.agent_pos) in self.food_positions:
            self.food_positions.remove(tuple(self.agent_pos))
            self.score += 20



    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 60
        )



# Simple Reflex Agent
class SimpleReflexAgent:

    def sense_and_act(self, percept):

        if percept["food_here"]:
            return "suck"

        elif percept["wall_ahead"]:
            return "Left"

        else:
            return "Up"



# Model Based Agent
class ModelBasedAgent:

    def __init__(self):

        self.visited_cells = set()
        self.last_action = None


    def sense_and_act(self, percept):

        current_state = str(percept)

        self.visited_cells.add(current_state)


        if percept["food_here"]:
            self.last_action = "suck"


        elif percept["wall_ahead"]:
            self.last_action = "Left"


        else:
            self.last_action = "Up"


        return self.last_action




class GridGameGUI:


    def __init__(self, root):

        self.root = root

        self.root.title("SE3062 Lab 02 Intelligent Agent")


        self.env = VisualGridHuntGame(
            width=10,
            height=10,
            num_food=10,
            num_opponents=0
        )


        self.agent = ModelBasedAgent()


        self.cell_size = 50


        self.canvas = tk.Canvas(
            root,
            width=500,
            height=500
        )

        self.canvas.pack()


        self.label = tk.Label(
            root,
            text="Score: 0"
        )

        self.label.pack()


        self.button = tk.Button(
            root,
            text="Start",
            command=self.run
        )

        self.button.pack()


        self.draw_grid()



    def draw_grid(self):

        self.canvas.delete("all")


        for x in range(self.env.width):

            for y in range(self.env.height):

                x1 = x * self.cell_size
                y1 = (self.env.height-y-1)*self.cell_size

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x1+self.cell_size,
                    y1+self.cell_size,
                    fill="white"
                )


        for fx,fy in self.env.food_positions:

            self.canvas.create_oval(
                fx*self.cell_size+15,
                (self.env.height-fy-1)*self.cell_size+15,
                fx*self.cell_size+35,
                (self.env.height-fy-1)*self.cell_size+35,
                fill="orange"
            )


        ax,ay=self.env.agent_pos


        self.canvas.create_oval(
            ax*self.cell_size+10,
            (self.env.height-ay-1)*self.cell_size+10,
            ax*self.cell_size+40,
            (self.env.height-ay-1)*self.cell_size+40,
            fill="blue"
        )



    def run(self):

        if not self.env.is_done():

            percept=self.env.get_percept()

            action=self.agent.sense_and_act(percept)


            if action=="suck":

                self.env.execute_action("Up")

            else:

                self.env.execute_action(action)


            self.draw_grid()


            self.label.config(
                text=f"Score: {self.env.score} Steps: {self.env.steps}"
            )


            self.root.after(
                500,
                self.run
            )



if __name__=="__main__":

    root=tk.Tk()

    app=GridGameGUI(root)

    root.mainloop()
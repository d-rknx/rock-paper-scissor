import tkinter as tk
import random

# emojis for rock, paper, scissors
EMOJIS = {
    "Rock": "🗿",
    "Paper": "🧻",
    "Scissors": "✂"
}

# colours for each type
COLORS = {
    "Rock": "gray",
    "Paper": "white",
    "Scissors": "red"
}

# rules
RULES = {
    "Rock": "Scissors",
    "Paper": "Rock",
    "Scissors": "Paper"
}

class RPSGame:
    def __init__(self, root, credits):
        self.root = root
        self.root.title("rock paper scissors battle")
        self.credits = credits
        self.bet = 0
        self.user_choice = None

        self.main_frame = tk.Frame(root, bg="black")
        self.main_frame.pack(fill="both", expand=True)
        
        self.title_label = tk.Label(self.main_frame, text="rock paper scissors", font=("Arial", 24), fg="white", bg="black")
        self.title_label.pack(pady=20)

        self.play_button = tk.Button(self.main_frame, text="play", font=("Arial", 16), command=self.start_game)
        self.play_button.pack(pady=10)

        self.bet_button = tk.Button(self.main_frame, text="bet", font=("Arial", 16), command=self.bet_screen)
        self.bet_button.pack(pady=10)

        self.credits_label = tk.Label(self.main_frame, text=f"credits: {self.credits}", font=("Arial", 16), fg="white", bg="black")
        self.credits_label.pack(pady=20)

    def start_game(self):
        self.main_frame.destroy()
        self.setup_game_canvas()

    def bet_screen(self):
        self.main_frame.destroy()
        self.bet_frame = tk.Frame(self.root, bg="black")
        self.bet_frame.pack(fill="both", expand=True)

        tk.Label(self.bet_frame, text="place your bet", font=("Arial", 24), fg="white", bg="black").pack(pady=20)

        self.bet_entry = tk.Entry(self.bet_frame, font=("Arial", 16))
        self.bet_entry.pack(pady=10)

        self.choice_var = tk.StringVar(value="Rock")
        for choice in ["Rock", "Paper", "Scissors"]:
            tk.Radiobutton(
                self.bet_frame, text=choice, variable=self.choice_var, value=choice,
                font=("Arial", 16), fg="white", bg="black", selectcolor="black"
            ).pack(anchor="w", padx=50)

        tk.Button(self.bet_frame, text="confirm", font=("Arial", 16), command=self.confirm_bet).pack(pady=10)

    def confirm_bet(self):
        try:
            self.bet = int(self.bet_entry.get())
            if self.bet <= 0 or self.bet > self.credits:
                raise ValueError
        except ValueError:
            tk.Label(self.bet_frame, text="invalid bet amount!", font=("Arial", 12), fg="red", bg="black").pack()
            return

        self.user_choice = self.choice_var.get()
        self.credits -= self.bet
        self.bet_frame.destroy()
        self.start_game()

    def setup_game_canvas(self):
        self.width = 800
        self.height = 600

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.objects = []
        for _ in range(20):
            self.create_object("Rock")
            self.create_object("Paper")
            self.create_object("Scissors")

        self.animate()

    def create_object(self, obj_type):
        x = random.randint(50, self.width - 50)
        y = random.randint(50, self.height - 50)
        dx = random.choice([-3, -2, 2, 3])
        dy = random.choice([-3, -2, 2, 3])
        obj_id = self.canvas.create_text(x, y, text=EMOJIS[obj_type], font=("Arial", 24), fill=COLORS[obj_type])
        self.objects.append({"type": obj_type, "id": obj_id, "dx": dx, "dy": dy})

    def animate(self):
        for obj in list(self.objects):
            if not self.canvas.bbox(obj["id"]):
                continue
            x1, y1, x2, y2 = self.canvas.bbox(obj["id"])
            dx = obj["dx"]
            dy = obj["dy"]

            if x1 + dx < 0 or x2 + dx > self.width:
                obj["dx"] = -dx
            if y1 + dy < 0 or y2 + dy > self.height:
                obj["dy"] = -dy

            self.canvas.move(obj["id"], obj["dx"], obj["dy"])

        self.check_collisions()

        if len(self.objects) > 1:
            self.root.after(16, self.animate)
        else:
            self.declare_winner()

    def check_collisions(self):
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]

                if not self.canvas.bbox(obj1["id"]) or not self.canvas.bbox(obj2["id"]):
                    continue

                if self.is_collision(obj1, obj2):
                    if RULES[obj1["type"]] == obj2["type"]:
                        self.transform_object(obj2, obj1["type"])
                    elif RULES[obj2["type"]] == obj1["type"]:
                        self.transform_object(obj1, obj2["type"])

    def is_collision(self, obj1, obj2):
        bbox1 = self.canvas.bbox(obj1["id"])
        bbox2 = self.canvas.bbox(obj2["id"])
        return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])

    def transform_object(self, obj, new_type):
        obj["type"] = new_type
        self.canvas.itemconfig(obj["id"], text=EMOJIS[new_type], fill=COLORS[new_type])

    def declare_winner(self):
        types_left = set(obj["type"] for obj in self.objects)
        
        if len(types_left) == 1:
            winning_type = types_left.pop()
            self.canvas.create_text(self.width // 2, self.height // 2, text=f"{winning_type} wins!", font=("Arial", 32), fill="green")

            if self.user_choice == winning_type:
                self.credits += self.bet * 2

            self.root.after(3000, self.show_main_screen)

    def show_main_screen(self):
        self.canvas.destroy()
        self.__init__(self.root, self.credits)

if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root, credits=100)
    root.mainloop()

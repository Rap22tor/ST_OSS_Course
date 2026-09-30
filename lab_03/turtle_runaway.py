# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.game_loop_running = False
        self.paused = False
        self.state = 'play'     # 'play', 'caught' or 'returning'
        self.time_left = 0
        self.last_time = time.time()
        self.on_time_up = lambda: None  # set by the menu code

        # Initialize 'runner' and 'chaser'
        self.setup_turtle(self.runner, 'blue')
        self.setup_turtle(self.chaser, 'red')

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.banner = turtle.RawTurtle(canvas)
        self.banner.hideturtle()
        self.banner.penup()

    def setup_turtle(self, t, color):
        t.shape('turtle')
        t.color(color)
        t.penup()
        t.speed(0)

    def swap_turtle(self, old, new, color):
        self.setup_turtle(new, color)
        new.setpos(old.pos())
        new.setheading(old.heading())
        old.hideturtle()

    def set_runner(self, new):
        self.swap_turtle(self.runner, new, 'blue')
        self.runner = new

    def set_chaser(self, new):
        self.swap_turtle(self.chaser, new, 'red')
        self.chaser = new

    def is_caught(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def reset_positions(self):
        self.runner.setpos((-self.init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+self.init_dist / 2, 0))
        self.chaser.setheading(180)

    def start(self, init_dist=400, ai_timer_msec=100, game_time=30):
        self.init_dist = init_dist
        self.ai_timer_msec = ai_timer_msec
        self.game_time = game_time
        self.time_left = game_time
        self.score = 0
        self.state = 'play'
        self.banner.clear()
        self.reset_positions()

        if not self.game_loop_running:
            # starts the initial game loop, but restarts don't affect this
            self.game_loop_running = True
            self.canvas.ontimer(self.step, self.ai_timer_msec)

    # smooth glide for after catch
    def glide(self, t, start, target, frac):
        (x0, y0), h0 = start
        (x1, y1), h1 = target
        t.setpos(x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac)
        t.setheading(h0 + ((h1 - h0 + 180) % 360 - 180) * frac)

    def step(self):
        # use actual time to avoid slow timer due to slow frames
        now = time.time()
        elapsed = now - self.last_time
        self.last_time = now
        if self.paused:
            pass
        elif self.state == 'play' and self.time_left > 0:
            self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
            self.chaser.run_ai(self.runner.pos(), self.runner.heading())
            self.time_left -= elapsed

            # set state 'caught' to trigger reset logic
            if self.is_caught():
                self.score += 1
                self.state = 'caught'
                self.reset_frames_remaining = 10
                self.banner.setpos(0, 0)
                self.banner.write('Caught!', align='center', font=('Arial', 32, 'bold'))
        elif self.state == 'caught':
            # very incredibly epic reset animation
            self.reset_frames_remaining -= 1
            if self.reset_frames_remaining == 0:
                self.banner.clear()
                self.state = 'returning'
                self.reset_frames_remaining = 10
                self.runner_from = (self.runner.pos(), self.runner.heading())
                self.chaser_from = (self.chaser.pos(), self.chaser.heading())
        elif self.state == 'returning':
            self.reset_frames_remaining -= 1
            frac = 1 - self.reset_frames_remaining / 10
            d = self.init_dist / 2
            self.glide(self.runner, self.runner_from, ((-d, 0), 0), frac)
            self.glide(self.chaser, self.chaser_from, ((d, 0), 180), frac)
            if self.reset_frames_remaining == 0:
                self.state = 'play'

        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Time: {max(self.time_left, 0):.0f}  Score: {self.score}')

        # End of round logic
        if self.state == 'play' and not self.paused and self.time_left <= 0:
            self.on_time_up()

        # Triggering a canvas update here avoids
        # canvas updates after every turtle move
        self.canvas.update()

        # Note:) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Arrow keys and WASD support, including holding multiple keys :D
        self.held = set()
        self.actions = {
            'Up': lambda: self.forward(self.step_move),
            'w': lambda: self.forward(self.step_move),
            'Down': lambda: self.backward(self.step_move),
            's': lambda: self.backward(self.step_move),
            'Left': lambda: self.left(self.step_turn),
            'a': lambda: self.left(self.step_turn),
            'Right': lambda: self.right(self.step_turn),
            'd': lambda: self.right(self.step_turn),
        }

        # Register event handlers
        for key in self.actions:
            canvas.onkeypress(lambda k=key: self.held.add(k), key)
            canvas.onkeyrelease(lambda k=key: self.held.discard(k), key)
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        for key in self.held:
            self.actions[key]()

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

def turn_toward(t, angle):
    # Turn by at most step_turn towards the given heading
    diff = (angle - t.heading() + 180) % 360 - 180
    t.left(max(-t.step_turn, min(t.step_turn, diff)))

# Theoretically perfect chaser, always moves towards runner
class SmartChaser(turtle.RawTurtle):
    def __init__(self, canvas, step_move=15, step_turn=30):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        turn_toward(self, self.towards(opp_pos))
        self.forward(self.step_move)

# Theoretically perfect runner (in a very naive way at the very least)
# Attempts to always turn away as much as possible from the chaser and run
class SmartRunner(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=30):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        x, y = self.pos()
        # Don't run into edges
        if abs(x) > 300 or abs(y) > 300:
            angle = self.towards(0, 0)
        else:
            angle = self.towards(opp_pos) + 180 # Naive "run away from chaser" implementation
        turn_toward(self, angle)
        self.forward(self.step_move)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    root.title('Turtle Runaway')
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.tracer(0)  # prevent automatic redraws

    runner = SmartRunner(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start() # start game logic

    runner_types = [('Manual', ManualMover), ('Random', RandomMover), ('Smart', SmartRunner)]
    chaser_types = [('Manual', ManualMover), ('Random', RandomMover), ('Smart', SmartChaser)]

    # Menu logic, for swapping tutel types, restarting, etc
    def make_type_button(role, types, index, set_turtle):
        button = tk.Button(canvas, text=f'{role}: {types[index][0]}')
        state = {'index': index}

        def click():
            state['index'] = (state['index'] + 1) % len(types)
            name, cls = types[state['index']]
            set_turtle(cls(screen))
            button.config(text=f'{role}: {name}')
            canvas.tag_raise('menu')  # the new turtle must stay behind the menu
            screen.listen()

        button.config(command=click)
        return button

    def open_menu(time_up=False):
        game.paused = True
        canvas.create_rectangle(-350, -350, 350, 350, fill='gray', stipple='gray50', tags='menu')
        title = 'Time is up!' if time_up else 'Paused'
        canvas.create_text(0, -120, text=title, font=('Arial', 28, 'bold'), tags='menu')
        buttons = menu_buttons
        # slightly adjusted menu when time is up, to display final score and hide "resume" button
        if time_up:
            canvas.create_text(0, -80, text=f'Final score: {game.score}',
                               font=('Arial', 18), tags='menu')
            buttons = menu_buttons[:3]  # nothing to resume
        for i, button in enumerate(buttons):
            canvas.create_window(0, -40 + i * 45, window=button, width=160, tags='menu')

    def close_menu():
        canvas.delete('menu')
        game.paused = False
        screen.listen()

    def toggle_menu(event=None):
        if game.time_left <= 0:
            return  # after time is up, the menu only closes with Restart
        if game.paused:
            close_menu()
        else:
            open_menu()

    def restart():
        game.start()
        close_menu()

    menu_buttons = [
        make_type_button('Runner', runner_types, 2, game.set_runner),
        make_type_button('Chaser', chaser_types, 0, game.set_chaser),
        tk.Button(canvas, text='Restart', command=restart),
        tk.Button(canvas, text='Resume', command=close_menu),
    ]
    root.bind('<Escape>', toggle_menu)
    game.on_time_up = lambda: open_menu(time_up=True)

    screen.mainloop()

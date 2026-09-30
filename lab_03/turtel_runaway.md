# Turtel Runaway

## Mission: Timer
Added a simple game timer using the actual machine time. This way, no matter how long a frame takes to render, the timer is always accurate. 

## Mission: My [Tutels](https://www.youtube.com/watch?v=oxzEdm29JLw) :D
Added two new turtles:
- Smart Runner
- Smart Chaser

They're both "theoretically" perfect AI's, with the runner always running in the opposite direction of the chaser, and the chaser always moving perfectly towards the runner.

## Mission: Scoring System
Added a simple scoring system, counting the amount of times the chaser caught the runner. The chaser has 30 seconds per round, and every time the runner is caught, both runner and chaser are reset to their starting positions (With a very epic and cool animation thank you very much). This way, the score is simply the amount of times the runner was caught.

## Misison: Extra Stuff
- Improved performance by manually calling canvas update
- Added a Pause Menu (ESC Key), including resume and restart
- Added WASD support (because I'm a real gamer)
- Added support for holding down keys, so pressing a new key doesn't interrupt the old action. This enables for example turning and moving forward at the same time.
- Added a Time Up screen (It's just the Pause Menu but a bit different)
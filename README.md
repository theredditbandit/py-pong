# Py-Pong Game

This is a fork of the Py-Pong game by [theredditbandit](https://github.com/theredditbandit) - Description of the contribution, with updates to fix some of the biggest bugs which are updated in his repository [py-pong](https://github.com/theredditbandit/py-pong).

## Installation

1. Clone the repository to your local machine.
   ```shell
   git clone https://github.com/theredditbandit/py-pong 
   ```

2. Make sure you have Python installed.

3. Install the required dependencies.
   ```shell
   pip install pygame
   ```

## Usage

To run the game, navigate to the project directory and run the following command:
```shell
python solution.py
```

## Gameplay

- Use the **W** and **S** keys to move the left paddle up and down, respectively.
- Use the **Up Arrow** and **Down Arrow** keys to move the right paddle up and down, respectively.

The objective of the game is to hit the ball with your paddle and score points by making the ball touch the opponent's side. The player who reaches the score limit first wins.

## Updates

The following updates have been made to fix the biggest bugs in the game:

- Fixed an issue where the ball would bounce out of the left goal instead of scoring a point.
- Addressed an infinite scoring bug that allowed the left player to gain infinite points by scoring once in the right side.
- Added dynamic window size functionality to make the game window resizable.
- Improved paddle movement responsiveness and added speed control.
- Enhanced collision detection between the ball and paddles.
- Updated the scoring system and added a game over screen.


## Credits

This game is based on the original Py-Pong game, created by the one and only [theredditbandit](https://github.com/theredditbandit). His repository link can be found here: https://github.com/theredditbandit/py-pong 

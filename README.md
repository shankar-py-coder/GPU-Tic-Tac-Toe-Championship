
# GPU Tic-Tac-Toe Championship

## Project Description

GPU Tic-Tac-Toe Championship is a competitive game in which two independent CUDA-based AI players compete against each other.

Both competitors use different decision-making strategies to select their moves. The game runs automatically until one player wins or the match ends in a draw.

## Project Objectives

- Implement two GPU-based competitors.
- Develop different AI decision-making strategies.
- Use CUDA kernels for move selection.
- Coordinate two competitor threads.
- Visualize the game and display its result.

## Technologies Used

- CUDA C++
- Python
- NumPy
- Matplotlib
- ctypes
- NVIDIA GPU
- Google Colab

## Competitor Strategies

### GPU Player 1 (X)

Uses a winning-first strategy.

1. Searches for an immediate winning move.
2. Blocks the opponent.
3. Selects the centre.
4. Selects a corner.
5. Selects any remaining position.

### GPU Player 2 (O)

Uses a defensive and positional strategy.

1. Searches for an immediate winning move.
2. Blocks the opponent.
3. Selects an available opposite-corner position.
4. Selects the centre.
5. Selects another available corner.
6. Selects any remaining position.

## System Architecture

Both competitors use independent CUDA kernels.

Python manages the game board and alternates between the competitors.

Dedicated worker threads execute the two competitors. A GPU lock coordinates access to the single available physical GPU.

## Project Structure

GPU_Tic_Tac_Toe/
- src/
  - game.py
  - player1.cu
  - player2.cu
  - gpu_players.py
  - main.py
  - threaded_main.py
  - visualize.py
- results/
  - game_animation.gif
- screenshots/
- README.md

## Execution

Compile Player 1:

nvcc -Xcompiler -fPIC -shared src/player1.cu -o src/player1.so

Compile Player 2:

nvcc -Xcompiler -fPIC -shared src/player2.cu -o src/player2.so

Run the game:

python src/main.py

Run the threaded competition:

python src/threaded_main.py

Generate visualization:

python src/visualize.py

## GPU Implementation

The project was developed in an environment with one NVIDIA GPU.

The two CUDA-based competitors operate independently and execute in separate worker threads. GPU access is coordinated using a lock.

This demonstrates two competing GPU-based programs without requiring two physical GPUs.

## Testing Results

- GPU Player 1 move selection: PASS
- GPU Player 2 move selection: PASS
- Winner detection: PASS
- Draw detection: PASS
- Project file verification: PASS

## Conclusion

The project demonstrates how CUDA kernels can be used to implement competing AI game strategies. It combines GPU programming, Python integration, multithreading and graphical visualization in an interactive game.

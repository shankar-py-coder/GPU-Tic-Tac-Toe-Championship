
#include <cuda_runtime.h>

__device__ int check_winner(int *board, int player)
{
    for (int r = 0; r < 3; r++)
        if (board[r*3] == player &&
            board[r*3+1] == player &&
            board[r*3+2] == player)
            return 1;

    for (int c = 0; c < 3; c++)
        if (board[c] == player &&
            board[c+3] == player &&
            board[c+6] == player)
            return 1;

    if (board[0] == player && board[4] == player && board[8] == player)
        return 1;

    if (board[2] == player && board[4] == player && board[6] == player)
        return 1;

    return 0;
}

__global__ void player2_kernel(int *board, int *move)
{
    if (threadIdx.x == 0)
    {
        int result = -1;

        // Priority 1: Find a winning move
        for (int i = 0; i < 9; i++)
        {
            if (board[i] == 0)
            {
                board[i] = 2;

                if (check_winner(board, 2))
                    result = i;

                board[i] = 0;

                if (result != -1)
                    break;
            }
        }

        // Priority 2: Block Player 1
        if (result == -1)
        {
            for (int i = 0; i < 9; i++)
            {
                if (board[i] == 0)
                {
                    board[i] = 1;

                    if (check_winner(board, 1))
                        result = i;

                    board[i] = 0;

                    if (result != -1)
                        break;
                }
            }
        }

        // Priority 3: Opposite corner
        if (result == -1)
        {
            int opposite[4] = {8, 6, 2, 0};

            for (int i = 0; i < 4; i++)
            {
                if (board[opposite[i]] == 0)
                {
                    result = opposite[i];
                    break;
                }
            }
        }

        // Priority 4: Centre
        if (result == -1 && board[4] == 0)
            result = 4;

        // Priority 5: Remaining corners
        if (result == -1)
        {
            int corners[4] = {0, 2, 6, 8};

            for (int i = 0; i < 4; i++)
            {
                if (board[corners[i]] == 0)
                {
                    result = corners[i];
                    break;
                }
            }
        }

        // Priority 6: Remaining positions
        if (result == -1)
        {
            for (int i = 0; i < 9; i++)
            {
                if (board[i] == 0)
                {
                    result = i;
                    break;
                }
            }
        }

        *move = result;
    }
}

extern "C" void get_player2_move(int *board, int *move)
{
    int *d_board, *d_move;

    cudaMalloc(&d_board, 9 * sizeof(int));
    cudaMalloc(&d_move, sizeof(int));

    cudaMemcpy(d_board, board, 9 * sizeof(int), cudaMemcpyHostToDevice);

    player2_kernel<<<1, 1>>>(d_board, d_move);

    cudaDeviceSynchronize();

    cudaMemcpy(move, d_move, sizeof(int), cudaMemcpyDeviceToHost);

    cudaFree(d_board);
    cudaFree(d_move);
}

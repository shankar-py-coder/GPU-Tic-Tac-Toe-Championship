
#include <cuda_runtime.h>

__device__ int check_line(int a, int b, int c, int player)
{
    if (a == player && b == player && c == 0)
        return 2;

    if (a == player && c == player && b == 0)
        return 1;

    if (b == player && c == player && a == 0)
        return 0;

    return -1;
}

__global__ void player1_kernel(int *board, int *move)
{
    int idx = threadIdx.x;

    if (idx == 0)
    {
        int result = -1;

        // First priority: Win immediately
        for (int i = 0; i < 9; i++)
        {
            if (board[i] == 0)
            {
                board[i] = 1;

                int win = 0;

                for (int r = 0; r < 3; r++)
                    if (board[r*3] == 1 &&
                        board[r*3+1] == 1 &&
                        board[r*3+2] == 1)
                        win = 1;

                for (int c = 0; c < 3; c++)
                    if (board[c] == 1 &&
                        board[c+3] == 1 &&
                        board[c+6] == 1)
                        win = 1;

                if (board[0] == 1 && board[4] == 1 && board[8] == 1)
                    win = 1;

                if (board[2] == 1 && board[4] == 1 && board[6] == 1)
                    win = 1;

                board[i] = 0;

                if (win)
                {
                    result = i;
                    break;
                }
            }
        }

        // Second priority: Block opponent
        if (result == -1)
        {
            for (int i = 0; i < 9; i++)
            {
                if (board[i] == 0)
                {
                    board[i] = 2;

                    int win = 0;

                    for (int r = 0; r < 3; r++)
                        if (board[r*3] == 2 &&
                            board[r*3+1] == 2 &&
                            board[r*3+2] == 2)
                            win = 1;

                    for (int c = 0; c < 3; c++)
                        if (board[c] == 2 &&
                            board[c+3] == 2 &&
                            board[c+6] == 2)
                            win = 1;

                    if (board[0] == 2 && board[4] == 2 && board[8] == 2)
                        win = 1;

                    if (board[2] == 2 && board[4] == 2 && board[6] == 2)
                        win = 1;

                    board[i] = 0;

                    if (win)
                    {
                        result = i;
                        break;
                    }
                }
            }
        }

        // Third priority: Centre
        if (result == -1 && board[4] == 0)
            result = 4;

        // Fourth priority: Corners
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

        // Final priority: Any empty position
        if (result == -1)
        {
            for (int i = 0; i < 9; i++)
                if (board[i] == 0)
                {
                    result = i;
                    break;
                }
        }

        *move = result;
    }
}

extern "C" void get_player1_move(int *board, int *move)
{
    int *d_board, *d_move;

    cudaMalloc(&d_board, 9 * sizeof(int));
    cudaMalloc(&d_move, sizeof(int));

    cudaMemcpy(d_board, board, 9 * sizeof(int), cudaMemcpyHostToDevice);

    player1_kernel<<<1, 1>>>(d_board, d_move);

    cudaDeviceSynchronize();

    cudaMemcpy(move, d_move, sizeof(int), cudaMemcpyDeviceToHost);

    cudaFree(d_board);
    cudaFree(d_move);
}

import random
import time
import tracemalloc

# hàm kiểm tra số đưa vào bảng có hợp lệ hay không
def is_valid(board, row, col, num):
    for i in range(9):

        # nếu hàng dọc hoặc hàng ngang có số giống với số được đưa vào, trả về false
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)

    # nếu trong ô nhỏ 3x3 có số giống với số được đưa vào, trả về false
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

# hàm khởi tạo bảng
def generate_random_board():

    # tạo bảng 3x3 gồm các ô nhỏ có kích cỡ 3x3
    board = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(random.randint(10, 20)):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
    
    # kiểm tra số được tạo có hợp lệ hay không
        if is_valid(board, row, col, num):
            board[row][col] = num
    return board

# hàm in các bước step-by-step
def print_step(board, row, col, num, action):
    step = f"{action} {num} at ({row}, {col})"
    file.write(f"\n{step}\n")
    print(step)
    print_board(board)

# hàm in bảng
def print_board(board):
    for i, row in enumerate(board):

        # vẽ hàng ngang phân cách
        if i % 3 == 0 and i != 0:
            border = "-" * 23
            file.write(f"{border}\n")
            print(border)
        row_str = ""
        for j, num in enumerate(row):

            # vẽ hàng cột phân cách
            if j % 3 == 0 and j != 0:
                row_str += " |"
            row_str += f" {num if num != 0 else '.'}"
        file.write(f"{row_str}\n")
        print(row_str)
    print("\n")

# hàm thực hiện tìm kiếm theo chiều sâu
# xét bảng vị trí từ 0-8
def dfs(board, row=0, col=0):
    global count
    # nếu row = 9 thì xét đã hết bảng, trả về true
    if row == 9:
        return True

    # nếu col = 9 thì đã hết cột, tiến hành xuống duyệt hàng tiếp theo 
    if col == 9:
        return dfs(board, row + 1, 0) 
    
    # tiến hành tìm các vị trí trống
    # tại vị trí đang xét nếu có số sẵn, duyệt cột tiếp theo
    if board[row][col] != 0:
        return dfs(board, row, col + 1)
    for num in range(1, 10):

        # nếu số đưa vào hợp lệ thì gán số
        if is_valid(board, row, col, num):
            board[row][col] = num

            # sử dụng hồi quy để duyệt liên tục các cột sau
            print_step(board, row, col, num, "Place")
            count = count + 1
            if dfs(board, row, col + 1):
                return True
            
            # nếu số không thỏa mãn thì lập tức xóa số đó và thử lại các con số khác
            board[row][col] = 0
            count = count + 1
            print_step(board, row, col, num, "Remove")
    return False 

# hàm main
def main():
    global file
    global count
    count = 0
    # mở file để tiến hành ghi vào file kết quả
    with open("sudoku_testcase.txt", "w") as file:
        tracemalloc.start()
        board = generate_random_board()
        file.write("Initial Board: \n")
        print("Initial Board: ")
        print_board(board)

        # đếm giờ
        start_time = time.time()

        # nếu giải thành công thì in bảng kết quả, ngược lại thì in ra không có kết quả
        if dfs(board):
            time.sleep(0.2)
            end_time = time.time()
            file.write("\nSolved Sudoku Board: \n")
            print("\nSolved Sudoku Board:")
            print_board(board)
            step_result = f"\nNumber of Steps: {count}"
            file.write(step_result)
            print(step_result)
            result =f"\nFinish time: {round(end_time - start_time)}s"
            file.write(result)
            print(result)
        else:
            result = "\nNo solutions."
            file.write(result)
            print(result)
        snapshot = tracemalloc.take_snapshot()

        # tính bộ nhớ và thời gian đã dùng
        mem_usage = sum(stat.size for stat in snapshot.statistics("lineno"))
        memory_result = f"\nMemory Used: {mem_usage / 1024:.2f} KB"
        file.write(memory_result)
        print(memory_result)

if __name__=="__main__":
    main()
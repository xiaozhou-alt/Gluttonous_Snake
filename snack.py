import pygame, sys, random
from pygame.math import Vector2 as V2

color_green = pygame.Color(187, 255, 121)
color_red = pygame.Color(255, 0, 0)
color_deep_green = pygame.Color(173, 234, 113)
color_black = pygame.Color(0, 0, 0)


# 游戏初始设定类
class GameSet():
    # 设置主窗口
    screen = None

    # 设置单元格大小和单元格号
    cell_size = 20
    cell_number = 40

    # 创建食物
    food = pygame.image.load(r'pic/apple.png')

    # 创建蛇
    snake = None

    # 初始分数
    score = 0

    def __init__(self):
        pass

    def start_game(self):
        # 游戏初始化
        pygame.init()
        # 建立窗口
        GameSet.screen = pygame.display.set_mode([GameSet.cell_size * \
                                                  GameSet.cell_number, GameSet.cell_size * GameSet.cell_number])
        # 设置初始帧频
        clock = pygame.time.Clock()

        # 初始化蛇和食物
        main_game = Main()

        # 设置一个计时器，让他每隔150毫秒进行一次
        Screen_update = pygame.USEREVENT
        pygame.time.set_timer(Screen_update, 100)

        # 主循环
        while 1:
            # 给背景填充成绿色
            GameSet.screen.fill(color_green)

            # 获取所有事件
            for event in pygame.event.get():
                # 点击退出按钮能直接结束程序
                if event.type == pygame.QUIT:
                    Main.game_over()

                # 当输入为设置好的自动输入的计时器效果时
                # 调用移动蛇的函数，相当于给蛇定速
                if event.type == Screen_update:
                    main_game.update()

                # 从键盘按下按键时的操作
                if event.type == pygame.KEYDOWN:
                    # 方向键上(余下同理)
                    if event.key == pygame.K_UP and main_game.snake.direction != V2(0, 1):
                        main_game.snake.direction = V2(0, -1)
                    if event.key == pygame.K_DOWN and main_game.snake.direction != V2(0, -1):
                        main_game.snake.direction = V2(0, 1)
                    if event.key == pygame.K_LEFT and main_game.snake.direction != V2(1, 0):
                        main_game.snake.direction = V2(-1, 0)
                    if event.key == pygame.K_RIGHT and main_game.snake.direction != V2(-1, 0):
                        main_game.snake.direction = V2(1, 0)

            # 在场景内绘制所有元素
            main_game.draw_elements()

            # 将绘制文字得到的画布，粘贴到窗口中（20,20）的位置
            GameSet.screen.blit(self.get_TextSurface('得分：%d'
                                                     % GameSet.score), (20, 20))
            if not main_game.snake.live:
                main_game.game_over()
            # 刷新页面
            pygame.display.update()

            # 设置帧频
            clock.tick(60)

    # 左上角文字绘制
    def get_TextSurface(self, text):
        # 初始化字体模块
        pygame.font.init()
        # 选择合适字体
        font = pygame.font.SysFont('kaiti', 40, False)
        # 使用对应字符完成绘制
        text_surface = font.render(text, True, color_black)
        return text_surface


# 主游戏类
class Main():
    def __init__(self):
        # 将蛇和食物初始化
        self.snake = Snake()
        self.food = Food()

    def update(self):
        # 更新控制蛇的移动
        self.snake.move_snake()
        # 更新控制蛇吃到食物
        self.check_collision()
        # 更新判断蛇是否死亡（游戏是否结束）
        self.check_fail()

    def draw_elements(self):
        # 绘制草地
        self.draw_grass()

        # 产生食物
        self.food.draw_food()

        # 产生蛇蛇
        self.snake.draw_snake()

    # 检查蛇头与食物是否碰撞的函数
    def check_collision(self):
        if self.food.pos == self.snake.body[0]:
            # 让食物消失，并重新出现
            self.food.randomize()
            # 让蛇变长一节
            self.snake.add_block()
            # 得分 +1
            GameSet.score += 1

    # 检查蛇是否存活，来判断游戏是否结束函数
    def check_fail(self):
        # 判断蛇头是否还在屏幕内(将屏幕划分为单元格，判断是否在单元格当中)
        if not 0 <= self.snake.body[0].x < GameSet.cell_number or \
                not 0 <= self.snake.body[0].y < GameSet.cell_number:
            self.snake.live = False

        # 判断蛇头是否与身体的其他部分相碰撞
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.live = False

    # 绘制草地的函数
    def draw_grass(self):
        for row in range(GameSet.cell_number):
            if row % 2 == 0:
                for col in range(GameSet.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(2 * col * GameSet.cell_size,
                          2 * row * GameSet.cell_size, 2 * GameSet.cell_size, 2 * GameSet.cell_size)
                        pygame.draw.rect(GameSet.screen, color_deep_green, grass_rect)
            else:
                for col in range(GameSet.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(2 * col * GameSet.cell_size,
                          2 * row * GameSet.cell_size, 2 * GameSet.cell_size, 2 * GameSet.cell_size)
                        pygame.draw.rect(GameSet.screen, color_deep_green, grass_rect)

    # 结束游戏函数
    def game_over(self):
        pygame.quit()
        sys.exit()


# 蛇类
class Snake():
    def __init__(self):
        # 引入图像
        self.head_up = pygame.image.load(r'pic/snakeU.png')
        self.head_down = pygame.image.load(r'pic/snakeD.png')
        self.head_left = pygame.image.load(r'pic/snakeL.png')
        self.head_right = pygame.image.load(r'pic/snakeR.png')

        self.tail_up = pygame.image.load(r'pic/tail-U.png')
        self.tail_down = pygame.image.load(r'pic/tail-D.png')
        self.tail_left = pygame.image.load(r'pic/tail-L.png')
        self.tail_right = pygame.image.load(r'pic/tail-R.png')

        self.body_x = pygame.image.load(r'pic/body-X.png')
        self.body_y = pygame.image.load(r'pic/body-Y.png')

        self.turn_lt = pygame.image.load(r'pic/turn-left&top.png')
        self.turn_ld = pygame.image.load(r'pic/turn-left&down.png')
        self.turn_rt = pygame.image.load(r'pic/turn-right&top.png')
        self.turn_rd = pygame.image.load(r'pic/turn-right&down.png')

        # 建立蛇身
        self.body = [V2(5, 10), V2(4, 10), V2(3, 10)]

        # 蛇的方向
        self.direction = V2(0, 1)

        # 蛇头、身、尾的初始图标
        self.head = self.head_up
        self.tail = self.tail_down

        # 新增的蛇尾
        self.new_block = False

        # 蛇是否存活
        self.live = True

    # 生成蛇的函数
    def draw_snake(self):
        # 更改头部方向和尾部方向
        self.update_head()
        self.update_tail()

        # 遍历蛇的每一个身体躯干
        for index, block in enumerate(self.body):
            # 获得蛇的位置
            x_pos = int(block.x * GameSet.cell_size)
            y_pos = int(block.y * GameSet.cell_size)
            block_pos = pygame.Rect(x_pos, y_pos, GameSet.cell_size, GameSet.cell_size)

            # 蛇的朝向问题
            if index == 0:
                GameSet.screen.blit(self.head, block_pos)
            elif index == len(self.body) - 1:
                GameSet.screen.blit(self.tail, block_pos)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    GameSet.screen.blit(self.body_y, block_pos)
                elif previous_block.y == next_block.y:
                    GameSet.screen.blit(self.body_x, block_pos)
                else:
                    # 设置转角处的蛇身
                    if previous_block.x == -1 and next_block.y == -1 or \
                            previous_block.y == -1 and next_block.x == -1:
                        GameSet.screen.blit(self.turn_rd, block_pos)
                    if previous_block.x == 1 and next_block.y == -1 or \
                            previous_block.y == -1 and next_block.x == 1:
                        GameSet.screen.blit(self.turn_ld, block_pos)
                    if previous_block.x == -1 and next_block.y == 1 or \
                            previous_block.y == 1 and next_block.x == -1:
                        GameSet.screen.blit(self.turn_rt, block_pos)
                    if previous_block.x == 1 and next_block.y == 1 or \
                            previous_block.y == 1 and next_block.x == 1:
                        GameSet.screen.blit(self.turn_lt, block_pos)

    # 控制蛇移动的函数
    def move_snake(self):
        if self.new_block:
            # 相当于完整输入，不删除最后一块
            body_copy = self.body[:]
            # 将新的块插入
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            # 倒着取蛇躯干的每一块来完成移动
            body_copy = self.body[:-1]
            # 将最后一块去掉，刷新页面来看做移动
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    # 控制蛇尾部增长
    def add_block(self):
        self.new_block = True

    # 控制头部状态更新的函数
    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == V2(1, 0):
            self.head = self.head_left
        elif head_relation == V2(-1, 0):
            self.head = self.head_right
        elif head_relation == V2(0, 1):
            self.head = self.head_up
        elif head_relation == V2(0, -1):
            self.head = self.head_down

    # 控制尾部更新的函数
    def update_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == V2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == V2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == V2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == V2(0, -1):
            self.tail = self.tail_down


# 食物类
class Food():
    def __init__(self):
        self.randomize()

    # 展示食物
    def draw_food(self):
        food_rect = pygame.Rect(int(self.pos.x * GameSet.cell_size), int(self.pos.y * GameSet.cell_size),
                                GameSet.cell_size, GameSet.cell_size)
        # pygame.draw.rect(GameSet.screen, (255, 0, 0), food_rect)
        GameSet.screen.blit(GameSet.food, food_rect)

    # 重新生成食物
    def randomize(self):
        # 建立初始的x，y坐标
        # 在原有的单元格号上减1，保证食物生成位置不会出现在屏幕范围之外
        self.x = random.randint(0, GameSet.cell_number - 1)
        self.y = random.randint(0, GameSet.cell_number - 1)

        # 用Vectors来存储二维向量
        self.pos = V2(self.x, self.y)


if __name__ == '__main__':
    t = GameSet()
    t.start_game()

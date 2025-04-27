import pygame
import random

# 初始化pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("谷歌小恐龙游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 游戏变量
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 1
JUMP_HEIGHT = 15
GROUND_HEIGHT = SCREEN_HEIGHT - 50

# 恐龙类
class Dinosaur:
    def __init__(self):
        self.x = 50
        self.y = GROUND_HEIGHT
        self.width = 40
        self.height = 60
        self.vel_y = 0
        self.jump_count = 0
        self.max_jumps = 2
        self.is_jumping = False

    def jump(self):
        if self.jump_count < self.max_jumps:
            self.vel_y = -JUMP_HEIGHT
            self.jump_count += 1
            self.is_jumping = True

    def update(self):
        # 应用重力
        self.vel_y += GRAVITY
        self.y += self.vel_y

        # 确保恐龙不会掉出屏幕
        if self.y > GROUND_HEIGHT:
            self.y = GROUND_HEIGHT
            self.vel_y = 0
            self.jump_count = 0
            self.is_jumping = False

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

# 障碍物类
class Obstacle:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = GROUND_HEIGHT
        self.width = 30
        self.height = 40
        self.speed = 5

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x < -self.width

# 游戏主循环
def main():
    dinosaur = Dinosaur()
    obstacles = []
    obstacle_timer = 0
    score = 0
    font = pygame.font.SysFont(None, 36)
    game_over = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    dinosaur.jump()
                if event.key == pygame.K_r and game_over:
                    # 重置游戏
                    dinosaur = Dinosaur()
                    obstacles = []
                    obstacle_timer = 0
                    score = 0
                    game_over = False

        if not game_over:
            # 更新恐龙
            dinosaur.update()

            # 生成障碍物
            obstacle_timer += 1
            if obstacle_timer > random.randint(50, 150):
                obstacles.append(Obstacle())
                obstacle_timer = 0

            # 更新障碍物
            for obstacle in obstacles:
                obstacle.update()
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 1

                # 碰撞检测
                if (dinosaur.x < obstacle.x + obstacle.width and
                    dinosaur.x + dinosaur.width > obstacle.x and
                    dinosaur.y < obstacle.y + obstacle.height and
                    dinosaur.y + dinosaur.height > obstacle.y):
                    game_over = True

        # 绘制
        screen.fill(WHITE)
        dinosaur.draw()
        for obstacle in obstacles:
            obstacle.draw()

        # 显示分数
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press R to restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
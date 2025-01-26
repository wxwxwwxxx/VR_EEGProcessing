import pygame
import random
import threading
from neuracle_lib.triggerBox import TriggerBox

# 初始化 pygame
pygame.init()

# 定义屏幕尺寸
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("箭头显示与间隔倒计时")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 设置字体
font = pygame.font.Font(None, 74)


# 加载箭头图像或绘制箭头
def draw_arrow(screen, direction):
    if direction == 1:
        # 绘制左箭头
        pygame.draw.polygon(screen, BLACK, [(400, 300), (500, 250), (500, 350)])
    elif direction == 2:
        # 绘制右箭头
        pygame.draw.polygon(screen, BLACK, [(400, 300), (300, 250), (300, 350)])


# 显示箭头和倒计时的函数
def show_arrow_with_timer(direction, duration=3):
    for i in range(duration, 0, -1):  # 从 duration 开始倒计时到 1
        screen.fill(WHITE)  # 填充背景
        draw_arrow(screen, direction)  # 绘制箭头

        # 显示倒计时
        timer_text = font.render(str(i), True, RED)
        text_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(timer_text, text_rect)

        pygame.display.flip()  # 更新显示
        pygame.time.wait(1000)  # 等待 1 秒，替代 time.sleep


# 显示间隔时间倒计时
def show_interval_timer(interval=5):
    for i in range(interval, 0, -1):  # 从 interval 开始倒计时到 1
        screen.fill(WHITE)  # 填充背景

        # 显示间隔倒计时
        interval_text = font.render(f"Next arrow in: {i}s", True, BLUE)
        text_rect = interval_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(interval_text, text_rect)

        pygame.display.flip()  # 更新显示
        pygame.time.wait(1000)  # 等待 1 秒，替代 time.sleep


# 用后台线程运行倒计时和箭头显示
def run_program():
    arrow_directions = [1,2]  # 箭头方向
    num_arrows = 200 # 箭头总数
    triggerbox = TriggerBox("COM3")
    for _ in range(num_arrows):
        # 随机选择箭头方向
        direction = random.choice(arrow_directions)
        show_interval_timer(interval=5)  # 显示间隔倒计时
        triggerbox.output_event_data(direction)
        show_arrow_with_timer(direction, duration=4)  # 显示箭头和倒计时



# 主函数
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 启动后台线程
        if not threading.active_count() > 1:
            thread = threading.Thread(target=run_program)
            thread.start()

        # 在主线程中继续处理 pygame 事件
        pygame.display.update()  # 强制更新屏幕

    pygame.quit()


if __name__ == "__main__":
    main()

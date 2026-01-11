# app/display_month_graph.py
import json
import pygame
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DATA_PATH = Path(__file__).parent.parent / "data" / "data.json"

SCREEN_SIZE = (800, 480)
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
BAR_COLOR = (0, 200, 255)

last_reload_date = None


def load_monthly_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    now = datetime.now()
    daily_sum = defaultdict(int)

    for item in data:
        dt = datetime.strptime(item["送信時間"], "%Y-%m-%d %H:%M:%S")
        key = dt.strftime("%m/%d")
        daily_sum[key] += item["money_info"]

    return dict(sorted(daily_sum.items()))


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Monthly Usage Graph")

    font_title = pygame.font.SysFont(None, 40)
    font_label = pygame.font.SysFont(None, 20)

    data = load_monthly_data()
    total = sum(data.values())

    max_value = max(data.values()) if data else 1
    bar_width = 40
    margin = 60
    graph_height = 250

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        now = datetime.now()
        if now.hour == 12 and now.minute == 0:
            today = now.date()
            if last_reload_date != today:
                last_reload_date = today
                data = load_monthly_data()
                total = sum(data.values())
                max_value = max(data.values()) if data else 1

        # タイトル & 合計
        title = font_title.render(f"今月の利用合計 ¥{total:,}", True, TEXT_COLOR)
        screen.blit(title, (20, 20))

        # グラフ描画
        x = margin
        y_base = 350

        for day, amount in data.items():
            bar_height = int((amount / max_value) * graph_height)
            rect = pygame.Rect(x, y_base - bar_height, bar_width, bar_height)
            pygame.draw.rect(screen, BAR_COLOR, rect)

            # 金額表示
            value_text = font_label.render(f"{amount}", True, TEXT_COLOR)
            screen.blit(value_text, (x, y_base - bar_height - 20))

            # 日付表示
            label = font_label.render(day, True, TEXT_COLOR)
            screen.blit(label, (x, y_base + 5))

            x += bar_width + 15

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

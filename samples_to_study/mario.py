# 이 예제에서는 마리오와 버섯을 이미지로 불러온 후, 각각의 좌표를 지정하여 화면에 그립니다. 마리오는 키보드 입력을 통해 좌우로 이동할 수 있고, 버섯은 좌우로 이동하면서 충돌 검사를 통해 마리오와 충돌하면 다시 화면 오른쪽 끝으로 이동합니다. 이 예제는 간단한 플랫폼 게임의 기본 구조를 보여줍니다.

import pygame

# 게임 환경 설정
pygame.init()
WIDTH, HEIGHT = 640, 480
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Mario Game")

# 색상 설정
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 이미지 로드
mario_img = pygame.image.load("mario.png").convert_alpha()
mushroom_img = pygame.image.load("mushroom.png").convert_alpha()

# 게임 변수 초기화
mario_x = 0
mario_y = HEIGHT - mario_img.get_height()
mushroom_x = WIDTH - mushroom_img.get_width()
mushroom_y = HEIGHT - mushroom_img.get_height()
mushroom_direction = "left"

# 게임 루프
while True:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # 마리오 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        mario_x -= 5
    elif keys[pygame.K_RIGHT]:
        mario_x += 5

    # 버섯 이동
    if mushroom_direction == "left":
        mushroom_x -= 3
        if mushroom_x < 0:
            mushroom_direction = "right"
    else:
        mushroom_x += 3
        if mushroom_x > WIDTH - mushroom_img.get_width():
            mushroom_direction = "left"

    # 충돌 검사
    mario_rect = pygame.Rect(mario_x, mario_y, mario_img.get_width(), mario_img.get_height())
    mushroom_rect = pygame.Rect(mushroom_x, mushroom_y, mushroom_img.get_width(), mushroom_img.get_height())
    if mario_rect.colliderect(mushroom_rect):
        mushroom_x = WIDTH - mushroom_img.get_width()
        mushroom_y = HEIGHT - mushroom_img.get_height()

    # 그리기
    SCREEN.fill(BLACK)
    SCREEN.blit(mario_img, (mario_x, mario_y))
    SCREEN.blit(mushroom_img, (mushroom_x, mushroom_y))
    pygame.display.flip()

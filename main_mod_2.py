# 기본 라이브러리 임포트
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import numpy as np
import cv2
import pybullet


# 직접 정의한 모듈 임포트
import config.settings
from env.env import PickPlaceEnv
from env.constants import ALL_BLOCKS, ALL_BOWLS
from lmp.setup import setup_LMP
from config.lmp_config import cfg_tabletop


# 초기 설정
_ = config.settings

# 초기 선택
num_blocks = 3 #@param {type:"slider", min:0, max:4, step:1}
num_bowls = 3 #@param {type:"slider", min:0, max:4, step:1}
high_resolution = True #@param {type:"boolean"}
high_frame_rate = True #@param {type:"boolean"}


# 시뮬레이션 환경 준비
env = PickPlaceEnv(render=True, high_res=high_resolution, high_frame_rate=high_frame_rate)
# 물체 리스트
block_list = np.random.choice(ALL_BLOCKS, size=num_blocks, replace=False).tolist()
bowl_list = np.random.choice(ALL_BOWLS, size=num_bowls, replace=False).tolist()
obj_list = block_list + bowl_list
_ = env.reset(obj_list)
# LMP
lmp_tabletop_ui = setup_LMP(env, cfg_tabletop)


print('available objects:')
print(obj_list)

print('Write \'close\' to terminate the program')

while True:
  # 현재 상태에 대한 이미지 저장
  image = env.get_camera_image()
  image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  cv2.imwrite("env_view.png", image_rgb)

  # 자연어 명령 입력
  user_input = input() #@param {allow-input: true, type:"string"}
  if user_input.strip()=='close': # 종료 조건
    pybullet.disconnect()
    break

  env.cache_video = [] # 이후 실행될 로봇 동작 프레임을 여기에 하나씩 저장
  print('Running policy and recording video...')
  lmp_tabletop_ui(user_input, f'objects = {env.object_list}') # 자연어 명령 처리 부분

  if env.cache_video: # 프레임이 제대로 저장되었다면
    rendered_clip = ImageSequenceClip(env.cache_video, fps=35 if high_frame_rate else 25) # 영상 클립으로 변환
    rendered_clip.write_videofile('Demo.mp4') # 영상 파일로 저장
  print('Waiting for the next command...')
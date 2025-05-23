# setup_LMP 함수


# 기본 임포트
import copy
import shapely
import numpy as np
from shapely.geometry import *
from shapely.affinity import *

# 직접 정의한 모듈 임포트
from lmp.wrapper import LMP_wrapper
from config.lmp_config import lmp_tabletop_coords
from lmp.lmp_base import LMP, LMPFGen


def setup_LMP(env, cfg_tabletop): # 각각 PickPlaceEnv 인스턴스와 LMP 설정 딕셔너리
  # LMP env wrapper
  cfg_tabletop = copy.deepcopy(cfg_tabletop) # cfg_tabletop은 함수 내부에서 수정되므로, 원본 설정값을 보존하기 위해 깊은 복사 수행
  cfg_tabletop['env'] = dict() # cfg_tabletop 딕셔너리에 env라는 키 추가, 빈 딕셔너리로 초기화
  cfg_tabletop['env']['init_objs'] = list(env.obj_name_to_id.keys()) # 초기 물체 목록 저장 # 현재 환경에 배치된 물체 이름 -> pybullet object ID 매핑 # keys()로 이름 목록 추출
  cfg_tabletop['env']['coords'] = lmp_tabletop_coords # LMP가 객체 위치 등을 해석할 때 사용할 좌표계 정보
  LMP_env = LMP_wrapper(env, cfg_tabletop) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  
  # creating APIs that the LMPs can interact with
  # LMP 내부에서 사용될 고정 변수들 저장하는 딕셔너리
  fixed_vars = {
      'np': np
  }
  fixed_vars.update({
      name: eval(name)
      for name in shapely.geometry.__all__ + shapely.affinity.__all__
  })
  variable_vars = { # LMP_env가 제공하는 다양한 메서드를 variable_vars라는 딕셔너리에 저장 # 이 변수들은 런타임 시점에서 LMP 코드에 주입될 수 있는 동적 기능
      k: getattr(LMP_env, k)
      for k in [
          'get_bbox', 'get_obj_pos', 'get_color', 'is_obj_visible', 'denormalize_xy',
          'put_first_on_second', 'get_obj_names',
          'get_corner_name', 'get_side_name',
      ]
  }
  variable_vars['say'] = lambda msg: print(f'robot says: {msg}') # say라는 함수명을 통해 LMP 내부에서 robot says: 형식의 출력 메시지를 생성할 수 있게 람다 함수 등록

  # creating the function-generating LMP
  # LMPFGen 클래스는 LMP가 실행할 파이썬 함수를 문자열로부터 생성
  lmp_fgen = LMPFGen(cfg_tabletop['lmps']['fgen'], fixed_vars, variable_vars) # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  # creating other low-level LMPs
  variable_vars.update({
      k: LMP(k, cfg_tabletop['lmps'][k], lmp_fgen, fixed_vars, variable_vars)
      for k in ['parse_obj_name', 'parse_position', 'parse_question', 'transform_shape_pts']
  })

  # creating the LMP that deals w/ high-level language commands
  # 최상위 LMP 생성
  # 실제 사용자의 자연어 명령어를 해석하고, 적절한 하위 LMP들을 호출하여 동작을 수행
  lmp_tabletop_ui = LMP(
      'tabletop_ui', cfg_tabletop['lmps']['tabletop_ui'], lmp_fgen, fixed_vars, variable_vars
  )

  return lmp_tabletop_ui
# cfg_tabletop, lmp_tabletop_coords 변수(?)


# 직접 정의한 모듈 불러오기
from config.prompts import *
from config.settings import model_name


cfg_tabletop = {
  'lmps': {
    'tabletop_ui': {
      'prompt_text': prompt_tabletop_ui,
      'engine': model_name,
      'max_tokens': 512,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#', 'objects = ['],
      'maintain_session': True,
      'debug_mode': False,
      'include_context': True,
      'has_return': False,
      'return_val_name': 'ret_val',
    },
    'parse_obj_name': {
      'prompt_text': prompt_parse_obj_name,
      'engine': model_name,
      'max_tokens': 512,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#', 'objects = ['],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'ret_val',
    },
    'parse_position': {
      'prompt_text': prompt_parse_position,
      'engine': model_name,
      'max_tokens': 512,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#'],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'ret_val',
    },
    'parse_question': {
      'prompt_text': prompt_parse_question,
      'engine': model_name,
      'max_tokens': 512,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#', 'objects = ['],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'ret_val',
    },
    'transform_shape_pts': {
      'prompt_text': prompt_transform_shape_pts,
      'engine': model_name,
      'max_tokens': 512,
      'temperature': 0,
      'query_prefix': '# ',
      'query_suffix': '.',
      'stop': ['#'],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
      'has_return': True,
      'return_val_name': 'new_shape_pts',
    },
    'fgen': {
      'prompt_text': prompt_fgen,
      'engine': model_name,
      'max_tokens': 512,
      'temperature': 0,
      'query_prefix': '# define function: ',
      'query_suffix': '.',
      'stop': ['# define', '# example'],
      'maintain_session': False,
      'debug_mode': False,
      'include_context': True,
    }
  }
}

lmp_tabletop_coords = {
        'top_left':     (-0.3 + 0.05, -0.2 - 0.05),
        'top_side':     (0,           -0.2 - 0.05),
        'top_right':    (0.3 - 0.05,  -0.2 - 0.05),
        'left_side':    (-0.3 + 0.05, -0.5,      ),
        'middle':       (0,           -0.5,      ),
        'right_side':   (0.3 - 0.05,  -0.5,      ),
        'bottom_left':  (-0.3 + 0.05, -0.8 + 0.05),
        'bottom_side':  (0,           -0.8 + 0.05),
        'bottom_right': (0.3 - 0.05,  -0.8 + 0.05),
        'table_z':       0.0,
      }
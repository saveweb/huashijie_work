import os
import secrets

import requests

from huashijie.util.device import XIAOMI_MODELS
from huashijie.util.unique_str import uniquestr

ss = requests.session()

workid = 200200
status_s = {}
while workid and os.path.exists('run'):
  r = ss.get(
    'http://app.huashijie.art/api/work/detailV2',
    params={
      'visitorId': '-1', # 当前用户 id，访客是 -1
      'workId': workid, # 作品 id, 如： 200202585
      'cur_user_id': '-1', # 当前用户 id，访客 -1
      'platform': 'android',
      'os_version': secrets.choice([i for i in range(23, 34)]),
      'version_code': '224',
      'device_brand': 'Xiaomi',
      'device_model': secrets.choice(XIAOMI_MODELS),
      'token': '', # 访客传 "" 空字符串即可
      'channel': 'main', # main 是画世界。还有熊猫绘画
    },
    headers={
      uniquestr('Referer'): '*.painterclub.cn',
      uniquestr('Referer'): '*.pandapaint.net',
      uniquestr('Referer'): '*.huashijie.art',
      'Connection': 'Keep-Alive',
      'Accept-Encoding': 'gzip',
      'User-Agent': 'okhttp/3.12.0',
    },
  )
  r.raise_for_status()
  r_json = r.json()
  if str(r_json['msg']) not in status_s:
    print(r_json)
    status_s[str(r_json['msg'])] = r_json
  workid = secrets.randbelow(200200)
  print(workid, '--->', len(status_s))

print('===========')
print(status_s)
# status 1: 正常
# {"status":43,"msg":"作品不存在"}
# {"status":43,"msg":"非法作品id"}
# {'status': 43, 'msg': '暂无查看该作品的权限'}
# {"status":72,"msg":"作品已删除"}
# {'status': 72, 'msg': '由于作者隐私设置，您没有权限查看此作品'}
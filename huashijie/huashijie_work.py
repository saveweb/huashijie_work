from datetime import datetime
import os
import secrets
import sys
import time
import traceback

import requests
from requests.adapters import HTTPAdapter

from huashijie.util.archivist import get_archivist, new_archivist
from huashijie.util.device import XIAOMI_MODELS
from huashijie.util.task import Status, Task
from huashijie.util.tracker import Tracker
from huashijie.util.unique_str import uniquestr

VERSION = "1.0"

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=3))
session.mount("http://", HTTPAdapter(max_retries=3))

def get_work_detail_r(work_id: int):
    r = session.get('http://app.huashijie.art/api/work/detailV2',
        params={
            'visitorId': '-1', # 当前用户 id，访客是 -1
            'workId': work_id, # 作品 id, 200202585
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
    return r

def process(tracker: Tracker, TASK: Task):
    
    r = get_work_detail_r(TASK.id)
    r.raise_for_status()
    r_json = r.json()

    TO_INSERT = False

# status 1: 正常
# {"status":43,"msg":"作品不存在"}
# {"status":43,"msg":"非法作品id"}
# {'status': 43, 'msg': '暂无查看该作品的权限'}
# {"status":72,"msg":"作品已删除"}
# {'status': 72, 'msg': '由于作者隐私设置，您没有权限查看此作品'}

    if 'status' in r_json:
        status = r_json['status']
        if status == 1:
            # OK
            TO_INSERT = True
            item_status = 1
            payload = r_json
        elif status in (43, 72):
            print(r_json)
            TO_INSERT = True
            item_status = status
            payload = r_json
        else:
            raise Exception("Unknown status: " + r.text)
    else:
        raise Exception("Unknown response: " + r.text)

    if TO_INSERT:
        tracker.insert_item(item_id=TASK.id, item_status=item_status, payload=payload)
        tracker.update_task(task_id=TASK.id, status=Status.DONE)
    else:
        raise NotImplementedError(r.text)

def main():
    print("zh: 为避免您的节点被 ban，请不要使用相同 IP 多开同一个项目！")
    print("en: To avoid being banned, please do not run concurrently on the same project with the same IP!")

    archivist = get_archivist() or new_archivist()

    time.sleep(1) # avoid infinite restart consume too much CPU
    tracker = Tracker(project_id="huashijie_work", client_version=VERSION, archivist=archivist, session=session)

    while True:
        if tracker.project.status.paused:
            print("[tracker->client] Project paused, sleep 120s")
            time.sleep(120)
            continue
        if os.path.exists("stop"):
            print("[STOP] stop file exists, exit")
            return

        TASK_raw = tracker.claim_task()
        if TASK_raw is None:
            notask_sleep = tracker.project.client.claim_task_delay * 3
            print(f"No tasks available, sleep {notask_sleep:.2f}s")
            time.sleep(notask_sleep)
            continue

        TASK = Task(**TASK_raw)
        
        start = time.time()
        try:
            print('===', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), TASK, '===')
            process(tracker=tracker, TASK=TASK)
        except Exception as e:
            print(f"Task {TASK} failed: {e}")
            traceback.print_exc()

            # 抛的异常都会把任务设成 FAIL
            tracker.update_task(task_id=TASK.id, status=Status.FAIL)

            if isinstance(e, requests.exceptions.HTTPError):
                if e.response.status_code == 403:
                    print("403")
                    sys.exit(1)

        print(f"Task {TASK.id} done in {time.time() - start:.2f}s")

if __name__ == "__main__":
    main()

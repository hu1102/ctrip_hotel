import math
import requests
import json
import time
import random


MY_COOKIES = """"""

FX_TOKEN = "09031148113011295299"
TRACE_ID = "09031148113011295299-1764315176256-8334839"


def get_hotel_comments(hotel_id, page_index=1, tag_list=None):

    url = "https://m.ctrip.com/restapi/soa2/34308/getHotelCommentInfo"
    params = {
        "_fxpcqlniredt": FX_TOKEN,
        "x-traceID": TRACE_ID
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://m.ctrip.com",
        "Referer": f"https://m.ctrip.com/webapp/hotel/j/hoteldetail/dianping/{hotel_id}.html",
        "Cookie": MY_COOKIES
    }
    if tag_list is None:
        tag_list = ["1"]  # 默认为"1"，通常代表"全部"
    # 构造动态 Payload
    payload = {
        "hotelId": hotel_id,
        "sceneTypes": ["CommentList"],
        "commentFilterOptions": {
            "pageIndex": page_index,
            "pageSize": 10,
            "keyWord": "",
            "commonStatisticList": tag_list,  # 筛选标签
            "orderBy": "1",
            "rooms": [],  # 可以根据房间号筛选评论
            "travelTypes": [],  # 可以根据出游类型筛选评论
            "filterDateTypeList": [],  # 筛选入住月份
            "repeatComment": 1
        },
        "head": {
            "cid": "09031148113011295299",
            "ctok": "", "cver": "1.0", "lang": "01", "sid": "8888", "syscode": "09", "auth": "", "xsid": "",
            "extension": [{"name": "sotpLocale", "value": "zh-CN"}, {"name": "sotpRegion", "value": "CN"},
                          {"name": "sotpGroup", "value": "ctrip"}, {"name": "sotpBu", "value": "hbu"},
                          {"name": "locale", "value": "zh-CN"}, {"name": "pageId", "value": "228032"},
                          {"name": "htl-bu", "value": "HBU"}, {"name": "htl-timeZone", "value": "8"}],
            "platform": "H5", "group": "ctrip", "bu": "HBU", "locale": "zh-CN", "region": "CN", "currency": "CNY",
            "appId": "100054203", "timeZone": "8", "pageId": "228032", "isEnforceSyscode": True, "isSSR": False
        }
    }

    try:
        response = requests.post(url, params=params, headers=headers, json=payload, timeout=10)
        if response.status_code != 200:
            return [], 0

        data = response.json()
        if data.get('ResponseStatus', {}).get('Ack') != 'Success':
            return [], 0

        # 解析数据
        group_list = data["data"].get('groupList', [])
        extracted_comments = []
        total_count = data["data"].get('totalCount', 0)  # 初始化总数
        for group in group_list:
            # 找到包含评论列表的那个 group
            if 'commentList' in group:
                raw_comments = group['commentList']

                for item in raw_comments:
                    user_info = item.get('userInfo', {})

                    images = []
                    # 优先检查 imageCollagesList，因为它包含高清大图的完整 URL
                    if 'imageList' in item and item['imageCuttingsList']:
                        for img_obj in item['imageCuttingsList']:
                            # 优先获取 bigImageUrl (大图)，如果没有则获取 mediumImageUrl
                            img_url = img_obj.get('bigImageUrl') or img_obj.get('mediumImageUrl')
                            if img_url:
                                images.append(img_url)
                    videos = []
                    if 'videoList' in item and item['videoList']:
                        for vid_obj in item['videoList']:
                            video_info = {
                                "url": vid_obj.get('url'),  # 视频播放地址
                                "cover": vid_obj.get('cover'),  # 视频封面图
                                "duration": vid_obj.get('duration')  # 视频时长
                            }
                            if video_info['url']:
                                videos.append(video_info)
                    comment_obj = {
                        "id": item.get('id'),
                        "content": item.get('content', ''),
                        "score": item.get('ratingInfo', {}),
                        "user_nick": user_info.get('nickName', '匿名用户'),
                        "createDate": item.get('createDate', ''),
                        "check_in": item.get('checkinDate', ''),
                        "room_name": item.get('roomName', ''),
                        "room_id": item.get('roomID', ''),
                        "images": images,
                        "videos": videos,
                    }

                    extracted_comments.append(comment_obj)

        return extracted_comments, total_count

    except Exception as e:
        print(f"Error: {e}")
        return [], 0


def run_spider(hotel_id, start_page=1, end_page=0, tag_list=['1'], save_path=None):
    all_data = []
    current_page = start_page
    target_end_page = end_page if end_page > 0 else float('inf')

    while current_page <= target_end_page:
        print(f"正在爬取第 {current_page} 页...", end="")

        comments, total_count = get_hotel_comments(hotel_id, page_index=current_page, tag_list=tag_list)
        # === 1. 空数据保护 ===
        if not comments:
            print("接口无数据或已爬完，提前结束。")
            break
        # 只有在爬第一页（相对于start_page）且成功获取到total_count时才计算
        if current_page == start_page:
            if total_count > 0:
                # 计算实际总页数
                total_pages = math.ceil(total_count / 10)
                # 核心逻辑修正：
                if end_page == 0:
                    target_end_page = total_pages
                else:
                    # 防止用户输入 end_page=100 但实际只有 50 页的情况
                    target_end_page = min(end_page, total_pages)
            else:
                print("未获取到总数，将尝试逐页爬取直到无数据")

        # === 3. 存储数据 ===
        all_data.extend(comments)
        print(f"本页 {len(comments)} 条 | 累计 {len(all_data)} 条")

        # === 4. 循环结束检查 ===
        # 虽然 while 条件也会检查，但在这里检查可以避免不必要的 sleep
        if current_page >= target_end_page:
            print("已达到目标结束页，停止爬取。")
            break

        # === 5. 页码递增与延时 ===
        current_page += 1
        time.sleep(random.uniform(1, 3))

    # === 6. 保存结果 ===
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"\n爬取结束！共 {len(all_data)} 条数据，已保存至 {save_path}")
    except Exception as e:
        print(f" 保存出错: {e}")


# ==========================================
#                  如何调用
# ==========================================

if __name__ == "__main__":
    hotel_id = 131826949
    all_data = []

    # === 使用场景 1: 爬取【所有】评论 (筛选：全部) ===
    # run_spider(hotel_id, start_page=1, end_page=0, tag_list=["1"])

    # === 使用场景 2: 爬取【指定页数】 (例如第 2 到第 3 页) ===
    run_spider(hotel_id, start_page=1, end_page=3, tag_list=["1"], save_path=f"output/comments_{hotel_id}.json")
    # === 使用场景 3: 爬取【所有差评】 (需要先确定差评 tag 是多少，假设是 "5") ===
    # run_spider(hotel_id, start_page=1, end_page=0, tag_list=["5"])
    # === 使用场景 4: 爬取【所有带图评论】 (假设 tag 是 "3") ===
    # run_spider(hotel_id, start_page=1, end_page=0, tag_list=["3"])


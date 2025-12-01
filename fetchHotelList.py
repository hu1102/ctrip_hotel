import math
import requests
from datetime import datetime, timedelta
import json


MY_COOKIES = """"""


def search_hotels(city_id, check_in, check_out, keyword, filters, pageIndex, proxy_url=""):
    url = "https://m.ctrip.com/restapi/soa2/34951/fetchHotelList"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://hotels.ctrip.com",
        "Referer": "https://hotels.ctrip.com/",
        'accept': '*/*',
        'Cookie': MY_COOKIES,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    if not check_in or not check_out:
        today = datetime.now() + timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        check_in_str = today.strftime("%Y%m%d")
        check_out_str = tomorrow.strftime("%Y%m%d")
    else:
        check_in_str = check_in.replace("-", "")
        check_out_str = check_out.replace("-", "")
    # 构造 Payload
    payload = {
        "date": {
            "dateType": 1,
            "dateInfo": {
                "checkInDate": check_in_str,
                "checkOutDate": check_out_str
            }
        },
        "destination": {
            "type": 1,
            "geo": {
                "cityId": city_id,
                "countryId": 1
            },
            "keyword": {
                "word": keyword
            }
        },
        "filters": filters if filters else [],
        "paging": {
            "pageIndex": pageIndex,
            "pageSize": 10,
            "pageCode": "10650171192"
        },
        "head": {
            "platform": "PC",
            "cver": "0",
            "bu": "HBU",
            "group": "ctrip",
            "locale": "zh-CN",
            "timezone": "8",
            "currency": "CNY",
            "pageId": "10650171192",
            "guid": "",
            "isSSR": False
        }
    }

    current_filters = filters if filters else []

    # 检查传入的filters中是否包含行政区筛选 (type: 9) 或其他精确筛选
    is_specific_filter_search = any(f.get("type") == "9" for f in current_filters)

    if is_specific_filter_search:
        # 这是行政区或类似精确筛选，destination.type应为1
        payload["destination"] = {
            "type": 1,
            "geo": {"cityId": city_id, "countryId": 1},
            "keyword": {"word": keyword}  # 即使是精确筛选，destination.keyword也存在
        }
        # filter已经在current_filters里了，无需额外操作

    elif keyword:
        # 这是一个普通的关键字搜索，destination.type应为3
        payload["destination"] = {
            "type": 3,
            "geo": {"cityId": city_id, "countryId": 1},
            "keyword": {"word": keyword}
        }
        # 添加type: 30的filter
        current_filters.append({
            "type": "30",
            "value": keyword,
            "filterId": f"30|{keyword}"
        })

    else:
        # 无筛选、无关键字的基础城市搜索
        payload["destination"] = {
            "type": 1,
            "geo": {"cityId": city_id, "countryId": 1}
        }

    payload["filters"] = current_filters

    proxies = {}
    if proxy_url:
        proxies = {"http": proxy_url, "https": proxy_url}

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            proxies=proxies,
            timeout=30
        )
        response.raise_for_status()
    except Exception as e:
        print(f"请求失败: {e}")
        return [], 0
    response_data = response.json()
    if "data" not in response_data or "hotelList" not in response_data["data"]:
        return [], 0

    hotel_list = response_data["data"]["hotelList"]

    # --- 获取总数 ---
    addition_info = response_data["data"].get("hotelListAddtionInfo", {})
    total_count = addition_info.get("hotelTotalCount", 0)

    hotels_formatted = []
    for item in hotel_list:
        hotel_info = item["hotelInfo"]
        room_info = item.get("roomInfo", [])

        # 安全提取价格
        price = "暂无"
        if room_info:
            p_info = room_info[0].get("priceInfo", {})
            price = f"{p_info.get('displayPrice', '')}{p_info.get('afterPriceText', '')}"

        imgs = hotel_info.get("hotelImages", {}).get("multiImgs", [])
        imgurls = [img["url"] for img in imgs]

        hotel_item = {
            "hotelId": int(hotel_info["summary"]["hotelId"]),
            "name": hotel_info.get("nameInfo", {})["name"],
            "star": hotel_info.get("hotelStar", {})["star"],
            "address": hotel_info.get("positionInfo", {}).get("address"),
            "price": price,
            "score": hotel_info.get("commentInfo", {}).get("commentScore", 0),
            "image": imgurls,
            "detail_url": f"https://hotels.ctrip.com/hotels/detail/?hotelId={hotel_info['summary']['hotelId']}"
        }
        hotels_formatted.append(hotel_item)

        # 返回 (数据列表, 总数)
    return hotels_formatted, total_count


def fetchHotels(city_id, check_in, check_out, keyword="", filters=None, numPages=0, savePath="hotelLists.json"):
    allHotels = []
    # --- 1. 爬取第1页 ---
    page1_hotels, total_count = search_hotels(city_id, check_in, check_out, keyword, filters, pageIndex=1)
    if not page1_hotels:
        print("第 1 页未获取到数据，任务停止。")
        return []

    allHotels.extend(page1_hotels)
    with open(savePath, "w", encoding="utf-8") as f:
        json.dump(allHotels, f, ensure_ascii=False, indent=4)
    # --- 2. 计算总页数 ---
    real_total_pages = math.ceil(total_count / 10)
    # print(f"API返回总数: {total_count} 条，共计 {real_total_pages} 页。")

    # --- 3. 确定最终要爬的页数 ---
    if numPages == 0:
        final_pages = real_total_pages
    else:
        final_pages = min(numPages, real_total_pages)
    # --- 4. 循环爬取剩余页面 (单线程安全模式) ---
    if final_pages > 1:
        for page_idx in range(2, final_pages + 1):

            hotels, _ = search_hotels(
                city_id, check_in, check_out, keyword, filters, pageIndex=page_idx
            )

            if hotels:
                allHotels.extend(hotels)
                # print(f"第 {page_idx} 页成功，获取 {len(hotels)} 条。")
                # 实时保存 (每爬一页存一次，防止中断丢失)
                try:
                    with open(savePath, "w", encoding="utf-8") as f:
                        json.dump(allHotels, f, ensure_ascii=False, indent=4)
                except Exception as e:
                    print(f"保存文件出错: {e}")
            else:
                print(f"第 {page_idx} 页无数据，可能是翻页结束或触发风控，提前退出。")
                break

    print(f"任务完成！共获取 {len(allHotels)} 家酒店。")
    # === 去重逻辑 (根据 hotelId) ===
    unique_hotels = {}
    for hotel in allHotels:
        h_id = hotel['hotelId']
        # 将 hotelId 作为 key，数据作为 value
        # 只有当 ID 不在字典里时才添加，这样就保留了第一次出现的数据
        if h_id not in unique_hotels:
            unique_hotels[h_id] = hotel

    clean_list = list(unique_hotels.values())

    print(f"去重后数量: {len(clean_list)} 条")
    print(f"剔除了 {len(allHotels) - len(clean_list)} 条重复/冗余数据\n")

    # 保存去重后的最终文件
    with open((savePath.replace(".json", "")+"_cleaned.json"), "w", encoding="utf-8") as f:
        json.dump(clean_list, f, ensure_ascii=False, indent=4)
    return allHotels


if __name__ == "__main__":
    city_id = 477  # 武汉
    check_in = "2025-12-05"
    check_out = "2025-12-07"
    print(f"正在搜索城市ID: {city_id}, 日期: {check_in} - {check_out}")
    keyword = "武汉理工大学南湖校区"
    # 构造筛选条件
    my_filters = []

    # # 行政区筛选和keyword筛选只能二选一，其他可以共存
    # my_filters.append({
    #     "filterId": "9|431",
    #     "type": "9",
    #     "value": "431",
    #     "title": "行政区筛选"
    # })
    # keyword 筛选
    my_filters.append({
        "filterId": f"30|{keyword}",
        "type": "30",
        "value": keyword,
        "title": "keyword筛选"
    })

    hotelLists = fetchHotels(
        city_id=city_id,
        check_in=check_in,
        check_out=check_out,
        keyword=keyword,  # 使用filters时，keyword留空
        filters=my_filters,
        numPages=3,       # numPages=0 时爬取全部
        savePath="output/hotelLists.json"
    )


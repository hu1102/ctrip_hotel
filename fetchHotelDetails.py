import requests
import json

MY_COOKIES = """"""


def fetchInfo(hotelId, checkIn, checkOut, save_path):
    cookies = {
        'Hm_lvt_a8d6737197d542432f4ff4abc6e06384': '1757074904',
        'HMACCOUNT': '6F86E0C9E2731DC9',
        'UBT_VID': '1757074904851.1d98GRGifqwz',
        '_ga': 'GA1.1.592361527.1757074905',
        'GUID': '09031125113956821417',
        'Session': 'smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=',
        'Union': 'AllianceID=4899&SID=135371&OUID=&createtime=1757074906&Expires=1757679705667',
        'MKT_CKID': '1757074905690.srr46.htfv',
        '_RSG': '9dKReSfFTz6tU0Gh1GgkE8',
        '_RDG': '28001d8b42dca823ec13d249b772a7c990',
        '_RGUID': '6f5d3e97-286d-49c9-83ae-a9006b4007b7',
        'MKT_Pagesource': 'PC',
        'manualclose': '1',
        'ibulanguage': 'CN',
        'ibulocale': 'zh_cn',
        'cookiePricesDisplayed': 'CNY',
        'librauuid': '',
        'nfes_isSupportWebP': '1',
        'Hm_lpvt_a8d6737197d542432f4ff4abc6e06384': '1757075254',
        '_ga_5DVRDQD429': 'GS2.1.s1757074904$o1$g1$t1757075262$j52$l0$h0',
        '_ga_B77BES1Z8Z': 'GS2.1.s1757074904$o1$g1$t1757075262$j52$l0$h0',
        '_ga_9BZF483VNQ': 'GS2.1.s1757074904$o1$g1$t1757075262$j52$l0$h0',
        '_ubtstatus': '%7B%22vid%22%3A%221757074904851.1d98GRGifqwz%22%2C%22sid%22%3A1%2C%22pvid%22%3A12%2C%22pid%22%3A600001375%7D',
        '_bfaStatusPVSend': '1',
        '_bfi': 'p1%3D600001375%26p2%3D102001%26v1%3D12%26v2%3D11',
        '_bfaStatus': 'success',
        'intl_ht1': 'h4=30_67690986,2_8063900,30_535673,30_105849420,30_347431',
        '_jzqco': '%7C%7C%7C%7C1757074905860%7C1.1290556627.1757074905688.1757081292854.1757081998459.1757081292854.1757081998459.0.0.0.16.16',
        '_RF1': '82.26.72.152',
        '_bfa': '1.1757074904851.1d98GRGifqwz.1.1757081997983.1757083547323.1.18.102003',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://hotels.ctrip.com',
        'p': '37856503287',
        'priority': 'u=1, i',
        'referer': 'https://hotels.ctrip.com/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        # 'cookie': 'Hm_lvt_a8d6737197d542432f4ff4abc6e06384=1757074904; HMACCOUNT=6F86E0C9E2731DC9; UBT_VID=1757074904851.1d98GRGifqwz; _ga=GA1.1.592361527.1757074905; GUID=09031125113956821417; Session=smartlinkcode=U135371&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4899&SID=135371&OUID=&createtime=1757074906&Expires=1757679705667; MKT_CKID=1757074905690.srr46.htfv; _RSG=9dKReSfFTz6tU0Gh1GgkE8; _RDG=28001d8b42dca823ec13d249b772a7c990; _RGUID=6f5d3e97-286d-49c9-83ae-a9006b4007b7; MKT_Pagesource=PC; manualclose=1; ibulanguage=CN; ibulocale=zh_cn; cookiePricesDisplayed=CNY; librauuid=; nfes_isSupportWebP=1; Hm_lpvt_a8d6737197d542432f4ff4abc6e06384=1757075254; _ga_5DVRDQD429=GS2.1.s1757074904$o1$g1$t1757075262$j52$l0$h0; _ga_B77BES1Z8Z=GS2.1.s1757074904$o1$g1$t1757075262$j52$l0$h0; _ga_9BZF483VNQ=GS2.1.s1757074904$o1$g1$t1757075262$j52$l0$h0; _ubtstatus=%7B%22vid%22%3A%221757074904851.1d98GRGifqwz%22%2C%22sid%22%3A1%2C%22pvid%22%3A12%2C%22pid%22%3A600001375%7D; _bfaStatusPVSend=1; _bfi=p1%3D600001375%26p2%3D102001%26v1%3D12%26v2%3D11; _bfaStatus=success; intl_ht1=h4=30_67690986,2_8063900,30_535673,30_105849420,30_347431; _jzqco=%7C%7C%7C%7C1757074905860%7C1.1290556627.1757074905688.1757081292854.1757081998459.1757081292854.1757081998459.0.0.0.16.16; _RF1=82.26.72.152; _bfa=1.1757074904851.1d98GRGifqwz.1.1757081997983.1757083547323.1.18.102003',
    }

    json_data = {
        'masterHotelId': hotelId,
        'isBusiness': False,
        'feature': [],
        'cityCode': 30,
        'checkIn': checkIn,
        'checkOut': checkOut,
        'head': {
            'Locale': 'zh-CN',
            'Currency': 'CNY',
            'Device': 'PC',
            'Group': 'ctrip',
            'ReferenceID': '',
            'UserRegion': 'CN',
            'AID': '4899',
            'SID': '135371',
            'Ticket': '',
            'UID': '',
            'IsQuickBooking': '',
            'ClientID': '09031125113956821417',
            'OUID': '',
            'TimeZone': '8',
            'P': '37856503287',
            'PageID': '102003',
            'Version': '',
            'HotelExtension': {
                'WebpSupport': True,
                'group': 'CTRIP',
                'Qid': '411664735611',
                'hasAidInUrl': False,
            },
            'Frontend': {
                'vid': '1757074904851.1d98GRGifqwz',
                'sessionID': '1',
                'pvid': '18',
            },
        },
        'ServerData': '',
    }
    response = requests.post(
        'https://m.ctrip.com/restapi/soa2/21881/json/hotelStaticInfo',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    data = json.loads(response.text)['Response']

    # 酒店名称，星级，具体地址，房间数，开业时间，description
    hotelInfo = data.get('hotelInfo', {})
    hotelPolicy = data.get('hotelPolicy', {})
    hotelFacility = data.get('hotelFacility', {})
    results = {
        "hotelId": hotelId,
        "hotelName": hotelInfo["basic"]["name"],
        "hotelInfo": hotelInfo,
        "hotelPolicy": hotelPolicy,
        "hotelFacility": hotelFacility
    }
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    return results


def get_hotel_room_list(hotelId, checkIn, checkOut, save_path):
    # 目标 API URL
    url = "https://m.ctrip.com/restapi/soa2/33278/getHotelRoomListInland"

    # 设置 HTTP 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://m.ctrip.com",
        "Referer": "https://m.ctrip.com/webapp/hotel/hoteldetail/986963.html",
        "Accept": "application/json",
        "Cookie": MY_COOKIES
    }

    # 构造请求体 (Payload)
    payload = {

        "head": {
            "cid": "09031109111783748130",
            "ctok": "",
            "cver": "999999",
            "lang": "01",
            "sid": "2611971",
            "syscode": "09",
            "auth": "",
            "xsid": "",
            "extension": [],
            "platform": "H5",
            "aid": "4899",
            "ouid": "Singapore",
            "locale": "zh-CN",
            "pageId": "",
            "currency": "CNY",
            "vid": "",
            "timezone": "8",
            "isSSR": False,
            "guid": "",
            "group": "ctrip",
            "bu": "HBU"
        },

        "search": {
            "hotelId": hotelId,
            "checkIn": checkIn.replace("-", ""),  # 移除连字符以匹配API期望的格式
            "checkOut": checkOut.replace("-", ""),  # 移除连字符以匹配API期望的格式
             }
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)

        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()["data"]

            calendarInfo = data.get('calendarInfo', {})
            sale_room_map = data.get('saleRoomMap', {})
            physicRoomMap = data.get('physicRoomMap', {})

            results = fetchInfo(hotelId, checkIn, checkOut, save_path)
            results["calendarInfo"] = calendarInfo
            noRoomTip = data.get('noRoomTip', {})
            rooms = {}
            # 检查是否有足够的信息表明没有房间
            if noRoomTip.get("title") or noRoomTip.get("content"):
                print(f"{noRoomTip['title']},{noRoomTip['content']}")
                results["rooms"] = {}
                results["noRoomTip"] = noRoomTip
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=4)
                return results
            if not sale_room_map:
                print("未找到 saleRoomMap，请检查 Cookie ")
                results["rooms"] = {}
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=4)
                return results

            for sale_key, info in sale_room_map.items():
                # 确定这个房型是否有房
                isBooking = info.get('bookingStatusInfo', False).get('isBooking', False)
                if isBooking:
                    # 1. 提取房型名称 (对应截图中的 name)
                    room_name = info.get('name', '未知房型')
                    phy_id = info.get('physicalRoomId', 0)
                    room_images = []
                    for phy_key, room_info in physicRoomMap.items():
                        if room_info.get('id') == phy_id:
                            # 只要 ID 对上了，就拿它的图片（虽然可能有些许误差，但通常图片是通用的）
                            raw_pics = room_info.get('pictureInfo', [])
                            room_images = [p.get('url') for p in raw_pics]
                            break
                    # 2. 提取价格 (对应截图中的 price -> roomPriceText)
                    # 兼容不同结构：优先取 price 对象，没有则取 money 对象
                    price = "暂无"
                    if 'price' in info:
                        price = info['price'].get('roomPriceText', 0)

                    # 3. 提取是否钟点房
                    is_hour_room = info.get('isHourRoom', False)

                    # 4. 提取标签
                    tagInfoList = info.get('tagInfoList', [])

                    rooms[sale_key] = {
                        "id": info.get('id', 0),
                        "physicalRoomId": phy_id,
                        "name": room_name,
                        "is_hour_room": is_hour_room,
                        "price": price,
                        "images": room_images,
                        "tagInfoList": tagInfoList

                    }
            results["rooms"] = rooms
            print(f"成功获取 {len(rooms)} 条报价数据\n")
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            return results
        else:
            print(f"HTTP 请求失败，状态码: {response.status_code}")
            print(response.text)
            return {}

    except Exception as e:
        print(f"发生错误: {e}")
        return {}


if __name__ == "__main__":

    details = get_hotel_room_list(hotelId=111624963, checkIn="2025-11-29",
                                  checkOut="2025-11-30", save_path="output/hoteldetails.json")

from fetchHotelList import *
from fetchHotelDetails import *
from fetchHotelComments import *


# 获取酒店列表
city_id = 477  # 武汉
check_in = "2025-11-29"
check_out = "2025-11-30"
print(f"正在搜索城市ID: {city_id}, 日期: {check_in} - {check_out}")
keyword = "武汉理工大学南湖校区"
# 构造筛选条件
my_filters = []
my_filters.append({"filterId": f"30|{keyword}", "type": "30",
                   "value": keyword, "title": "keyword筛选"})

hotelLists = fetchHotels(
    city_id=city_id,
    check_in=check_in,
    check_out=check_out,
    keyword=keyword,  # 使用filters时，keyword留空
    filters=my_filters,
    numPages=1,  # numPages=0 时爬取全部
    savePath=f"output/hotelLists_{city_id}_{check_in}_{check_out}.json"
)

# 获取酒店房间详情
# hotel_id = 111624963
hotel_id = hotelLists[1]["hotelId"]
details = get_hotel_room_list(hotelId=hotel_id, checkIn=check_in, checkOut=check_out,
                              save_path=f"output/details_{hotel_id}.json")

# 获取酒店评论
comments = run_spider(hotel_id, start_page=1, end_page=2, save_path=f"output/comments_{hotel_id}.json")

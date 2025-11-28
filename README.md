# 携程酒店信息爬取

## 项目简介

本项目用于爬取携程网指定城市的酒店信息，并将结果保存为 JSON 文件。

## 使用方法

1. **克隆项目**

   ```bash
   git clone <项目地址>
   ```

2. **创建虚拟环境**

   使用 Conda 创建虚拟环境：

   ```bash
   conda create -n xiecheng_env python=3.10 -y
   conda activate xiecheng_env
   ```

3. **运行项目**

   修改 `main.py` 中的配置参数（如 `cityId`、`numHotelPages` 、`checkIn`和`checkOut`），并运行项目。`），然后运行：

   ```bash
   python main.py
   ```
    
4. **注意事项**

   注意修改MY_COOKIES,可以从网页上获取
   
   fetchHottelList和fecthHotelDetail代码中只需要修改MY_COOKIES即可，

   而fetchHotelComments代码中不仅需要修改MY_COOKIES还要修改FX_TOKEN、TRACE_ID
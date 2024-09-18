import streamlit as st
import googlemaps
from urllib.parse import quote  # 用於進行 URL 編碼

# 輸入你的 Google Maps API key

gmaps = googlemaps.Client(key=API_KEY)

# 地點資料（只包含地點名稱）
locations = [
    "雲林縣麥寮鄉公所",
    "雲林縣立麥寮高級中學",
    "麥寮義和保安宮",
    "雲林縣消防局第三大隊麥寮消防分隊",
    "星巴克 雲林麥寮門市",
    "台灣中油 品強加油站",
    "麥寮鄉農會濕穀集運中心",
    "麥寮鄉農會蔬果集貨場",
    "光大寮聚寶宮",
    "麥寮鎮南宮",
    "麥寮鎮西宮",
    "麥寮運動公園",
    "施府大將軍廟",
    "麥寮沙崙後安西宮",
    "7-ELEVEN 三勝門市",
    "後安福興宮",
    "霄仁厝永福宮",
    "許厝寮 福興宮",
    "三盛社區公園",
    "阿媽紀念公園",
    "台塑石油 春田加油站",
    "雲都商務飯店",
]
locations = sorted(locations)

# Streamlit 標題
st.title("最佳路徑規劃")

# 讓使用者選擇起點
#start_location = st.selectbox("選擇起點", locations)
#
start_location = "麥寮定點倒垃圾"
st.write(f'出發/終點: {start_location}')

# 讓使用者選擇要經過的地點
waypoints_selected = st.multiselect("選擇要經過的地點", [loc for loc in locations if loc != start_location])

# 提交按鈕
if st.button("規劃路徑"):
    try:
        # 使用 Google Maps API 進行路徑規劃
        directions_result = gmaps.directions(
            origin=start_location,
            destination=start_location,  # 回到起點
            mode="driving",
            waypoints=waypoints_selected,
            optimize_waypoints=True,
            language="zh-TW",
            departure_time="now",  # 指定當前時間出發
            traffic_model="best_guess"  # 使用交通模型進行最佳估算
        )
#        directions_result = gmaps.directions(
#            origin=start_location,
#            destination=start_location,  # 回到起點
#            mode="driving",
#            waypoints=waypoints_selected,
#            optimize_waypoints=True,
#            language="zh-TW"  # 設置語言為繁體中文
#        )

        # 檢查是否有返回結果
        if directions_result and len(directions_result) > 0:
            best_route = directions_result[0]['legs']
            total_duration = sum([leg['duration']['value'] for leg in best_route])  # 總時間（以秒為單位）
            total_duration_in_minutes = total_duration / 60  # 轉換為分鐘

            st.subheader("最佳路徑順序：")

            # 起始地點
            st.write(f"從 {start_location} 開始")
            pathNo = 1
            for i, leg in enumerate(best_route):
                # 找到該段路徑的起點和終點
                start_address = leg['start_address']
                end_address = leg['end_address']

                # 查找起點和終點的地點名稱
                start_name = start_location if i == 0 else waypoints_selected[i - 1]
                end_name = start_location if i == len(best_route) - 1 else waypoints_selected[i]

                # 顯示路徑，並在地址後加上地點名稱
                st.write(f"{pathNo: } 從 {start_name} 到 {end_name}, 距離: {leg['distance']['text']}, 預計時間: {leg['duration']['text']}")
                # 原版/顯示路徑，並在地址後加上地點名稱
#                st.write(f"{pathNo: } 從 {start_address} ({start_name}) 到 {end_address} ({end_name}), 距離: {leg['distance']['text']}, 預計時間: {leg['duration']['text']}")
                pathNo += 1

            # 顯示總行程時間
            st.write(f"\n總行程時間為: {total_duration_in_minutes:.2f} 分鐘")

            # 生成 Google Maps 路徑 URL
            base_url = "https://www.google.com/maps/dir/?api=1"
            origin_param = f"origin={quote(start_location)}"
            destination_param = f"destination={quote(start_location)}"

            # 對經過地點進行 URL 編碼
            waypoints_param = f"&waypoints={'|'.join([quote(loc) for loc in waypoints_selected])}" if waypoints_selected else ""

            # 生成最終 URL
            map_url = f"{base_url}&{origin_param}&{destination_param}{waypoints_param}&travelmode=driving"

            # 顯示 Google Maps 的鏈接
            st.markdown(f"[在 Google Maps 中查看路徑]({map_url})")

        else:
            st.error("無法找到路徑，請檢查輸入的地點是否正確。")

    except Exception as e:
        st.error(f"發生錯誤：{e}")

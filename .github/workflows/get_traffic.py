import requests
from bs4 import BeautifulSoup
import json
import re
import datetime

# Yahoo!道路交通情報（関東・高速）
URL = "https://roadway.yahoo.co.jp/traffic/area/4/highways"

def get_traffic_data():
    try:
        # 1. サイトにアクセス
        headers = {'User-Agent': 'Mozilla/5.0 (TrafficRadioApp/1.0)'}
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        traffic_messages = []
        
        # 2. 現在時刻を追加
        now = datetime.datetime.now().strftime('%H時%M分')
        traffic_messages.append(f"{now}現在の、道路交通情報をお知らせします。")

        # 3. 渋滞情報を探す (Yahooの構造に合わせて解析)
        # 注意: サイトの構造が変わると動かなくなる可能性があります
        found_info = False
        
        # 「section」タグの中に路線ごとの情報があることが多い
        sections = soup.find_all('div', class_='section')
        
        target_roads = ['中央道', '関越道', '東名', '首都高'] # 読み上げたい主要道路
        
        for section in sections:
            road_name_tag = section.find('h3')
            if not road_name_tag:
                continue
                
            road_name = road_name_tag.text.strip()
            
            # ターゲットの道路か確認
            is_target = False
            for t in target_roads:
                if t in road_name:
                    is_target = True
                    break
            if not is_target:
                continue

            # その道路の渋滞リストを取得
            # Yahooは tr タグなどでリスト化されている場合がある
            # ここでは簡易的にテキストを含む要素を探します
            info_text = section.get_text().replace('\n', ' ').strip()
            
            # 「渋滞」などのキーワードが含まれるか
            if '渋滞' in info_text or '事故' in info_text:
                # 余計な空白を削除して読みやすくする処理
                # 例: "中央道(上り) 小仏TN付近 渋滞20km" のようなパターンを抽出したい
                # 簡易的な抽出ロジック
                lines = section.find_all(['p', 'li', 'tr'])
                for line in lines:
                    text = line.get_text().strip()
                    if ('渋滞' in text or '事故' in text) and len(text) > 5:
                        # 読み上げ用に少し整形
                        text = text.replace('TN', 'トンネル').replace('IC', 'インター')
                        traffic_messages.append(f"{road_name}、{text}。")
                        found_info = True

        if not found_info:
            traffic_messages.append("現在、関東エリアの主要高速道路で、目立った渋滞情報は入っていません。順調に流れています。")
        
        traffic_messages.append("以上、交通情報をお伝えしました。")

        # 4. JSONファイルとして保存
        with open('traffic.json', 'w', encoding='utf-8') as f:
            json.dump(traffic_messages, f, ensure_ascii=False, indent=2)
            
        print("Data saved successfully.")

    except Exception as e:
        print(f"Error: {e}")
        # エラー時はダミーデータを入れる
        dummy = ["情報の取得に失敗しました。しばらくしてから再度お試しください。"]
        with open('traffic.json', 'w', encoding='utf-8') as f:
            json.dump(dummy, f, ensure_ascii=False)

if __name__ == "__main__":
    get_traffic_data()

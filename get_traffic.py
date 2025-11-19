import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

# Yahoo!道路交通情報（関東エリア・高速道路）
URL = "https://roadway.yahoo.co.jp/traffic/area/4/highways"

def get_traffic_data():
    messages = []
    
    # 1. 時刻を入れる
    now = datetime.datetime.now().strftime('%H時%M分')
    messages.append(f"{now}現在の、道路交通情報です。")

    try:
        print("Connecting to Yahoo...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        res = requests.get(URL, headers=headers, timeout=15)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'html.parser')

        # 2. データを抽出する（作戦変更：ページ内の「渋滞」を含む行をすべて拾う）
        # 特定のタグに頼らず、ページ全体のテキストから探す「網羅的」な方法
        all_text = soup.get_text('\n')
        lines = all_text.split('\n')
        
        found_info = []
        
        # ターゲット（これらが含まれていたら読む）
        targets = ['中央道', '関越道', '東名', '首都高', '常磐道', '東北道', '外環', '圏央道']

        for line in lines:
            text = line.strip()
            if not text: continue
            
            # 「渋滞」「事故」「規制」のどれかを含み、かつ「ターゲット道路」の名前が入っているか？
            if ('渋滞' in text or '事故' in text or '規制' in text or '通行止' in text):
                for road in targets:
                    if road in text:
                        # 余計な記号を掃除
                        clean = text.replace('>', '').replace('↓', '下り').replace('↑', '上り')
                        clean = re.sub(r'\s+', '、', clean) # 空白を読点に
                        
                        if clean not in found_info:
                            found_info.append(clean)
                        break

        # 3. 結果をまとめる
        if len(found_info) > 0:
            messages.extend(found_info)
        else:
            # 1件も見つからなかった場合（順調、または取得ミス）
            messages.append("現在、関東エリアの主要な高速道路で、目立った渋滞情報は見当たりません。")
            messages.append("全線、順調に流れています。")

    except Exception as e:
        print(f"Error: {e}")
        messages.append("情報の取得中にエラーが発生しました。")
        messages.append("ネット環境を確認してください。")

    messages.append("以上、交通情報をお伝えしました。")

    # 4. 保存
    with open('traffic.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    print("Success!")

if __name__ == "__main__":
    get_traffic_data()

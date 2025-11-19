import requests
from bs4 import BeautifulSoup
import json
import datetime

# --- 設定エリア ---
URL = "https://roadway.yahoo.co.jp/traffic/area/4/highways"
TARGETS = ['中央道', '関越道', '東名', '首都高', '東北道', '常磐道']

def get_traffic_data():
    messages = []
    try:
        # 1. サイトにアクセス
        print("Fetching data...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(URL, headers=headers, timeout=10)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, 'html.parser')

        # 2. 時刻を記録
        now = datetime.datetime.now().strftime('%H時%M分')
        messages.append(f"{now}現在の、道路交通情報です。")

        # 3. 情報を探す
        # ページ内のすべての文章を取得して、行ごとにチェックする作戦
        text_data = soup.get_text('\n')
        lines = text_data.split('\n')
        
        found_count = 0
        
        for line in lines:
            # 空白を削除
            text = line.strip()
            if not text:
                continue
                
            # キーワード判定
            # 「渋滞」「事故」「規制」のいずれかがあり、かつターゲットの道路名が入っているか
            is_incident = ('渋滞' in text) or ('事故' in text) or ('規制' in text)
            
            if is_incident:
                for road in TARGETS:
                    if road in text:
                        # 読み上げやすいように整形
                        clean_text = text.replace('>', '').replace('↓', '下り').replace('↑', '上り')
                        clean_text = clean_text.replace('TN', 'トンネル').replace('IC', 'インター')
                        clean_text = clean_text.replace('JCT', 'ジャンクション')
                        
                        # 重複チェック（同じ行を何度も読まないように）
                        if clean_text not in messages:
                            messages.append(clean_text)
                            found_count += 1
                        break

        # 4. 何も見つからなかった場合
        if found_count == 0:
            messages.append("現在、関東エリアの主要高速道路で、目立った渋滞情報はありません。順調です。")
        
        messages.append("以上、交通情報でした。")

    except Exception as e:
        print(f"Error: {e}")
        messages = ["情報の取得に失敗しました。", "ネットの接続状況などを確認してください。"]

    # 5. 保存
    with open('traffic.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    print("Saved successfully.")

if __name__ == "__main__":
    get_traffic_data()

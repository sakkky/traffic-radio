import requests
from bs4 import BeautifulSoup
import json
import datetime

# Yahoo!道路交通情報（関東・高速）
URL = "https://roadway.yahoo.co.jp/traffic/area/4/highways"

def get_traffic_data():
    messages = []
    
    try:
        # 1. サイトにアクセス
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. 現在時刻を追加
        now = datetime.datetime.now().strftime('%H時%M分')
        messages.append(f"{now}現在の、道路交通情報をお知らせします。")

        # 3. 情報を探す（ロジックを簡略化・強化）
        # Yahooのページからテキストを抽出
        found_something = False
        
        # ページ内の主要なリスト要素をざっくり探す
        # ターゲット道路：中央道, 関越道, 東名, 首都高, 東北道, 常磐道
        target_roads = ['中央道', '関越道', '東名', '首都高', '東北道', '常磐道']
        
        # ページ全体のテキストからキーワードを含む行を探す作戦に変更
        text_lines = soup.get_text('\n').split('\n')
        
        for line in text_lines:
            line = line.strip()
            if not line: continue

            # 「渋滞」または「事故」が含まれ、かつターゲットの道路名が含まれる行を探す
            if ('渋滞' in line or '事故' in line or '規制' in line):
                for road in target_roads:
                    if road in line:
                        # 余計な記号を削除して読みやすくする
                        clean_text = line.replace('>', '').replace('↓', '下り').replace('↑', '上り')
                        clean_text = clean_text.replace('TN', 'トンネル').replace('IC', 'インター').replace('JCT', 'ジャンクション')
                        
                        # 同じ情報が重複しないようにチェック
                        if clean_text not in messages:
                            messages.append(clean_text + "。")
                            found_something = True
                        break # この行はもう処理したので次へ

        # 4. もし何も見つからなかった場合のメッセージ
        if not found_something:
            messages.append("現在、関東エリアの主要な高速道路で、事故や渋滞の情報は見当たりません。順調に流れています。")
        
        messages.append("以上、交通情報をお伝えしました。")

    except Exception as e:
        print(f"Error: {e}")
        messages = ["情報の取得に失敗しました。", str(e)]

    # 5. JSONファイルとして保存
    with open('traffic.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    print("Done.")

if __name__ == "__main__":
    get_traffic_data()

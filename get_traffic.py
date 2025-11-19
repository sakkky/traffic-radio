import requests
import json
import datetime

# テスト用のシンプルなコード
def get_traffic_data():
    print("Start scraping...")
    messages = []
    
    # 1. 時刻を入れる
    now = datetime.datetime.now().strftime('%H時%M分')
    messages.append(f"{now}、情報の更新テストです。")
    
    # 2. とりあえず固定のメッセージを入れてみる（エラー回避）
    messages.append("現在、システムの調整を行っています。")
    messages.append("GitHub Actionsは正常に動いています。")
    
    # 3. 保存
    try:
        with open('traffic.json', 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print("Save success!")
    except Exception as e:
        print(f"Save failed: {e}")

if __name__ == "__main__":
    get_traffic_data()

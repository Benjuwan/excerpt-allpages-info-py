import google.generativeai as genai  # Google Gemini API用ライブラリ
import sys  # システム制御に関する標準ライブラリ（APIキーをチェックして無効の場合は処理を中断する）
import os  # OSの環境変数操作用
from urllib.parse import urljoin  # URLの結合・正規化
from urllib.parse import urlparse  # URLの解析
from tqdm import tqdm  # プログレスバーを表示するための非標準ライブラリ
import requests  # Webページからコンテンツ（情報）を取得
from bs4 import BeautifulSoup  # DOMを操作するための非標準ライブラリ
from PIL import Image  # 画像処理用ライブラリ（Pillow）
from io import BytesIO  # バイナリデータをファイルのように扱う
from dotenv import load_dotenv  # .envファイルから環境変数を読み込む


# Gemini APIの設定
load_dotenv()  # ローカルの .env ファイルから環境変数（秘匿情報など）を読み込んで、os.environ で参照できるようにする関数
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY is None:
    sys.exit("GOOGLE_API_KEY が設定されていない。または有効でないAPIキーです。")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")


# Gemini への処理要求
def _request_Gemini(img: str, img_url: str, keyword: str) -> dict | None:
    response = requests.get(img_url)

    # レスポンス判定
    if response.status_code != 200:
        print(f"レスポンスエラー：status-[{response.status_code}]\n{img}")
        return None

    # 画像形式の検証
    if not response.headers.get("content-type", "").startswith("image/"):
        print(f"画像ファイルではありません: {img_url}")
        return None

    # レスポンス内容をバイナリデータ化して画像データとして出力（開く）
    image = Image.open(BytesIO(response.content))

    prompt = f"画像内に「{keyword}」という文字列が含まれている場合は「処理中のページURL」と「画像内のどの部分に存在するか明示的に教えて」ください。含まれていない場合は「該当なし」という文言だけを返して処理スキップしてください。"

    # Geminiに画像を解析してもらう
    response = model.generate_content([prompt, image])

    # strip() で文字列・文章前後の空白をトリミングし、改行を。に置換する
    res_text = response.text.strip().replace("\n", "。")

    return dict({"title": res_text, "url": img_url})


def _create_img_list(current_url: str | None = None) -> list | None:
    if current_url is None:
        return None

    try:
        # webページの情報を取得。10秒以上かかる場合は処理中断
        res = requests.get(current_url, timeout=10)

        # HTTPステータスコードをチェックし、エラー（4xx, 5xx）があれば例外（`raise`）を発生させる
        res.raise_for_status()

        res = requests.get(current_url)
        res.encoding = res.apparent_encoding  # エンコーディング処理

        # BeautifulSoupでDOM操作を行う準備
        soup = BeautifulSoup(res.text, "html.parser")
        img_list = soup.find_all("img", src=True)

    # Exception：大部分の例外の基底クラス
    except Exception as e:
        print(f"エラーが発生しました | _create_img_list : {e}")
        return None

    return img_list


# 1. はじめに、モジュールの主要な処理を関数にまとめる
# 実引数は呼び出し元で指定するので、仮引数としてオプショナルな指定（None）に留めておく
def generate_filtered_result_byGemini(
    current_url: str | None = None,
    keyword: str | None = None,
    results: list[dict] | None = None,
) -> list[dict] | None:
    if current_url is None or keyword is None or results is None:
        return None

    img_list = _create_img_list(current_url)
    for img in tqdm(img_list, desc=f"{current_url} ページの画像処理中"):
        try:
            # 画像URLを取得して正規化
            img_url: str = img.get("src")

            if img_url is None:
                continue

            # URLスキーム（http:// や https:// など）の有無をチェック
            # `urlparse(img_url).scheme`はスキーム（プロトコル）がある場合はそのスキーム名を、無い場合は空文字を返す
            if not urlparse(img_url).scheme:
                # スキームが無い（適切なURL記述でない）場合は空文字が返ってくるので`img_url`は相対パスとなり、
                # それを`urljoin`で`current_url`を基準とした絶対パスに変換する
                img_url = urljoin(current_url, img_url)

            # Gemini への処理要求
            result: dict | None = _request_Gemini(img, img_url, keyword)

            if result is None or result["title"].count("該当なし") > 0:
                print(f"「{img_url}」の画像内に「{keyword}」は存在しませんでした")
                continue

            results.append(result)

        # Exception：大部分の例外の基底クラス
        except Exception as e:
            print(f"エラーが発生しました | generate_filtered_result_byGemini.py : {e}")
            continue

    print(f"generate_filtered_result_byGemini ：{results}")
    return results


# 2. モジュールを単独で（Pythonコマンドで）実行したときに関数を呼び出す処理を追加
if __name__ == "__main__":
    generate_filtered_result_byGemini()

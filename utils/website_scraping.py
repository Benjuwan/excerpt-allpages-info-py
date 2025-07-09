# webページの情報を取得する非標準ライブラリ
import requests

# 取得したwebページ内のDOMを操作するための非標準ライブラリ
from bs4 import BeautifulSoup

# webページの情報を取得する標準ライブラリ。今回は url文字列を操作（結合、解析）する処理を利用
from urllib.parse import urljoin, urlparse

# 指定した時間ごとに処理を行う標準ライブラリ
import time


# 第一引数：`対象サイトのURL`, 第二引数（任意）：`検出対象ページ数`（デフォルト = 100件）, 第三引数（任意）：`検出対象は同一オリジン限定か他のドメインも含めるか`（デフォルト = `True` -> 同一オリジン限定）
def website_scraping(
    start_url: str | None = None, max_pages=100, is_only_same_origin: bool = True
) -> list | None:
    if start_url is None:
        return None

    # 訪問結果履歴として扱うリスト
    visited: list[dict] = []

    # 訪問予定リスト（スクレイピング対象Webサイトの各種ページURLを格納する文字列リスト）
    to_visit: list[str] = [start_url]

    # スクレイピングしたいWebサイトのURLからドメイン名（`netloc`）を取得
    base_domain = urlparse(start_url).netloc

    # 訪問予定リストがあって、検索結果履歴数が検索ページ数の上限値以下の場合は、以下のループ処理を続ける
    while to_visit and len(visited) < max_pages:
        # 訪問予定リストの「先頭（※指定されたインデックス番号が 0 なので）」から文字列を抽出
        current_url = to_visit.pop(0)

        # 既にスクレイピング済みページの場合は処理スキップ
        is_task_skip = any(
            [current_url in visited_url["url"] for visited_url in visited]
        )
        if is_task_skip:
            continue

        try:
            print(f"{len(visited) + 1} | スクレイピング中: {current_url}\n")

            # webページの情報を取得。10秒以上かかる場合は処理中断
            res = requests.get(current_url, timeout=10)

            # HTTPステータスコードをチェックし、エラー（4xx, 5xx）があれば例外（`raise`）を発生させる
            res.raise_for_status()

            res = requests.get(current_url)
            res.encoding = res.apparent_encoding  # エンコーディング処理

            # BeautifulSoupでDOM操作を行う準備
            soup = BeautifulSoup(res.text, "html.parser")

            # スクレイピングしたWebページの title タグ情報を取得
            title = soup.find("title")

            # title タグ情報から空白や改行をトリミングして文字列整形する
            current_title = title.text.strip() if title else ""

            # 今しがたスクレイピングしたWebページの情報を新しい辞書として作成
            # ループ処理（while なので条件が Trueの限り処理を繰り返す）の中で、当該辞書データを都度作成することで現ループ時点の内容が格納され（て後述の visited リストに追加され）る
            visited_info: dict = dict({"title": current_title, "url": current_url})

            # href属性を持った全 a タグをループ処理
            for link in soup.find_all("a", href=True):
                # 相対パスから絶対パスを生成（href属性に指定された相対パスを絶対パスにした内容を取得）
                full_url = urljoin(current_url, link["href"])

                # 相対パスから生成した絶対パスを解析してURL文字列として扱う
                parsed_url = urlparse(full_url)

                # 同一ドメインのHTTP/HTTPSリンクのみ
                is_same_origin: bool = (
                    # ドメイン名が同じ場合
                    parsed_url.netloc == base_domain
                    # かつ（当該URL文字列のプロトコルが）`http`,`https`で始まる場合
                    and parsed_url.scheme in ["http", "https"]
                )

                # 同一ドメインに加えて他のドメインも検出対象に含む場合
                is_cross_origin: bool = parsed_url.scheme in ["http", "https"]

                is_can_add_to_visit: bool = (
                    is_same_origin
                    if is_only_same_origin
                    else is_cross_origin
                    # かつ未訪問（未スクレイピング）なWebページの場合（相対パスから生成した絶対パスが訪問結果履歴に含まれていない）
                    and full_url not in visited_info["url"]
                    and full_url not in to_visit
                )

                if is_can_add_to_visit:
                    # 新しく発見したURLを訪問予定リストの末尾に追加
                    to_visit.append(full_url)

            # 訪問結果履歴リストに今しがた検出した訪問結果を格納
            visited.append(visited_info)

            # 1秒間処理を停止（サーバーに負荷をかけないよう配慮）
            time.sleep(1)

        # 例外処理（エラーハンドリング）
        except Exception as e:
            print(f"エラー: {current_url} - {e}")

    # 訪問結果履歴リストを返す
    return visited


if __name__ == "__main__":
    website_scraping()

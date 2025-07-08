import requests  # webページの情報を取得する非標準ライブラリ


# 検索対象キーワードを含んだページ情報のみ返す
def _get_res_text(keyword: str, text: dict) -> dict | None:
    res = requests.get(text["url"])
    res.encoding = res.apparent_encoding  # エンコーディング処理

    if res.text.count(keyword):
        return dict({"title": text["title"], "url": text["url"]})

    return None


def filtered_keyword(res_text_list: list[dict] = []) -> list[dict] | None:
    # 検索対象キーワード
    keyword = input("入力文字にヒットしたページ限定で処理を進める：")

    if len(keyword) == 0:
        print(
            f"{len(keyword)}文字なので何も入力されていないようです\n全件（{len(res_text_list)}件）処理で進めます"
        )
        return None

    filtered_keyword_list: list[dict] = list(
        # filter(関数, イテラブル)
        filter(
            # lambda 引数: 式（今回はプライベートメソッド）
            lambda text: _get_res_text(keyword, text),
            res_text_list,
        )
    )

    if len(filtered_keyword_list) > 0:
        print(
            f"検索対象キーワード：「{keyword}」は「{len(filtered_keyword_list)}」件ヒットしました"
        )
        return filtered_keyword_list

    print(
        f"該当件数は「{len(filtered_keyword_list)}」件だったので全件（{len(res_text_list)}件）処理で進めます"
    )
    return None


if __name__ == "__main__":
    filtered_keyword()

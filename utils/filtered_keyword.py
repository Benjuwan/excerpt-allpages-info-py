import requests  # webページの情報を取得する非標準ライブラリ

from create_alt_txt_byGemini import create_alt_txt_byGemini


# ページ内（文字列）にキーワードが含まれている場合、ページ情報を返す
def _get_result_page_info_dict(keyword: str, text: dict) -> dict | None:
    res = requests.get(text["url"])
    res.encoding = res.apparent_encoding  # エンコーディング処理

    if res.text.count(keyword) > 0:
        return dict({"title": text["title"], "url": text["url"]})

    return None


# ページ内（文字列）にキーワードが含まれていない場合、ページ内の各画像チェックに移行
def _get_result_page_info_dict_list(
    keyword: str, text: dict, results: list[dict]
) -> list[dict] | None:
    res = requests.get(text["url"])
    res.encoding = res.apparent_encoding  # エンコーディング処理

    if res.text.count(keyword) == 0:
        images_analyze_by_Gemini_result: list[dict] | None = create_alt_txt_byGemini(
            res.url, keyword, results
        )
        if images_analyze_by_Gemini_result is not None or (
            images_analyze_by_Gemini_result is not None
            and len(images_analyze_by_Gemini_result) == 0
        ):
            return images_analyze_by_Gemini_result

    return None


def filtered_keyword(res_text_list: list[dict] = []) -> list[dict] | None:
    keyword = input("入力文字にヒットしたページ限定で処理を進める：")

    if len(keyword) == 0:
        print(
            f"{len(keyword)}文字なので何も入力されていないようです\n全件（{len(res_text_list)}件）処理で進めます"
        )
        return None

    # ページ内テキスト情報を対象とした検出処理
    filtered_keyword_list: list[dict] = list(
        # filter(関数, イテラブル)
        filter(
            # lambda 引数: 式（今回はプライベートメソッド）
            lambda text: _get_result_page_info_dict(keyword, text),
            res_text_list,
        )
    )

    if len(filtered_keyword_list) == 0:
        print(
            f"テキスト検出結果「{len(filtered_keyword_list)}件」だったのでページ内画像検出に移行します\n{'-' * 45}\n"
        )

    # ページ内の文字列検出でヒットしなかった場合、ページ内の画像検出処理に移行する
    results: list[dict] = []
    final_result_filtered_keyword_list = (
        filtered_keyword_list
        if len(filtered_keyword_list) > 0
        else list(
            filter(
                lambda text: _get_result_page_info_dict_list(keyword, text, results),
                res_text_list,
            )
        )
    )

    if len(final_result_filtered_keyword_list) > 0:
        print(
            f"検索対象キーワード：「{keyword}」は「{len(final_result_filtered_keyword_list)}」件ヒットしました"
        )
        return final_result_filtered_keyword_list

    print(
        f"該当件数は「{len(final_result_filtered_keyword_list)}」件だったので全件（{len(res_text_list)}件）処理で進めます"
    )
    return None


if __name__ == "__main__":
    filtered_keyword()

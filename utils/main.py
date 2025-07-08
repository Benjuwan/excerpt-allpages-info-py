from website_scraping import website_scraping
from filtered_keyword import filtered_keyword
from generate_xlsx import generate_xlsx

# スクレイピングしたいwebサイトのURL（と任意でスクレイピング処理対象ページ数）を指定
website_scraping_result = website_scraping("https://example-company.co.jp", 5)
if website_scraping_result is not None:
    print(f"総計 {len(website_scraping_result)} ページをスクレイピング")

    # 検索対象キーワードでフィルターする
    filtered_keyword_list = filtered_keyword(website_scraping_result)
    website_scraping_result = (
        website_scraping_result
        if filtered_keyword_list is None
        else filtered_keyword_list
    )

    # 抽出結果をエクセルファイルとして保存
    generate_xlsx(website_scraping_result)

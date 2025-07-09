from website_scraping import website_scraping
from filtered_keyword import filtered_keyword
from generate_xlsx import generate_xlsx

# 第一引数：`対象サイトのURL`, 第二引数（任意）：`検出対象ページ数`（デフォルト = 100件）, 第三引数（任意）：`検出対象は同一オリジン限定か他のドメインも含めるか`（デフォルト = `True` -> 同一オリジン限定）
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

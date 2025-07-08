import openpyxl  # エクセルファイルを操作するための非標準ライブラリ

# Excelのセルの配置やテキストの表示方法を制御するために使用する Alignment クラスをインポート
from openpyxl.styles import Alignment


def generate_xlsx(website_scraping_result: list[dict] | None = None):
    if website_scraping_result is None:
        print("website_scraping_result.py の処理結果が None です")
        return

    # ワークブックの作成
    workbook = openpyxl.Workbook()

    # シートの操作
    # （各シートの）セルを読み書きするには、操作対象とするブック（オブジェクト）を選択（アクティブに）する必要がある
    worksheet = workbook.active

    if worksheet is None:
        print("worksheet は None です")
        return

    # ワークシート[セル位置]で操作
    # 読み込み：ワークシート[セル位置].value
    # 書き込み：ワークシート[セル位置] = 値
    worksheet["A1"] = "ページタイトル"
    worksheet["B1"] = "ページアドレス"

    # 幅を調整（列名での指定）
    worksheet.column_dimensions["A"].width = 100
    worksheet.column_dimensions["B"].width = 200

    for i, result in enumerate(website_scraping_result, 1):
        worksheet[f"A{i}"] = result["title"]
        worksheet[f"B{i}"] = result["url"]

        # 行の高さ設定（行単位での指定）：15が標準の1行分（デフォルト）なので 30は約2行分
        worksheet.row_dimensions[i].height = 30
        # 折り返しの設定
        worksheet[f"A{i}"].alignment = Alignment(wrap_text=True)

    # ワークブックの保存（新規作成）
    # 同名ファイルが存在する場合は上書き保存されて、無い場合は新規作成される
    workbook.save("../utils/website_scraping_result.xlsx")
    print("エクセルファイル作成完了")


if __name__ == "__main__":
    generate_xlsx()

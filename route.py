
from flask import request, render_template
import controller
from controller import get_item_list

def create_route(app):

    # JSON取得
    @app.route("/json", methods=["GET", "POST"])
    def get_json():

        if "data" in request.args:

            d = request.args.get("data")

            if d in [
                "user",
                "item",
                "kubun",
                "category",
                "dept",
                "request"
            ]:

                return controller.get_json(d)

        return("GETパラメータを指定してください")


    # トップページ
    @app.route("/")
    def top():

        return render_template("top.html")


    # 検索画面
    @app.route("/search.html")
    def search():

        return render_template("search.html")


    # 検索結果画面
    @app.route("/search-result-list.html")
    def search_result_list():

        keyword = request.args.get("keyword", "")
        category = request.args.get("category", "")
        startDate = request.args.get("startDate", "")
        endDate = request.args.get("endDate", "")

        items = get_item_list()

        result = []

        for item in items:

            matchKeyword = (
                keyword == "" or
                keyword in item["特徴"] or
                keyword in item["分類名"]
            )

            matchCategory = (
                category == "" or
                category == item["分類名"]
            )

            itemDate = str(item["登録日時"])[:10]

            matchStartDate = (
                startDate == "" or
                itemDate >= startDate
            )

            matchEndDate = (
                endDate == "" or
                itemDate <= endDate
            )

            if (
                matchKeyword and
                matchCategory and
                matchStartDate and
                matchEndDate
            ):

                result.append(item)

        return render_template(
            "search-result-list.html",
            items=result
        )


    # 詳細画面
    @app.route("/item-detail/<int:item_id>")
    def item_detail(item_id):

        items = get_item_list()

        target = None

        for item in items:

            if item["拾得物ID"] == item_id:

                target = item
                break

        return render_template(
            "item-detail.html",
            item=target
        )
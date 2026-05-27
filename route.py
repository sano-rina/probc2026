from flask import request
import controller

def create_route(app):

    @app.route("/json", methods=["GET","POST"])
    def get_json():
        if "data" in request.args:
            d = request.args.get("data")
            if d in ["user","item","kubun","category","dept","request"]:
                return controller.get_json(d)
        return("GETパラメータを指定してください")
    
    



from flask import Flask, render_template
import requests
import os

app = Flask(__name__)
URL_API = "https://fakestoreapi.com/products/"


def guardar_img(file_name, url):
    response = requests.get(url, stream=True)

    root_directory = os.path.dirname(os.path.abspath(__file__))
    static_directory = os.path.join(root_directory, r"static/images")
    file_path = os.path.join(static_directory, file_name)

    if not os.path.isfile(file_path):
        with open(file_path, "wb") as file:
            for data in response.iter_content():
                file.write(data)

    response.close()


@app.route("/")
def index():
    response = requests.get(URL_API)
    response_json = response.json()

    data = []
    for producto in response_json:
        id = producto.get("id", "")
        rating = producto.get("rating", "")

        dato_producto = [id,
                         producto.get("title", ""),
                         producto.get("price", ""),
                         producto.get("description", ""),
                         producto.get("category", ""),
                         rating.get("rate", ""),
                         rating.get("count", ""),
                         f"images/%s.jpg" % id]
        data.append(dato_producto)

        guardar_img(str(id) + ".jpg", producto.get("image"))

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)

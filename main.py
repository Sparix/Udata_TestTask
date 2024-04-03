import json

from fastapi import FastAPI, HTTPException

app = FastAPI()


def read_json_file() -> dict:
    with open("product.json", "r", encoding="UTF-8") as json_file:
        file_contents = json_file.read()
        return json.loads(file_contents)


@app.get("/all_products/")
def get_all_products():
    return read_json_file()


@app.get("/products/{product_name}")
def get_product_by_name(product_name: str):
    products = read_json_file()
    product = products.get(product_name)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products/{product_name}/{product_field}")
def get_product_field_by_name(product_name: str, product_field: str):
    products = read_json_file()
    product = products.get(product_name)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    value = product.get(product_field)
    if value is None:
        raise HTTPException(status_code=404, detail="Product field not found")
    return {product_field: value}

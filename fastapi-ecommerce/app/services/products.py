import json
from pathlib import Path
from typing import List , Dict

DATA_FILE = Path(__file__).parent.parent /"data"/"products.json"

def Load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_products() -> List[Dict]:
    return Load_products()

def save_product(products: List[Dict]) -> None:
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

def add_product(product:Dict) -> Dict:
    products = get_all_products()

    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("SKU already exsist")

    products.append(product)
    save_product(products)
    return product

def remove_product(id:int) -> None:
    products = get_all_products()
    for idx , p in enumerate(products):
        if p["id"] == int(id):
            deleted = products.pop(idx)
            save_product(products)
            return {"Message": "product deleted successfuly"}

        

def change_product(product_id: int, update_data: dict):
    products = get_all_products()

    for index, product in enumerate(products):

        if product["id"] == product_id:

            for key, value in update_data.items():

                if value is None:
                    continue

                if isinstance(value, dict) and isinstance(product.get(key), dict):
                    product[key].update(value)
                else:
                    product[key] = value

            products[index] = product
            save_product(products)
            return product
    raise ValueError("product not found")
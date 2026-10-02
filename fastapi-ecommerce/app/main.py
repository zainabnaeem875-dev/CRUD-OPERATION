from dotenv import load_dotenv
import os
from  Schema.product import Product, ProductUpdate
from fastapi import FastAPI ,HTTPException , Query , Path
from services.products import add_product, get_all_products, remove_product, change_product
app = FastAPI()



load_dotenv()
#static router
@app.get("/")
def root():
    DB_PATH = os.getenv("BASE_URL")
    return{"message": "welcome to FastAPI", "data_path": DB_PATH}


#dynamic router
# @app.get("/products/{id}")
# def get_products(id:int):
#     products = ['mouse','mointer','CPU','keyboard']
#     return (
#         products[id] 
#         if products[id]
#         else HTTPException(status_code=404 , detail="No Found")
#     )


# @app.get("/products")
# def get_products():
#     return get_all_products()


@app.get("/products")
def list_products(
     
    name:str = Query(
        default=None, 
        min_length=1, 
        max_length=50,
        description="Search by product name (case insensitive)"
    ),
    sort_by_price:bool = Query(
        default=False,
        description="sort products by price"
    ),
    orders: str = Query(
        default="asc", description="sort orders when sort_by_price=true (acs,dsc)"
    ),
    limit:int = Query(
        default=4,
        ge=1,
        le=100,
        description='Number of items to returns'
    ),
    offset:int = Query(
            default=0,
            ge=0,
            description='pagination'
        ),                          
    ):

    products = get_all_products()
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]
    if not products:
        raise HTTPException(
            status_code=404, detail=f"No products found  matching name={name}"
        )

    if sort_by_price:
            reverse = orders == "desc"
            products = sorted(products, key=lambda p:p.get("price",0), reverse=reverse)

    total = len(products)
    products = products[offset:offset+limit]
    return {"total":total ,"limit":limit, "items": products}

@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: int = Path(
    ...,
    ge=1,
    description="Numeric ID of the product",
    example=1,
    )
):
    products = get_all_products()
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="No Product Found")


@app.post("/products",status_code=201)
def create_product(product: Product):
    product_dict = product.model_dump(mode="json")
    product_dict['id'] = len(get_all_products()) + 1

    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return  product.model_dump(mode="json")
     
     
@app.delete("/products/{product_id}")
def delete_product(
    product_id : int = Path(..., description="product int")
):
   try:
       res = remove_product(product_id)
       return res
   except Exception as e:
       raise HTTPException(status_code=404,detail=str(e))


@app.put("/products/{product_id}")
def update_product(
    product_id: int = Path(..., description="Product ID"),
    payload: ProductUpdate= ...
):
    try:
        updated_product = change_product(
            product_id,
            payload.model_dump(
                mode="json",
                exclude_unset=True
            )
        )
        return updated_product

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )




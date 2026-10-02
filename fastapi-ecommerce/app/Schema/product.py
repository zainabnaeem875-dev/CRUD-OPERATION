from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated, Literal, Optional, List
from fastapi import FastAPI

app = FastAPI()


class Product(BaseModel):

    id: int

    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="Stock Keeping Unit",
            description="Unique product SKU"
        )
    ]

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=50,
            title="Product Name",
            description="Readable product name",
            examples=["Smart Watch"]
        )
    ]
    description: Annotated[
        str,
        Field(
            max_length=200,
            description="Short Product Description"
        )
    ]
    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="category like mobiles/Electronics",
            examples=["mobile", "laptop"]
        )
    ]
    brand: Annotated[
        str,
        Field(
            min_length=3,
            max_length=40,
            examples=["Amazfit", "Sony"]
        )
    ]
    price: Annotated[
        float,
        Field(
            gt=0,
            strict=True,
            description='base price(PKR)'
        )
    ]
    currency: Literal["USD"] = "USD"
    discount_percent: Annotated[
        int,
        Field(
            ge=0,
            le=90,
            description="discount in percent"

        )
    ] = 0
    stock: Annotated[
        int,
        Field(
            ge=0,
            description="Avaliable stock"
        )
    ]
    rating: Annotated[
        float,
        Field(
            ge=0,
            le=5,
            description="rating out oof 5"
        )
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(
            default=None,
            max_length=10,
            description="Up to 10 tags"
        )
    ]

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value:str):
        if "-" not in value:
            raise ValueError("SKU must have '-' ")

        last = value.split("-")[-1]
        if not (len(last) == 4 and last.isdigit()):
            raise ValueError("SKU must end 4 digit and sequence like 0032")
        return value


    @model_validator(mode="after")
    @classmethod
    def validate_bussiness_rule(cls, mode:Product):
        if mode.stock == 0:
            raise ValueError("if stock is 0")
        if mode.discount_percent > 0 and mode.rating == 0:
            raise ValueError("discount product must have a rating")
        return mode


    @computed_field
    @property
    def final_price(self) ->float:
        return round(self.price * (1 - self.discount_percent / 100),2)




class ProductUpdate(BaseModel):
    sku: Annotated[
        Optional[str],
        Field(
            min_length=6,
            max_length=30,
            title="Stock Keeping Unit",
            description="Unique product SKU"
        )
    ]

    name: Annotated[
        Optional[str],
        Field(
            min_length=3,
            max_length=50,
            title="Product Name",
            description="Readable product name",
            examples=["Smart Watch"]
        )
    ]
    description: Annotated[
        Optional[str],
        Field(
            max_length=200,
            description="Short Product Description"
        )
    ]
    category: Annotated[
        Optional[str],
        Field(
            min_length=3,
            max_length=30,
            description="category like mobiles/Electronics",
            examples=["mobile", "laptop"]
        )
    ]
    brand: Annotated[
        Optional[str],
        Field(
            min_length=3,
            max_length=40,
            examples=["Amazfit", "Sony"]
        )
    ]
    price: Annotated[
        Optional[float],
        Field(
            gt=0,
            strict=True,
            description='base price(PKR)'
        )
    ]
    currency: Literal["USD"] = "USD"
    discount_percent: Annotated[
        Optional[int],
        Field(
            ge=0,
            le=90,
            description="discount in percent"

        )
    ] = 0
    stock: Annotated[
        Optional[int],
        Field(
            ge=0,
            description="Avaliable stock"
        )
    ]
    rating: Annotated[
        Optional[float],
        Field(
            ge=0,
            le=5,
            description="rating out oof 5"
        )
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(
            default=None,
            max_length=10,
            description="Up to 10 tags"
        )
    ]

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value:str):
        if "-" not in value:
            raise ValueError("SKU must have '-' ")

        last = value.split("-")[-1]
        if not (len(last) == 4 and last.isdigit()):
            raise ValueError("SKU must end 4 digit and sequence like 0032")
        return value


    @model_validator(mode="after")
    @classmethod
    def validate_bussiness_rule(cls, mode:Product):
        if mode.stock == 0:
            raise ValueError("if stock is 0")
        if mode.discount_percent > 0 and mode.rating == 0:
            raise ValueError("discount product must have a rating")
        return mode


    @computed_field
    @property
    def final_price(self) ->float:
        return round(self.price * (1 - self.discount_percent / 100),2)




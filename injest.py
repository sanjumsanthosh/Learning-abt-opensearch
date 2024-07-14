


import json
import requests

from pydantic import BaseModel

class ProductModel(BaseModel):
    productName: str
    productDescription: str
    department: str
    product: str
    productMaterial: str

def readFromJSON() -> list[ProductModel]:
    with open('./faker.json') as f:
        data = json.load(f)
        return [ProductModel(**product) for product in data]

def createBulkIndex(products: list[ProductModel]):
    injestionDocs = []
    for i, product in enumerate(products):
        injestionDocs.append({"index": {"_index": "eds-eng-product", "_id": i}})
        injestionDocs.append(product.dict())  # Convert Pydantic model to dict
    return injestionDocs

def pushToOpenSearch(injestDocs: list):
    bulk_data = ""
    for doc in injestDocs:
        bulk_data += json.dumps(doc) + "\n"  # Convert each dict to JSON and add a newline
    endpoint = "http://localhost:9200/_bulk"
    headers = {"Content-Type": "application/x-ndjson"}
    response = requests.post(endpoint, headers=headers, data=bulk_data)
    print(response.json())

def main():
    products = readFromJSON()
    injestDocs = createBulkIndex(products)
    pushToOpenSearch(injestDocs)

if __name__ == '__main__':
    main()
import os
from io import BytesIO
from flask import Flask, render_template
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from openpyxl import load_workbook

load_dotenv()

app = Flask(__name__)

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
blob_name = os.getenv("BLOB_NAME")


@app.route("/")
def home():
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    blob_data = blob_client.download_blob().readall()

    workbook = load_workbook(BytesIO(blob_data))
    sheet = workbook.active

    data = list(sheet.values)

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)

from typing import List

import uvicorn
from fastapi import FastAPI
from torch.utils.data.datapipes.gen_pyi import split_outside_bracket

from ocr_playlist_images import ocr_data
from pydantic import BaseModel, RootModel

app = FastAPI()


class OcrResponse(BaseModel):
    songTitle: str
    artistNames: str


class Base64EncodedImage(BaseModel):
    base64EncodedImage: str


class OcrRequest(BaseModel):
    images: List[Base64EncodedImage]

@app.post("/ocr", response_model=List[OcrResponse])
async def ocr_playlist_images(request_body: OcrRequest):
    responses = []
    for image in request_body.images:
        response = ocr_data(image.base64EncodedImage)
        responses.extend(response)
    return responses


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

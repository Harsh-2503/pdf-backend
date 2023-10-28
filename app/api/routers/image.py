from typing import Union,List
from fastapi import APIRouter
from fastapi import UploadFile
from app.services.image_buffer import convert_single_img_to_pdf,convert_img_to_pdf,convert_images_to_zip,pdf_to_img,delete_img_from_img_list,img_list_to_img_buffer,add_img_to_img_list
from fastapi.responses import StreamingResponse,FileResponse
import time
# from app.models.pdf_add import RequestData


router = APIRouter()

# @router.get("/image/{image_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# @router.post("/image/")
# async def upload_file(file:UploadFile):
#     if file and file.content_type.split('/')[0] == 'image':
#         data = await convert_single_img_to_pdf(file.file)
#         file_name = file.filename.split('.')
#         file_name[-1] = 'pdf'
#         file_name = ".".join(file_name)
#         headers = {'Content-Disposition': f'inline; filename="{file_name}"',"content-type": "application/octet-stream"}
#         return StreamingResponse(data,media_type='application/pdf',headers=headers)
#     else:
#         print("file not found")
#         return

@router.post("/images/")
async def upload_files(files:List[UploadFile]):
    start = time.perf_counter()
    try:
        if files:
            images = []
            for file in files:
                if file.content_type.split('/')[0] != 'image':
                    print("not all provied files are images")
                    return
                images.append(file.file)
            data = await convert_img_to_pdf(images)

            file_name = files[0].filename.split('.')
            file_name[-1] = 'pdf'
            file_name = ".".join(file_name)
            headers = {'Content-Disposition': f'inline; filename="{file_name}"',"content-type": "application/octet-stream"}
            print(round(time.perf_counter() - start,5))
            return StreamingResponse(data,media_type='application/pdf',headers=headers)
        else:
            print("No Files Uploaded")
            return
    except Exception as err:
        print(err)
        return
    

@router.post("/pdf-to-img-zip/")
async def upload_file(file:UploadFile):
    if file and file.content_type.split('/')[0] == 'application':
        data = await convert_images_to_zip(file.file)
        # print(data)
        # file_name = file.filename.split('.')
        # file_name[-1] = 'zip'
        # file_name = ".".join(file_name)
        # headers = {'Content-Disposition': f'inline; filename="{file_name}"'}
        headers={'Content-Disposition': 'attachment; filename="converted_images.zip"'}
        return StreamingResponse(data,media_type='application/zip',headers=headers)
    else:
        print("file not found")
        return


@router.post("/delete-img-from-pdf")
async def delete_pdf_img(file:UploadFile,positions_to_skip:list[int]):
    if file and file.content_type.split('/')[0] == 'application':
        img_list = await pdf_to_img(file.file)
        # new_img_buffer = await img_list_to_img_buffer(img_list,'PNG')
        new_img_list = await delete_img_from_img_list(img_list,positions_to_skip)
        print(len(new_img_list))
        data = await convert_img_to_pdf(new_img_list)
        file_name = "hello.pdf"
        headers = {'Content-Disposition': f'inline; filename="{file_name}"',"content-type": "application/octet-stream"}
        return StreamingResponse(data,media_type='application/pdf',headers=headers)

    

@router.post("/add-img-to-pdf")
async def delete_pdf_img(file:UploadFile,positions_to_add:List[int],img_to_add:List[UploadFile]):
    if file and file.content_type.split('/')[0] == 'application':
        img_list = await pdf_to_img(file.file)
        new_img_list = await add_img_to_img_list(img_list,positions_to_add,img_to_add)
        data = await convert_img_to_pdf(new_img_list)
        file_name = "hello.pdf"
        headers = {'Content-Disposition': f'inline; filename="{file_name}"',"content-type": "application/octet-stream"}
        return StreamingResponse(data,media_type='application/pdf',headers=headers)



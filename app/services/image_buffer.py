from PIL import Image
from io import BytesIO
from fastapi import BackgroundTasks
from pdf2image import convert_from_bytes
from zipfile import ZipFile
import asyncio
from concurrent.futures import ProcessPoolExecutor


async def convert_single_img_to_pdf(img):
    img_io = BytesIO()
    img = Image.open(img)
    img.convert("RGB")
    img.save(img_io,"PDF")
    img_io.seek(0)
    # BackgroundTasks.add_task(img_io.close)
    return img_io


# async def convert_img_to_rgb(img):
#     img = Image.open(BytesIO(img)).convert("RGB")
#     return img


# def convert_img_to_rgb(img):
#     with Image.open(img) as img:
#         img.convert("RGB")
#     return img


# async def convert_img_to_pdf(images):
#     img_io = BytesIO()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         first_image = executor.submit(convert_img_to_rgb,images.pop(0)).result()
#         img_list = []
#         if images:
#             img_threads = [executor.submit(convert_img_to_rgb,img) for img in images]
#             for rgb_img in concurrent.futures.as_completed(img_threads):
#                 img_list.append(rgb_img.result())        
#     first_image.save(img_io,"PDF",save_all=True, append_images=img_list)
#     img_io.seek(0)
#     return img_io






# asyncio

# def convert_img_to_rgb(img):
#     with Image.open(img) as img:
#         img.convert("RGB")
#         return img

# async def convert_img_to_pdf(images):
#     img_io = BytesIO()
#     with ProcessPoolExecutor() as pool:
#         # first_image = await convert_img_to_rgb(images.pop(0))
#         first_image = await asyncio.to_thread(pool,convert_img_to_rgb,images.pop(0))
#         img_list = []
#         if images:
#             img_list = [await convert_img_to_rgb(img) for img in images]
#         first_image.save(img_io,"PDF",save_all=True, append_images=img_list)
#         img_io.seek(0)
#     return img_io





        
# def convert_img_to_rgb(img):
#     with Image.open(img) as img:
#         img.convert("RGB")
#         return img

# async def convert_img_to_pdf(images):
#     img_io = BytesIO()
#     # with Pool(processes=4) as pool:
#     with Pool(processes=4) as pool:
#         # first_image = await convert_img_to_rgb(images.pop(0))
#         first_image = pool.map(convert_img_to_rgb,images.pop(0))
#         img_list = []
#         if images:
#             # img_list = [await convert_img_to_rgb(img) for img in images]
#             img_list = pool.map(convert_img_to_rgb,images)
#     first_image[0].save(img_io,"PDF",save_all=True, append_images=img_list)
#     img_io.seek(0)
#     return img_io



async def convert_img_to_rgb(img):
    if type(img) == bytes:
        img = Image.open(BytesIO(img)).convert("RGB")
        return img
    with Image.open(img) as img:
        img.convert("RGB")
        return img
    

async def convert_img_to_pdf(images):
    img_io = BytesIO()
    first_image = await convert_img_to_rgb(images.pop(0))
    img_list = []
    if images:
        img_list = [await convert_img_to_rgb(img) for img in images]
    first_image.save(img_io,"PDF",save_all=True, append_images=img_list)
    img_io.seek(0)
    return img_io


async def pdf_to_img(pdf):
    pdf_data = pdf.read()
    img_list = convert_from_bytes(pdf_data,dpi=300)
    return img_list


async def img_list_to_img_buffer(img_list,format:str):
    img_buffer = []
    for img in img_list:
        img_io = BytesIO()
        img.save(img_io,format)
        img_io.seek(0)
        img_buffer.append(img_io.getvalue())
    return img_buffer


async def delete_img_from_img_list(img_list,positions_to_skip:list[int]):
    img_buff_list = await img_list_to_img_buffer(img_list,'PNG')
    img_buff_list = [img for i,img in enumerate(img_buff_list) if i not in positions_to_skip]
    return img_buff_list


async def add_img_to_img_list(img_list,positions_to_add:int,img_to_add):
    img_buff_list = await img_list_to_img_buffer(img_list,'PNG')
    for i in range(1,len(img_buff_list)):
        if i in positions_to_add:
            img_io = BytesIO()
            data = Image.open(img_to_add[i-1].file)
            data.save(img_io,'PNG')
            img_buff_list.insert(i,img_io.getvalue())

    return img_buff_list


async def convert_images_to_zip(pdf):
    img_list= await pdf_to_img(pdf)
    zip_io = BytesIO()
    with ZipFile(zip_io,"w") as zip_archive:
        img_buff_list = await img_list_to_img_buffer(img_list,"PNG")
        for i, img in enumerate(img_buff_list):
            zip_archive.writestr(f"{i+1}.png",img)

    zip_io.seek(0)
    return zip_io

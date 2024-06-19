from sentence_transformers import SentenceTransformer
import os
from pinecone import Pinecone
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import json
from PIL import Image
from dotenv import load_dotenv
import io
from PIL.ExifTags import TAGS
from datetime import datetime
import time

model = SentenceTransformer("clip-ViT-L-14")

dir = 'Gallery'

load_dotenv()
pc = Pinecone(os.getenv("pinecone_key"))
index = pc.Index("multimodalsearch")

filelist = os.listdir(dir)
filenames = "filenames.json"

def get_exif_creation_date(filepath):
    image = Image.open(filepath)
    exif_data = image._getexif()
    if exif_data:
        for tag, value in exif_data.items():
            if TAGS.get(tag) == 'DateTimeOriginal':
                return value
    return None
def convert_to_timestamp(date_str: str) -> int:
    return int(time.mktime(datetime.strptime(date_str, "%Y-%m-%d").timetuple()))

def convert_exif_to_timestamp(exif_date: str) -> int:
    try:
        dt = datetime.strptime(exif_date, '%Y:%m:%d %H:%M:%S')
        return int(time.mktime(dt.timetuple()))
    except ValueError:
        return None

def addfiles(files:str, filelist:list):
    upsertfiles = list()
    try:
        with open(files, 'r') as file:
            sett = set(json.load(file))
    except json.JSONDecodeError:
        sett = set()
    for f in filelist:
        if f not in sett:
           upsertfiles.append(f)
           sett.add(f)
    with open(files, 'w') as file:
        json.dump(list(sett), file)
    return upsertfiles

def text_query(query: str, start_date: str, end_date: str, k=3):
    start_timestamp = convert_to_timestamp(start_date)
    end_timestamp = convert_to_timestamp(end_date)
    query_embedding = model.encode(query).tolist() 

    response = index.query(
        namespace="hehe",
        vector=query_embedding,
        top_k=k,
        filter={
            "date": {"$gte": start_timestamp, "$lte": end_timestamp}
        },
        include_values=True,
        include_metadata=True
    )
    return response

def image_query(query, start_date: str, end_date: str, k=3):
    data = query.read()
    image_stream = io.BytesIO(data)
    query_embedding = model.encode(Image.open(image_stream)).tolist() 
    start_timestamp = convert_to_timestamp(start_date)
    end_timestamp = convert_to_timestamp(end_date)

    response = index.query(
        namespace="hehe",
        vector=query_embedding,
        top_k=k,
        filter={
            "date": {"$gte": start_timestamp, "$lte": end_timestamp}
        },
        include_values=True,
        include_metadata=True
    )
    return response

def upsert(upsertfiles: list) -> None:
    for filename in upsertfiles:
        filepath = os.path.join(dir, filename)
        embedding = model.encode(Image.open(filepath)).tolist()  
        exif_date = get_exif_creation_date(filepath)
        if exif_date:
            creation_timestamp = convert_exif_to_timestamp(exif_date)
            metadata = {"date": creation_timestamp}
        else:
            metadata = {}

        index.upsert(
            vectors=[(filename, embedding, metadata)],  
            namespace="hehe"
        )

def upload()->None:
    print("Upsertion initiated")
    upsert(addfiles(filenames, filelist))
    print("Upsertion completed.")

def delete()->None:
    index.delete(delete_all=True, namespace="hehe")
    settt = set()
    with open(filenames, 'w') as file:
        json.dump(list(settt), file)
    print("deleted all files")



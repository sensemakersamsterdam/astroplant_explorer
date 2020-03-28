# -*- coding: utf-8 -*-
"""Access data in Minio"""

from minio import Minio
from minio.error import ResponseError
import credentials

minio_host = credentials.my_minio_host
minio_access_key = credentials.my_minio_access_key
minio_secret_key = credentials.my_minio_secret_key

minioClient = Minio(minio_host,
                    access_key=minio_access_key,
                    secret_key=minio_secret_key,
                    secure=True)

try:
    res = minioClient.fput_object('astroplant',
                                  'images/image0001.jpg',
                                  './images/image0001.jpg',
                                  content_type='image/jpeg')
    print(res)
    
except ResponseError as err:
    print(err)
                                  
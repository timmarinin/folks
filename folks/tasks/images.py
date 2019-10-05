import datetime
import os
import pathlib
import functools
import mimetypes
from uuid import uuid4
from PIL import Image
import boto3
import botocore
import mimetypes
mimetypes.init()

from .celery import app, logger
from celery import group
from config import Config

S3_ENDPOINT = Config.S3_ENDPOINT
S3_ACCESS_KEY = Config.S3_KEY
S3_SECRET_ACCESS_KEY = Config.S3_SECRET

s3 = boto3.client(
    's3',
    endpoint_url='https://{}'.format(S3_ENDPOINT),
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
)


def to_url(bucket, name):
    return "https://{}.{}/{}".format(bucket, S3_ENDPOINT, name)


@app.task()
def upload_workflow(path):
    """
    Gets image as uploaded and rotates, uploads, and generates thumbnails
    """
    rotate_according_to_exif(path)
    upload = upload_to_s3.delay(path, 'folks-images')
    thumbnails = generate_thumbnails(path, 'folks-thumbnails')
    Path(path).unlink()


def rotate_according_to_exif(file_path):
    """
    Rotates image to proper orientation according to EXIF metadata
    """
    tag = 0x0112
    im = Image.open(file_path)
    if not has_attr(im, '_getexif'):
        return

    exif = im._getexif()
    orientation = exif[tag]
    if orientation is not None:
        exif_transpose_sequences = [[],                # 0    (reserved)
                                    [],                                        # 1   top      left
                                    # 2   top      right
                                    [Image.FLIP_LEFT_RIGHT],
                                    # 3   bottom   right
                                    [Image.ROTATE_180],
                                    # 4   bottom   left
                                    [Image.FLIP_TOP_BOTTOM],
                                    # 5   left     top
                                    [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
                                    # 6   right    top
                                    [Image.ROTATE_270],
                                    # 7   right    bottom
                                    [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],
                                    # 8   left     bottom
                                    [Image.ROTATE_90],
                                    ]
        logger.info('Image {} was captured with orientation {}',
                    file_path, orientation)
        seq = exif_transpose_sequences[orientation]
        im = functools.reduce(type(im).transpose, seq, im)
        im.save()


@app.task(bind=True)
def upload_to_s3(self, file_path, bucket, acl="public-read"):
    """
    Upload file to S3
    """
    fp = pathlib.Path(file_path)
    content_type, enc = mimetypes.guess_type(fp.name)
    if enc is not None:
        logger.error('tried to upload {} (originally {})'.format(enc, fp.name))
        return None
    name = fp.name
    logger.info('uploading {} to {} with ContentType {}'.format(
        name, bucket, content_type))
    try:
        with fp.open('rb') as f:
            s3.upload_fileobj(
                f,
                bucket,
                name,
                ExtraArgs={"ACL": acl, "ContentType": content_type},
            )
    except Exception as exc:
        logger.error(exc)
        raise self.retry(exc=exc)
    return to_url(bucket, name)


@app.task
def generate_thumbnails(file_path, bucket):
    """Generate thumbnails (1600px, 640px, 320px)"""
    fp = pathlib.Path(file_path)
    sizes = [
        (1600, 1600),
        (640, 640),
        (320, 320)
    ]
    im = Image.open(file_path)
    thumb_paths = []
    for s in sizes:
        thumb_name = fp.with_name('{}-{}.jpg'.format(fp.stem, s[0]))
        logger.info("thumb name of {} is {}".format(s, thumb_name))
        im.thumbnail(s, Image.ANTIALIAS)
        im.save(thumb_name, "JPEG")
        thumb_paths.append(str(thumb_name))
    return group(upload_to_s3.s(p, bucket) for p in thumb_paths).apply_async()

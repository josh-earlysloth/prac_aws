import pdb
import boto3
from settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME


class S3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def upload(self, path, name):
        try:
            self.s3_client.upload_file(
                path,
                AWS_STORAGE_BUCKET_NAME,
                name,
            )
            return

        except:
            return None

    def download(self, name, path):
        try:
            self.s3_client.download_file(
                AWS_STORAGE_BUCKET_NAME,
                name,
                path,
            )
            return

        except:
            return None

    def getlist(self, **kwargs):  # MaxKeys=5, Prefix='file'
        continuation_token = None

        while True:
            param = dict(kwargs)  # MaxKeys=5, Prefix='file' // 딕셔너리에 딕셔너리를 씌우면 변화 없음

            if continuation_token:
                param['ContinuationToken'] = continuation_token
            # print(param)
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, **param)
            print(response['Contents'])
            continuation_token = response.get('NextContinuationToken')

            if not response['IsTruncated']:
                break

    def is_object(self, key):
        response = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
        return True if response else False

    def delete(self, file):
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=file)
        return


josh_s3 = S3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)

# josh_s3.upload('test.docx', 'test.docx')
# josh_s3.upload('test2.png', 'test2.png')
# josh_s3.delete('test.docx')
# josh_s3.download('test2.png', '/Users/byeongyeonjung/Dev/aws_prac/downloads/test2.png')

# print(josh_s3.getlist())  # 반환되는 값은 딕셔너리로, ['Content']를 key로 하여 S3 object 리스트를 조회할 수 있다
# print(josh_s3.is_object('test2.png'))
print(josh_s3.getlist(MaxKeys=2, Prefix='file'))


# print(josh_s3.getlist())

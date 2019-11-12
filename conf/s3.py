from pprint import pprint
import boto3
import json
import pickle
from SceneTalker.settings.production import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_REGION_NAME


class S3:
    def __init__(self, region_name=None, aws_access_key_id=None, aws_secret_access_key=None):
        self.s3 = boto3.resource('s3',
                                 region_name=region_name and region_name or AWS_S3_REGION_NAME,
                                 aws_access_key_id=aws_access_key_id and aws_access_key_id or AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=aws_secret_access_key and aws_secret_access_key or AWS_SECRET_ACCESS_KEY)

    def get_bucket(self, name):
        return self.s3.Bucket(name)

    def get_bucket_list(self):
        return [bucket.name for bucket in self.s3.buckets.all()]

    def get_objects_list(self, bucket_name):
        return [_object.key for _object in self.s3.Bucket(bucket_name).objects.all()]

    def iter_filter_object(self, bucket_name, prefix):
        print('prefix:', prefix)
        return self.s3.Bucket(bucket_name).objects.filter(Prefix=prefix)

    def has_object(self, bucket_name, obj_path):
        for s3_path in self.s3.Bucket(bucket_name).objects.filter(Prefix=obj_path):
            if s3_path.key == obj_path:
                return True
        return False

    def get_object(self, bucket_name, obj_path):
        assert self.has_object(bucket_name, obj_path), '해당 파일을 찾을 수 없습니다.'

        obj = self.s3.Object(bucket_name, obj_path)
        obj_type = obj.key.split('/')[-1].split('.')[-1]

        # TODO 현재는 json 파일만 읽어오는 형태
        if obj_type == 'json':
            try:
                obj_content = obj.get()['Body'].read().decode('utf-8')
                return json.loads(obj_content)
            except UnicodeDecodeError:
                obj_content = obj.get()['Body'].read()
                return pickle.loads(obj_content)
        elif obj_type in ['png', 'jpg']:
            return f'https://{bucket_name}.s3.ap-northeast-2.amazonaws.com/{obj.key}'
        else:
            raise Exception('지원되지 않는 파일 형식입니다.')

    def download_file(self, bucket_name, obj_path, save_path):
        assert self.has_object(bucket_name, obj_path), '해당 파일을 찾을 수 없습니다.'

        self.s3.Bucket(bucket_name).download_file(obj_path, save_path)

    def create_bucket(self, name, region_name=AWS_S3_REGION_NAME):
        self.s3.create_bucket(Bucket=name, CreateBucketConfiguration={'LocationConstraint': region_name})

    def upload_file(self, bucket_name, file_path, save_path, access='public-read'):
        '''
        private : 소유자는 FULL_CONTROL을 가집니다. 다른 누구도 액세스 권한이 없습니다(기본).
        public-read : 소유자는 FULL_CONTROL을 가집니다. AllUsers 그룹은(피부여자란? 참조) READ 액세스 권한을 가집니다. 퍼블릭액세스가 된다.
        '''
        self.s3.Bucket(bucket_name).upload_file(file_path, save_path, ExtraArgs={'ACL': access})

    def put_object(self, bucket_name, obj, save_path):
        self.s3.Bucket(bucket_name).put_object(Key=save_path, Body=obj)


if __name__ == '__main__':
    s3 = S3()

    # s3.put_object('qaster-namu', json.dumps({'hi': 'bye'}), 'alba/data2.json')
    # print(s3.has_object(bucket_name='qaster-namu', obj_path='adbrix/33ddf4941fe60dd550794ae7d676feb965de062e8dfd65467a1e4cc5d8e6dafb/data.json'))
    # print(s3.get_objects_list('qaster-cache'))
    # print(s3.get_object('qaster-cache', 'test/스크린샷 2019-11-06 오전 11.59.33.png'))
    print(s3.get_bucket_list())

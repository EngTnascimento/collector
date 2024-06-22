import json
from io import BytesIO

from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

from .minio import MinioStorage


class MinioPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        self.minio = MinioStorage()
        self.bucket_name = settings.get("MINIO_BUCKET_NAME")
        self.minio.create_bucket(self.bucket_name)

    def process_item(self, item, spider):
        if not item:
            raise DropItem("Missing item data")

        item_data = json.dumps(dict(item)).encode("utf-8")
        item_key = f"{spider.name}/{item['id']}.json"  # Customize this key as needed

        self.minio.upload(
            bucket_name=self.bucket_name, object_name=item_key, data=BytesIO(item_data)
        )
        spider.logger.info(f"Item saved to Minio: {item_key}")
        return item

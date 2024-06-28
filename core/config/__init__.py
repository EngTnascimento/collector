from .logging import LoggingSettings
from .main import MainSettings
from .scrapy import ScrapySettings
from .secret import MinioSettings

main_settings = MainSettings()
minio_settings = MinioSettings()
logging_settings = LoggingSettings()
scrapy_settings = ScrapySettings()

from .resume_crud import ResumeCrud
from .media_crud import MediaCrud
from models import (Resume, Media)

resume = ResumeCrud(Resume)
media = MediaCrud(Media)

from .resume_crud import ResumeCrud, CertificateBlockCrud
from .media_crud import MediaCrud
from models import (Resume, Media, CertificateBlock)

resume = ResumeCrud(Resume)
media = MediaCrud(Media)
certificate = CertificateBlockCrud(CertificateBlock)

from .resume_crud import ResumeCrud
from .certificate_crud import CertificateBlockCrud
from .skill_crud import SkillBlockCrud
from .media_crud import MediaCrud
from models import (Resume, Media, CertificateBlock, SkillBlock)

resume = ResumeCrud(Resume)
media = MediaCrud(Media)
certificate = CertificateBlockCrud(CertificateBlock)
skill = SkillBlockCrud(SkillBlock)

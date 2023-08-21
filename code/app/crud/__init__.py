from .resume_crud import ResumeCrud
from .certificate_crud import CertificateBlockCrud
from .skill_crud import SkillBlockCrud
from .media_crud import MediaCrud
from .sphere_crud import SphereCrud
from .profession_crud import ProfessionCrud
from models import (Resume, Media, CertificateBlock, SkillBlock, Sphere, Profession)

resume = ResumeCrud(Resume)
media = MediaCrud(Media)
certificate = CertificateBlockCrud(CertificateBlock)
skill = SkillBlockCrud(SkillBlock)
sphere = SphereCrud(Sphere)
profession = ProfessionCrud(Profession)

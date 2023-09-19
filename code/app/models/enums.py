import enum


class TokenType(str, enum.Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


# class LanguageLevelEnum(str, enum.Enum):
#     BEGINNER = "beginner"
#     INTERMEDIATE = "intermediate"
#     PROFICIENT = "proficient"
#     FLUENT = "fluent"
#     NATIVE = "native"
#
#
# class SkillLevelEnum(str, enum.Enum):
#     NOVICE = "novice"
#     BEGINNER = "beginner"
#     SKILLFUL = "skillful"
#     EXPERIENCED = "experienced"
#     EXPERT = "expert"

class ResumeStatusEnum(str, enum.Enum):
    PUBLISH = "publish"
    DRAFT = "draft"
    PENDING = "pending"
    PRIVATE = "private"
    TRASH = "trash"
    REJECT = 'reject'


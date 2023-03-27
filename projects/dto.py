from typing import NamedTuple
from .models import Link
from users.models import Skill


class SkillType(NamedTuple):
    skills: list[Skill]


class LinkType(NamedTuple):
    links: list[Link]


class SkillLinkType(NamedTuple):
    skills_data: SkillType
    links_data: LinkType

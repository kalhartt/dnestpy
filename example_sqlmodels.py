#!/usr/bin/python2.7
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

dbPath = 'dnt.db'
engine = sqla.create_engine('sqlite:///%s' % dbPath)
Base = declarative_base(engine)

class UIString(Base):
    __tablename__ = 'UISTRING'
    __table_args__ = {'autoload':True}

    def __str__(self):
        return self._Message

    def __repr__(self):
        return '<UISTRING(%d %s)>' % (self.id, self._Message)


class Job(Base):
    __tablename__ = 'JOBTABLE'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_JobName'],['UISTRING.id']),
            sqla.ForeignKeyConstraint(['_JobDescriptionID'],['UISTRING.id']),
            sqla.ForeignKeyConstraint(['_ParentJob'],['JOBTABLE.id']),
            {'autoload':True})

    job_name = relationship('UIString', primaryjoin = 'JOBTABLE.c._JobName == UISTRING.c.id')
    job_description = relationship('UIString', primaryjoin = 'JOBTABLE.c._JobDescriptionID == UISTRING.c.id')
    parent_job = relationship('Job', primaryjoin = 'JOBTABLE.c._ParentJob == JOBTABLE.c.id')

    def __str__(self):
        return self.job_name._Message

class Skill(Base):
    __tablename__ = 'SKILLTABLE_CHARACTER'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_NameID'],['UISTRING.id']),
            sqla.ForeignKeyConstraint(['_NeedJob'],['JOBTABLE.id']),
            sqla.ForeignKeyConstraint(['_BaseSkillID'],['SKILLTABLE_CHARACTER.id']),
            {'autoload':True})

    name = relationship('UIString', primaryjoin = 'SKILLTABLE_CHARACTER.c._NameID == UISTRING.c.id')
    need_job = relationship('Job', primaryjoin = 'SKILLTABLE_CHARACTER.c._NeedJob == JOBTABLE.c.id')
    base_skill = relationship('Skill', primaryjoin = 'SKILLTABLE_CHARACTER.c._BaseSkillID == SKILLTABLE_CHARACTER.c.id')

    def __str__(self):
        return self.name._Message

class SkillTree(Base):
    __tablename__ = 'SKILLTREETABLE'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillTableID'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_ParentSkillID1'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_ParentSkillID2'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_ParentSkillID3'],['SKILLTABLE_CHARACTER.id']),
            {'autoload':True})
    
    skill = relationship('Skill', primaryjoin = 'SKILLTREETABLE.c._SkillTableID == SKILLTABLE_CHARACTER.c.id')
    parent_skill1 = relationship('Skill', primaryjoin = 'SKILLTREETABLE.c._ParentSkillID1 == SKILLTABLE_CHARACTER.c.id')
    parent_skill2 = relationship('Skill', primaryjoin = 'SKILLTREETABLE.c._ParentSkillID2 == SKILLTABLE_CHARACTER.c.id')
    parent_skill3 = relationship('Skill', primaryjoin = 'SKILLTREETABLE.c._ParentSkillID3 == SKILLTABLE_CHARACTER.c.id')

    def __str__(self):
        return self.skill.name._Message

class SkillLevelAcademic(Base):
    __tablename__ = 'SKILLLEVELTABLE_CHARACTERACADEMIC'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillIndex'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_SkillExplanationID'],['UISTRING.id']),
            {'autoload':True})

    skill = relationship('Skill', primaryjoin = 'SKILLLEVELTABLE_CHARACTERACADEMIC.c._SkillIndex == SKILLTABLE_CHARACTER.c.id')
    skill_explanation = relationship('UIString', primaryjoin = 'SKILLLEVELTABLE_CHARACTERACADEMIC.c._SkillExplanationID == UISTRING.c.id')

    def __str__(self):
        return self.skill.name._Message

class SkillLevelArcher(Base):
    __tablename__ = 'SKILLLEVELTABLE_CHARACTERARCHER'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillIndex'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_SkillExplanationID'],['UISTRING.id']),
            {'autoload':True})

    skill = relationship('Skill', primaryjoin = 'SKILLLEVELTABLE_CHARACTERARCHER.c._SkillIndex == SKILLTABLE_CHARACTER.c.id')
    skill_explanation = relationship('UIString', primaryjoin = 'SKILLLEVELTABLE_CHARACTERARCHER.c._SkillExplanationID == UISTRING.c.id')

    def __str__(self):
        return self.skill.name._Message

class SkillLevelCleric(Base):
    __tablename__ = 'SKILLLEVELTABLE_CHARACTERCLERIC'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillIndex'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_SkillExplanationID'],['UISTRING.id']),
            {'autoload':True})

    skill = relationship('Skill', primaryjoin = 'SKILLLEVELTABLE_CHARACTERCLERIC.c._SkillIndex == SKILLTABLE_CHARACTER.c.id')
    skill_explanation = relationship('UIString', primaryjoin = 'SKILLLEVELTABLE_CHARACTERCLERIC.c._SkillExplanationID == UISTRING.c.id')

    def __str__(self):
        return self.skill.name._Message

class SkillLevelEtc(Base):
    __tablename__ = 'SKILLLEVELTABLE_CHARACTERETC'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillIndex'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_SkillExplanationID'],['UISTRING.id']),
            {'autoload':True})

    skill = relationship('Skill', primaryjoin = 'SKILLLEVELTABLE_CHARACTERETC.c._SkillIndex == SKILLTABLE_CHARACTER.c.id')
    skill_explanation = relationship('UIString', primaryjoin = 'SKILLLEVELTABLE_CHARACTERETC.c._SkillExplanationID == UISTRING.c.id')

    def __str__(self):
        return self.skill.name._Message

class SkillLevelKali(Base):
    __tablename__ = 'SKILLLEVELTABLE_CHARACTERKALI'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillIndex'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_SkillExplanationID'],['UISTRING.id']),
            {'autoload':True})

    skill = relationship('Skill', primaryjoin = 'SKILLLEVELTABLE_CHARACTERKALI.c._SkillIndex == SKILLTABLE_CHARACTER.c.id')
    skill_explanation = relationship('UIString', primaryjoin = 'SKILLLEVELTABLE_CHARACTERKALI.c._SkillExplanationID == UISTRING.c.id')

    def __str__(self):
        return self.skill.name._Message

class SkillLevelSorceress(Base):
    __tablename__ = 'SKILLLEVELTABLE_CHARACTERSOCERESS'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillIndex'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_SkillExplanationID'],['UISTRING.id']),
            {'autoload':True})

    skill = relationship('Skill', primaryjoin = 'SKILLLEVELTABLE_CHARACTERSOCERESS.c._SkillIndex == SKILLTABLE_CHARACTER.c.id')
    skill_explanation = relationship('UIString', primaryjoin = 'SKILLLEVELTABLE_CHARACTERSOCERESS.c._SkillExplanationID == UISTRING.c.id')

    def __str__(self):
        return self.skill.name._Message

class SkillLevelWarrior(Base):
    __tablename__ = 'SKILLLEVELTABLE_CHARACTERWARRIOR'
    __table_args__ = (
            sqla.ForeignKeyConstraint(['_SkillIndex'],['SKILLTABLE_CHARACTER.id']),
            sqla.ForeignKeyConstraint(['_SkillExplanationID'],['UISTRING.id']),
            {'autoload':True})

    skill = relationship('Skill', primaryjoin = 'SKILLLEVELTABLE_CHARACTERWARRIOR.c._SkillIndex == SKILLTABLE_CHARACTER.c.id')
    skill_explanation = relationship('UIString', primaryjoin = 'SKILLLEVELTABLE_CHARACTERWARRIOR.c._SkillExplanationID == UISTRING.c.id')

    def __str__(self):
        return self.skill.name._Message

if __name__ == '__main__':
    metadata = Base.metadata
    session = sessionmaker(bind=engine)()
    
    job_name = 'WARRIOR'
    job_class = SkillLevelWarrior
    job = session.query(Job).filter(Job._EnglishName == job_name).one()

    job_skills = session.query(Skill).filter(Skill._NeedJob == job.id).all()
    for skill in job_skills:
        skilltree = session.query(SkillTree).filter(SkillTree._SkillTableID == skill.id).one()
        print skill, skilltree._TreeSlotIndex, skill._IconImageIndex

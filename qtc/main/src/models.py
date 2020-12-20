from abc import abstractmethod
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Table
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import backref, relation, relationship, sessionmaker
from sqlalchemy.sql.operators import nullslast_op
from datetime import datetime, timedelta
from dataclasses import dataclass
import orjson
from orjson import OPT_INDENT_2, dumps as jsonify


def to_json(obj) -> str:
    return orjson.dumps(obj, option=OPT_INDENT_2).decode('utf8')


class Entity(object):

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)

    @abstractmethod
    def json(self) -> str:
        pass


Model = declarative_base(cls=Entity)

participation_table = Table(
    'participation',
    Model.metadata,
    Column('course_id', Integer, ForeignKey('course.id')),
    Column('member_id', Integer, ForeignKey('member.id'))
)


@dataclass
class Member(Model):
    name = Column(String(80), nullable=False)
    is_moderator = Column(Boolean, nullable=False)
    is_owner = Column(Boolean, nullable=False)
    total_donation = Column(Integer, nullable=False)

    active_courses = relationship('Course', secondary=participation_table, backref='participants', lazy=True)


@dataclass
class SourceLanguage(Model):
    title = Column(String(10), nullable=False)
    is_compiled = Column(Boolean, nullable=False)
    compile_command = Column(String(100), nullable=True)
    execution_command = Column(String(100), nullable=False)
    source_extension = Column(String(10), nullable=False)
    compiled_extension = Column(String(10), nullable=True)


@dataclass
class Course(Model):
    title = Column(String(30), nullable=False)
    description = Column(String(100))
    creation_time = Column(DateTime, nullable=False)
    password = Column(String(100), nullable=False)

    creator_id = Column(Integer, ForeignKey('member.id'), nullable=False)

    creator = relationship('Member', backref='created_courses', lazy=True)


@dataclass
class Assignment(Model):
    title = Column(String(30), nullable=False)
    creation_time = Column(DateTime, nullable=False)
    deadline = Column(DateTime, nullable=False)

    admin_id = Column(Integer, ForeignKey('member.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)

    admin = relationship('Member', backref='administrations', lazy=True)
    course = relationship('Course', backref='assignments', lazy=True)


@dataclass
class Problem(Model):
    title = Column(String(30), nullable=False)
    has_bible = Column(Boolean, nullable=False)

    assignment_id = Column(Integer, ForeignKey('assignment.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    bible_language_id = Column(Integer, ForeignKey('language.id'), nullable=False)
    solver_id = Column(Integer, ForeignKey('member.id'), nullable=True)

    assignment = relationship('Assignment', backref='problems', lazy=True)
    course = relationship('Course', backref='problems', lazy=True)
    bible_language = relationship('SourceLanguage', backref='problems', lazy=True)
    solver = relationship('Member', backref='solved_problems', lazy=True)


@dataclass
class Case(Model):
    description = Column(String(100), nullable=True)

    assignment_id = Column(Integer, ForeignKey('assignment.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    problem_id = Column(Integer, ForeignKey('problem.id'), nullable=False)
    submitter_id = Column(Integer, ForeignKey('member.id'), nullable=False)

    assignment = relationship('Assignment', backref='cases', lazy=True)
    course = relationship('Course', backref='cases', lazy=True)
    problem = relationship('Problem', backref='cases', lazy=True)
    submitter = relationship('Member', backref='submitted_cases', lazy=True)


@dataclass
class Hint(Model):
    text = Column(String(200), nullable=True)
    level = Column(Integer, nullable=False)

    assignment_id = Column(Integer, ForeignKey('assignment.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    problem_id = Column(Integer, ForeignKey('problem.id'), nullable=False)
    submitter_id = Column(Integer, ForeignKey('member.id'), nullable=False)

    assignment = relationship('Assignment', backref='hints', lazy=True)
    course = relationship('Course', backref='hints', lazy=True)
    problem = relationship('Problem', backref='hints', lazy=True)
    submitter = relationship('Member', backref='submitted_hints', lazy=True)

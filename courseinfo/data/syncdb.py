# import datetime

# open(r'/root/log.txt', 'a').write(str(datetime.datetime.now()) + '\n')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("oracle+cx_oracle://jw_user:Hdlgdx18@172.20.8.37:1521/orcl")
Base = declarative_base()


class Classroom(Base):
    __tablename__ = 'VIEW_DJZX_CLASSROMM'
    ID = Column(String(100), primary_key=True)
    ROOM_NAME = Column(String(100))
    BUILDING = Column(String(100))
    TYPE = Column(String(100))
    CAMPUS = Column(String(100))


class Course(Base):
    __tablename__ = 'VIEW_DJZX_SCHEDULE'
    JX0404ID = Column(String(100), primary_key=True)
    TERMNAME = Column(String(100))          # 学期（2018-2019-1：18年-19年第一学期；2018-2019-2：18年-19年第二学期；）
    KCMC = Column(String(100))              # 课程名称
    TEACHER_ID = Column(String(100))        # 教师ID
    TEACHER_NAME = Column(String(100))      # 教师姓名
    CLASS_TIME = Column(String(100))        # 上课时间（例如030102，03是周三的课，0102是1-2节，这个字段可以不用，后面有分开的字段
    START_TIME = Column(String(100))        # 上课安排（1-9|全，课程安排是第1周到第9周，全是每周都有，单是单数周有课，双是双数周有课；这个字段可以不用，后面有分开的字段）
    CLASSROOM_NAME = Column(String(100))    # 教室名称
    CLASSROOM_ID = Column(String(100), ForeignKey('VIEW_DJZX_CLASSROMM.ID'))  # 教室ID（对应教室表）
    XQ = Column(Integer)                    # 星期（4就是周四）
    KS = Column(Integer)                    # 开始的课节（01）
    JS = Column(Integer)                    # 结束的课节（04）代表上午01-04节的课
    ZC1 = Column(Integer)                   # 第几周开始课程（01）
    ZC2 = Column(Integer)                   # 第几周结束课程（09）代表课程安排是第1周到第9周
    SJBZ = Column(Integer)                  # 只有0、1、2三个数字，0代表每周都有课，1代表单数周有课，2代表双数周有课
    SHOWTEXT = Column(String(100))          # 备注上课安排

# def init_db():
#     Base.metadata.create_all(engine)

# def drop_db():
#     Base.metadata.drop_all(engine)

# drop_db()
# init_db()


Session = sessionmaker(bind=engine)
session = Session()

# #往team表里插入两条数据
# session.add(Team(caption='dba'))
# session.add(Team(caption='ddd'))
# # session.add(Team(caption='dd2'))
# session.commit()

# session.add_all([
#     User(name='zzz',team_id=1),
#     User(name='sss',team_id=2),
#     User(name='ccc',team_id=3),
# ])
# session.commit()

ret = session.query(Classroom).all()
print(ret)
# # ret = session.query(User.name).filter(User.name=='zzz').all()
# obj = ret[0]
# print(ret, obj, obj.name)

# # 等价于SELECT user.name AS FROM user INNER JOIN team ON team.tid = user.team_id
# ret = session.query(User.name, Team.caption).join(Team).all()
# print(ret)

# ret = session.query(User.name, Team.caption).join(Team,isouter=True).all()
# print(ret)

# ret = session.query(User).all()
# for obj in ret:
#     print(obj.nid,obj.name, 
#           obj.favor,
#           obj.favor.tid if obj.favor else None,
#           obj.favor.caption if obj.favor else None)

# ret = session.query(Team).filter(Team.caption == 'dba').all()
# print(ret[0].tid)
# print(ret[0].caption)
# print(ret[0].user)
from enum import Enum
class Gender(Enum):
    male='male'
    female='female'
class Role(Enum):
    admin='admin'
    user='user'
    ngo_admin='ngo_admin'
class Status(Enum):
    approved='approved'
    rejected='rejected'
    pending='pending'
  
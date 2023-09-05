from peewee import *
from config import db


class Base(Model):
    class Meta:
        database = db


class Project(Base):
    title = CharField(max_length=255, unique=True, index=True)
    created_at = DateTimeField()

    @property
    def active_contracts(self):
        return self.contracts.where(Contract.status=="active")


class Contract(Base):
    STATUSES = [
        [
            "draft",
            "draft",
        ],
        [
            "active",
            "active",
        ],
        ["finished", "finished"],
    ]
    title = CharField(unique=True, index=True, max_length=255)
    created_at = DateTimeField()
    signed_at = DateTimeField(null=True)
    status = CharField(choices=STATUSES)
    project = ForeignKeyField(
        model=Project, backref="contracts", on_delete="CASCADE", null=True
    )

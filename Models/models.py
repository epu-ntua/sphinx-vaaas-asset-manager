import pytz
from mongoengine import StringField, DynamicDocument, DateTimeField, BooleanField, FloatField, IntField, DictField, ListField, ReferenceField, CASCADE, EmbeddedDocument, \
    DynamicEmbeddedDocument, Document, signals
import json
from datetime import datetime
import re

ip_regexp = re.compile('^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$')
mac_regexp = re.compile('^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$')


# def update_modified(sender, document):
#     document.modified = datetime.now(pytz.timezone('Europe/Athens'))


#
# class CPE(DynamicDocument):
#     part = StringField()
#     vendor = StringField()
#     product = StringField()
#     version = StringField()
#     update = StringField()
#     edition = StringField()
#
#
# class Service(DynamicEmbeddedDocument):
#     name = StringField()
#     port = IntField()
#     cpes = ListField(ReferenceField(CPE))


class Asset(DynamicDocument):
    name = StringField()
    hostnames = ListField(StringField())
    description = StringField()
    assetType = StringField()
    assessed = BooleanField(default=False)
    cvss = FloatField(default=0.0)
    Slice = IntField()
    created = DateTimeField(default=datetime.now(pytz.timezone('Europe/Athens')))
    modified = DateTimeField()
    status = BooleanField(default=True)
    sensitivity = IntField(default=0)
    location = StringField()
    owner = StringField()
    backupLocation = StringField()
    services = ListField(DictField())
    assetValue = IntField(default=0)
    vendor = StringField()
    active = BooleanField(default=True)
    ip = StringField(required=True, regex=ip_regexp, unique=True)  # 10.0.0.1
    mac = StringField(regex=mac_regexp, null=True)  # 01:23:45:67:89:AB
    os = DictField()

    # @classmethod
    # def pre_save(cls, sender, document, **kwargs):
    #     # document.modified = datetime.now(pytz.timezone('Europe/Athens'))
    #     pass
    #
    # @classmethod
    # def post_save(cls, sender, document, **kwargs):
    #     print("Post Save: %s" % document.name)
    #     if 'created' in kwargs:
    #         if kwargs['created']:
    #             print("Created")
    #             document.modified = datetime.now(pytz.timezone('Europe/Athens'))
    #         else:
    #             pass
    #     elif 'updated' in kwargs:
    #         if kwargs['updated']:
    #             print("Updated")
    #             document.modified = datetime.now(pytz.timezone('Europe/Athens'))
    #         else:
    #             pass


# signals.pre_save.connect(update_modified)
# signals.pre_save.connect(Asset.pre_save, sender=Asset)
# signals.post_save.connect(Asset.post_save, sender=Asset)

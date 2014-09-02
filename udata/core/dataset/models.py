# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from blinker import Signal
from flask import url_for
from mongoengine.signals import pre_save, post_save

from udata.models import db, WithMetrics, Issue, Follow, SpatialCoverage
from udata.i18n import lazy_gettext as _


__all__ = (
    'License', 'Resource', 'Dataset',
    'DatasetIssue', 'FollowDataset',
    'UPDATE_FREQUENCIES',
)

UPDATE_FREQUENCIES = {
    'punctual': _('Punctual'),
    'realtime': _('Real time'),
    'daily': _('Daily'),
    'weekly': _('Weekly'),
    'fortnighly': _('Fortnighly'),
    'monthly': _('Monthly'),
    'bimonthly': _('Bimonthly'),
    'quarterly': _('Quarterly'),
    'biannual': _('Biannual'),
    'annual': _('Annual'),
    'biennial': _('Biennial'),
    'triennial': _('Triennial'),
    'quinquennial': _('Quinquennial'),
    'unknown': _('Unknown'),
}


class License(db.Document):
    id = db.StringField(primary_key=True)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(required=True)
    slug = db.SlugField(required=True, populate_from='title')
    url = db.URLField()
    maintainer = db.StringField()
    flags = db.ListField(db.StringField())

    active = db.BooleanField()

    def __unicode__(self):
        return self.title


class DatasetQuerySet(db.BaseQuerySet):
    def visible(self):
        return self(private__ne=True, resources__0__exists=True, deleted=None)


class Resource(db.EmbeddedDocument):
    id = db.AutoUUIDField()
    title = db.StringField(verbose_name="Title", required=True)
    description = db.StringField()
    url = db.StringField()
    checksum = db.StringField()
    format = db.StringField()
    owner = db.ReferenceField('User')

    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    modified = db.DateTimeField(default=datetime.datetime.now, required=True)
    published = db.DateTimeField(default=datetime.datetime.now, required=True)
    deleted = db.DateTimeField()

    on_added = Signal()
    on_deleted = Signal()


class Dataset(WithMetrics, db.Datetimed, db.Document):
    title = db.StringField(max_length=255, required=True)
    slug = db.SlugField(max_length=255, required=True, populate_from='title', update=True)
    description = db.StringField(required=True, default='')
    license = db.ReferenceField('License')

    tags = db.ListField(db.StringField())
    resources = db.ListField(db.EmbeddedDocumentField(Resource))
    community_resources = db.ListField(db.EmbeddedDocumentField(Resource))

    private = db.BooleanField()
    owner = db.ReferenceField('User')
    organization = db.ReferenceField('Organization')
    supplier = db.ReferenceField('Organization')

    frequency = db.StringField(choices=UPDATE_FREQUENCIES.keys())
    temporal_coverage = db.EmbeddedDocumentField(db.DateRange)
    spatial = db.EmbeddedDocumentField(SpatialCoverage)

    ext = db.MapField(db.GenericEmbeddedDocumentField())
    extras = db.ExtrasField()

    featured = db.BooleanField(required=True, default=False)

    deleted = db.DateTimeField()

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug', 'organization', 'supplier'],
        'ordering': ['-created_at'],
        'queryset_class': DatasetQuerySet,
    }

    before_save = Signal()
    after_save = Signal()
    on_create = Signal()
    on_update = Signal()
    before_delete = Signal()
    after_delete = Signal()
    on_delete = Signal()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        cls.before_save.send(document)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        cls.after_save.send(document)
        if kwargs.get('created'):
            cls.on_create.send(document)
        else:
            cls.on_update.send(document)

    @property
    def display_url(self):
        return url_for('datasets.show', dataset=self)

    @property
    def image_url(self):
        if self.organization:
            return self.organization.image_url
        else:
            return self.owner.avatar_url

    @property
    def frequency_label(self):
        return UPDATE_FREQUENCIES.get(self.frequency or 'unknown', UPDATE_FREQUENCIES['unknown'])


pre_save.connect(Dataset.pre_save, sender=Dataset)
post_save.connect(Dataset.post_save, sender=Dataset)


class DatasetIssue(Issue):
    subject = db.ReferenceField(Dataset)


class FollowDataset(Follow):
    following = db.ReferenceField(Dataset)

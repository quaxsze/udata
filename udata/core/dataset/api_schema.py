from marshmallow import Schema, fields, validate

resource_fields = api.model('Resource', {
    'id': fields.String(description='The resource unique ID', readonly=True),
    'title': fields.String(description='The resource title', required=True),
    'description': fields.Markdown(
        description='The resource markdown description'),
    'filetype': fields.String(
        description=('Whether the resource is an uploaded file, '
                     'a remote file or an API'),
        required=True, enum=list(RESOURCE_FILETYPES)),
    'type': fields.String(
        description=('Resource type (documentation, API...)'),
        required=True, enum=list(RESOURCE_TYPES)),
    'format': fields.String(description='The resource format', required=True),
    'url': fields.String(description='The resource URL', required=True),
    'latest': fields.String(description='The permanent URL redirecting to '
                            'the latest version of the resource. When the '
                            'resource data is updated, the URL will '
                            'change, the latest URL won\'t.',
                            readonly=True),
    'checksum': fields.Nested(
        checksum_fields, allow_null=True,
        description='A checksum to validate file validity'),
    'filesize': fields.Integer(description='The resource file size in bytes'),
    'mime': fields.String(description='The resource mime type'),
    'created_at': fields.ISODateTime(
        readonly=True, description='The resource creation date'),
    'published': fields.ISODateTime(
        description='The resource publication date'),
    'last_modified': fields.ISODateTime(
        attribute='modified', readonly=True,
        description='The resource last modification date'),
    'metrics': fields.Raw(
        description='The resource metrics', readonly=True),
    'extras': fields.Raw(description='Extra attributes as key-value pairs'),
    'preview_url': fields.String(description='An optional preview URL to be '
                                 'loaded as a standalone page (ie. iframe or '
                                 'new page)',
                                 readonly=True),
})

class ResourceSchema(Schema):
    id = fields.String(description='The resource unique ID', dump_only=True)
    title = fields.String(description='The resource title', required=True),
    description = fields.String(description='The resource markdown description')
    filetype = fields.String(
        description='Whether the resource is an uploaded file, a remote file or an API',
        required=True, validate=validate.OneOf(list(RESOURCE_FILETYPES)))
    type = fields.String(
        description='Resource type (documentation, API...)',
        required=True,
        validate=validate.OneOf(list(RESOURCE_TYPES)))
    format = fields.String(description='The resource format', required=True),
    url = fields.String(description='The resource URL', required=True),
    latest = fields.String(description='The permanent URL redirecting to '
                            'the latest version of the resource. When the '
                            'resource data is updated, the URL will '
                            'change, the latest URL won\'t.',
                            dump_only=True),
    checksum = fields.Nested()
    filesize = fields.Integer(description='The resource file size in bytes')
    mime = fields.String(description='The resource mime type')
    created_at = fields.DateTime(format='iso', description='The resource creation date', dump_only=True)
    published = fields.DateTime(format='iso', description='The resource publication date')
    last_modified = fields.DateTime(format='iso', description='The resource last modification date', dump_only=True)
    metrics = fields.Raw()
    extras = fields.Raw()
    preview_url = fields.Str()


class DatasetSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    acronym = fields.Str()
    slug = fields.Str()
    description = fields.Str()
    created_at = fields.DateTime(format='iso')
    last_modified = fields.DateTime(format='iso')
    deleted = fields.DateTime(format='iso')
    archived = fields.DateTime(format='iso')
    featured = fields.Boolean()
    private = fields.Boolean()
    tags = fields.List()
    badges = fields.List()
    resources = fields.List(fields.Nested(ResourceSchema))
    community_resources = fields.List()
    frequency = fields.Str()
    frequency_date = fields.DateTime(format='iso')
    extras = fields.Raw()
    metrics = fields.Raw()
    organization = fields.Nested()
    owner = fields.Nested()
    temporal_coverage = fields.Nested()
    spatial = fields.Nested()
    license = fields.Str()
    uri = fields.Url()
    page = fields.Url()
    quality = fields.Raw()
    last_update = fields.DateTime(format='iso')

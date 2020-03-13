from udata import entrypoints


def init_app(app):
    # Load all core metrics
    import udata.core.user.metrics  # noqa
    import udata.core.organization.metrics  # noqa
    import udata.core.issues.metrics  # noqa
    import udata.core.discussions.metrics  # noqa
    import udata.core.dataset.metrics  # noqa
    import udata.core.followers.metrics  # noqa
    import udata.core.site.metrics # noqa

    # Load metrics from plugins
    entrypoints.get_enabled('udata.metrics', app)

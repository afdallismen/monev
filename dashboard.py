from django.utils.translation import ugettext_lazy as _

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools_stats.modules import DashboardCharts, get_active_graph


class CustomIndexDashboard(Dashboard):
    columns = 1

    def init_with_context(self, context):
        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('account.*',),
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*', 'account.*', 'admin_tools_stats.*'),
        ))

        # append an app list module
        self.children.append(modules.AppList(
            _('Dashboard Stats Settings'),
            models=('admin_tools_stats.*', ),
        ))

        # Copy following code into your custom dashboard
        # append following code after recent actions module or
        # a link list module for "quick links"
        graph_list = get_active_graph()
        for i in graph_list:
            kwargs = {}
            kwargs['require_chart_jscss'] = True
            kwargs['graph_key'] = i.graph_key

            for key in context['request'].POST:
                if key.startswith('select_box_'):
                    kwargs[key] = context['request'].POST[key]

            self.children.append(DashboardCharts(**kwargs))


class CustomAppIndexDashboard(AppIndexDashboard):
    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        return super(CustomAppIndexDashboard, self).init_with_context(context)

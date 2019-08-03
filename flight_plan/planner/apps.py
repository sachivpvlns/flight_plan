from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlannerConfig(AppConfig):
    name = "flight_plan.planner"
    verbose_name = _("Planner")

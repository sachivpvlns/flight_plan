from django.urls import path

from flight_plan.planner.views import (
    lazy_jack
)

app_name = "planner"
urlpatterns = [
    path("lazy_jack/", view=lazy_jack, name="lazy_jack"),
]

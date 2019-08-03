from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .plan import Plan


@api_view(['POST'])
def lazy_jack(request):
    if request.method == 'POST':
        data = request.data
        key = hash(frozenset(data))

        cache_data = cache.get(key)
        if cache_data is None:
            if 'schedules' in data and 'trip_plan' in data and 'prefered_time' in data:
                plan = Plan(data['schedules'], data['trip_plan']['start_city'], data['trip_plan']['end_city'],
                            data['prefered_time'])
                flight_plan = plan.get_flight_plan()
                response = {"flight_plan": flight_plan}
                cache.set(key, response, timeout=25)
                return Response(response)
        else:
            return Response(cache_data)
    return Response({"message": "Invalid request"})

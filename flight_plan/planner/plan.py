from collections import defaultdict


class Plan:
    """
    The concept of finding the best flight plan is based on finding the shortest path
    in a graph by Djikstra’s shortest path algorithm
    """

    def __init__(self, schedules, start_city, end_city, prefered_time):
        """
        Initialize the graph class
        :param schedules: List of schedules
        :param start_city: Name of the start city
        :param end_city: Name of the end city
        :param prefered_time: Unix time of preferred time to start the trip
        """
        self.schedules = defaultdict(list)
        self.travel_times = {}
        self.start_city = start_city
        self.end_city = end_city
        self.prefered_time = prefered_time

        for schedule in schedules:
            # Consider only timestamps after preferred time
            if schedule['departure']['timestamp'] > prefered_time:
                self.add_schedule(schedule)

    def add_schedule(self, schedule):
        """
        Adds the schedule data into travel_times and schedules
        :param schedule: Schedule of a particular flight
        e.g.
        {
            “departure”: {“city”: “Mumbai”, “timestamp”: 1564561265346 },
            “arrival”: { “city”: “Singapore”, “timestamp”: 1564583044545 }
        },
        :return: None
        """
        key = (schedule['departure']['city'], schedule['arrival']['city'])
        travel_time = schedule['arrival']['timestamp'] - schedule['departure']['timestamp']
        if key not in self.travel_times or travel_time < self.travel_times[key]:
            """
            self.travel_times has all the travel times in Unix format between two cities,
            with the two cities as a tuple as the key
            e.g. {('Mumbai', 'Singapore'): 12345, ('Singapore', 'Sydney'): 234343, ...}
            """
            self.travel_times[(schedule['departure']['city'], schedule['arrival']['city'])] = travel_time
            """
            self.schedules is a dict of all possible next cities
            e.g. {'Mumbai': ['Singapore', 'Sydney'], ...}
            """
            self.schedules[schedule['departure']['city']].append(schedule)

    def get_best_path(self):
        """
         Djikstra’s shortest path algorithm
        :return: List of schedules which define the shortest path
        """
        # shortest paths is a dict of cities
        # whose value is a tuple of (previous city, travel_time)
        shortest_paths = {self.start_city: (None, 0, {})}
        current_city = self.start_city
        visited_cities = set()

        while current_city != self.end_city:
            visited_cities.add(current_city)
            destinations = self.schedules[current_city]
            travel_time_to_current_city = shortest_paths[current_city][1]

            for next_city in destinations:
                travel_time = self.travel_times[
                                  (current_city, next_city['arrival']['city'])] + travel_time_to_current_city
                if next_city['arrival']['city'] not in shortest_paths:
                    shortest_paths[next_city['arrival']['city']] = (current_city, travel_time, next_city)
                else:
                    current_shortest_travel_time = shortest_paths[next_city['arrival']['city']][1]
                    if current_shortest_travel_time > travel_time:
                        shortest_paths[next_city['arrival']['city']] = (current_city, travel_time, next_city)

            next_destinations = {city: shortest_paths[city] for city in shortest_paths if city not in visited_cities}
            if not next_destinations:
                return []
            # next city is the destination with the lowest travel_time
            current_city = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in shortest path
        path = []
        while current_city is not None:
            path.append(shortest_paths[current_city][2])
            next_city = shortest_paths[current_city][0]
            current_city = next_city
        # Reverse path
        path = path[:-1][::-1]
        return path

    def get_flight_plan(self):
        """
        Convert list of schedules into flight path format
        e.g.:
        [
            {
                "city": "Mumbai",
                "timestamp": 1564561265346
            },
            {
                "city": "Singapore",
                "timestamp": 1564583044545
            }
        ]
        :return: Final flight plan
        """
        schedules = self.get_best_path()
        flight_plan = []
        for index, schedule in enumerate(schedules):
            flight_plan.append({
                'city': schedule['departure']['city'],
                'timestamp': schedule['departure']['timestamp']
            })
            if index == len(schedules) - 1:
                flight_plan.append({
                    'city': schedule['arrival']['city'],
                    'timestamp': schedule['arrival']['timestamp']
                })
        return flight_plan

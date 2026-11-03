
class TrafficManager:

    def __init__(self, threshold=50):
        self.threshold = threshold

    def check_congestion(self, vehicle_count):
        if vehicle_count > self.threshold:
            return "High Traffic"
        elif vehicle_count > 20:
            return "Moderate Traffic"
        else:
            return "Low Traffic"

    def suggest_route(self, roads):
        if not roads:
            return None

        return min(
            roads,
            key=lambda road: road["vehicle_count"]
        )

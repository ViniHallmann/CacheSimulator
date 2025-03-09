class Statistics:
    def __init__(self):
        self.misses = {
            "compulsory": 0,
            "capacity": 0,
            "conflict": 0
        }
        self.access = 0
        self.hit = 0

    def increment_compulsory(self):
        self.misses["compulsory"] += 1

    def increment_capacity(self):
        self.misses["capacity"] += 1

    def increment_conflict(self):
        self.misses["conflict"] += 1

    def increment_hit(self):
        self.hit += 1
    
    def increment_access(self):
        self.access += 1

    def get_hit_rate(self):
        return self.hit / self.access
    
    def get_miss_rate(self):
        return 1 - self.get_hit_rate()

    def get_total_misses(self):
        return self.misses["compulsory"] + self.misses["capacity"] + self.misses["conflict"]
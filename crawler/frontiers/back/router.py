class BackQueueRouter:

    def __init__(self):
        self.host_to_queue = dict()

    def get_host_key(self, host_url) -> int:
        hash_key = hash(host_url)
        if hash_key not in self.host_to_queue:
            self.host_to_queue[hash_key] = len(self.host_to_queue)

        return self.host_to_queue[hash_key]

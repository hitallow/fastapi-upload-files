class FakeAwsClient:
    def send_message(self, *params, **kparams):
        pass

    def get_queue_url(self, *params, **kparams):
        pass

    def create_queue(self, *params, **kparams):
        pass

    def receive_message(self, *params, **kparams):
        pass

class FakeAwsClient:
    def send_message(self, *params, **kparams):
        pass

    def get_queue_url(self, *params, **kparams):
        pass

    def create_queue(self, *params, **kparams):
        pass

    def receive_message(self, *params, **kparams):
        pass
    
    def list_buckets(self, *params, **kparams):
        pass
    
    def create_bucket(self, *params, **kparams):
        pass
    
    def get_object(self, *params, **kparams):
        pass

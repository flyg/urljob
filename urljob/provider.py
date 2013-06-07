from data import url_job

# base class for url job provider
class url_job_provider:
    category = "",
    sub_category = ""

    def run_job(self, url_job):
        result = self.run(url_job)
        #post to the server

    # called on the client to run the job
    # child class inherits it to provide the actual logic
    def run(self, url_job):
        return ''

    # called on the server to process result from client
    # child class inherits it to provide the actual logic
    def process_result(self, url_job, result):
        pass
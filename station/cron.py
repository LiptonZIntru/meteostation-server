def cron_update():
    import requests
    requests.post('http://localhost/station/')

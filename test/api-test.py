import requests, json

with open(r'test/test.mp4', 'rb') as finput:
    files = {'file': finput}
    response = requests.post('http://35.222.141.247:8080/od-api/video/', headers={'Content-Disposition':'Content-Disposition: attachment; filename=test.mp4'}, files=files)
    print(response.json())
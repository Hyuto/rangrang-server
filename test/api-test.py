import requests, json
import base64

with open(r'test/test.mp4', 'rb') as finput:
    test = base64.b64encode(finput.read()).decode('utf-8')
    data = json.dumps({'filename' : 'test.mp4', 'video' : test})
    response = requests.post('http://127.0.0.1:8000/od-api/video/', data=data)
    print(response.json())
import requests
  
url = 'http://172.17.0.2:5000/process_image'
image_url = 'https://img1.baidu.com/it/u=4131411748,2639492443&fm=253&app=138&size=w931&n=0&f=JPEG&fmt=auto?sec=1681232400&t=cfa37a0c0d162a83bc31c8fccce22715'

data = {'url': image_url}

try:
    response = requests.post(url, json=data)
    print(response.json())
except ValueError as e:
    print('Error parsing JSON:', e)

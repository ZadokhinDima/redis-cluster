import requests
import time



def main():
    requests.post(url="http://localhost:5000/mykey?value=value")

    while True:
        time.sleep(5)
        response = requests.get("http://localhost:5000/mykey")
        body = response.text
        print(body)

if __name__ == "__main__":
    main()
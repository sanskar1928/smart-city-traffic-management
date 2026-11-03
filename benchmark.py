
import time
import urllib.request

url = "http://127.0.0.1:5000/api/traffic"
requests_count = 100

start = time.perf_counter()
successful = 0

for i in range(requests_count):
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                successful += 1
    except Exception as error:
        print("Request failed:", error)

end = time.perf_counter()

duration = end - start
throughput = successful / duration

print("Successful requests:", successful)
print("Total time:", round(duration, 3), "seconds")
print("Throughput:", round(throughput, 2), "req/sec")

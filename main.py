from requests import request, exceptions
from json import loads
from collections import defaultdict

STAGE = 2
HEADER = {
    "playerid": "410b8eaa-ddfa-494e-9baa-06aa30d05e6f",
    "stage": str(STAGE),
    "Content-Type": "application/x-www-form-urlencoded"
}


def MakeRequest(method: str, url: str, message: str, data: dict = None, headers={}, raw: bool = False, returnError: bool = False):
    if data is None:
        res = request(method=method, url=url, headers=headers)
    else:
        res = request(method=method, url=url, data=data, headers=headers)
    print(f"{res.status_code} | {method} | {url.replace("https://", "").split("/", 1)[0]} | {message}")
    try:
        res.raise_for_status()
        if res.status_code == 200:
            return (res if raw else res.text)
    except exceptions.HTTPError as e:
        if returnError:
            return e
        print(f"URL: {e.response.url}")
        print(f"Response Message: {e.response.text}")
        exit(1)


distanceMatrix  = loads(MakeRequest(
    "GET",
    "http://192.168.131.50:8081/data",
    "Test",
    headers=HEADER
))

visited = [0]
distanceMatrix = {i: {j: distanceMatrix[i][j] for j in range(len(distanceMatrix[i]))} for i in range(len(distanceMatrix))}
while len(visited) < len(distanceMatrix):
    current = visited[-1]
    s = sorted(distanceMatrix[current].items(), key=lambda x: x[1])
    s.pop(0)
    posted = False
    i = 0
    while not posted and i < len(s):
        if s[i][0] not in visited:
            visited.append(s[i][0])
            posted = True
        else: 
            i += 1
solution = visited + [0]

distanceMatrix  = MakeRequest(
    "POST",
    "http://192.168.131.50:8081/answer",
    "Basic Answer",
    data={"route": str(solution)},
    headers=HEADER
)


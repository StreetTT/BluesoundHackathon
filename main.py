from requests import request, exceptions
from json import loads

HEADER = {
    "playerid": "410b8eaa-ddfa-494e-9baa-06aa30d05e6f",
    "stage": "1",
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


distanceMatrix  = MakeRequest(
    "GET",
    "http://192.168.131.50:8081/data",
    "Test",
    headers=HEADER
)
visited = [0]
distanceMatrix = loads(distanceMatrix)
distanceMatrix = {i: {j: distanceMatrix[i][j] for j in range(len(distanceMatrix[i]))} for i in range(len(distanceMatrix))}
while len(visited) < 10:
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
visited += [0]

distanceMatrix  = MakeRequest(
    "POST",
    "http://192.168.131.50:8081/answer",
    "Basic Answer",
    data={"route": str([0,1,2,3,4,5,6,7,8,9,10,0])},
    headers=HEADER
)


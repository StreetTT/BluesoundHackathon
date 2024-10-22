from requests import request, exceptions
from json import loads, dumps
import os


LIVE = False # As the challenge is no longer live, I don't want to send requests to random IPs....
STAGE = 3
SERVER = "192.168.131.50:8081"
ID = "410b8eaa-ddfa-494e-9baa-06aa30d05e6f"
HEADER = {
    "playerid": ID,
    "stage": str(STAGE),
    "Content-Type": "application/x-www-form-urlencoded"
}

# Utility Function
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


# Setup distanceMatrix
file_path = f"stage{STAGE}.json"
if not os.path.exists(file_path) and LIVE:
    distanceMatrix  = loads(MakeRequest(
        "GET",
        f"http://{SERVER}/data",
        "Retrieve distanceMatrix",
        headers=HEADER
    ))
    with open(file_path, "w") as f:
        f.write(dumps(distanceMatrix))
elif os.path.exists(file_path):
    with open(file_path, "r") as f:
        distanceMatrix = loads(f.read()) 
else:
    print("No data to run the challenge with.")
    exit(1)
    
distanceMatrix = {i: {j: distanceMatrix[i][j] for j in range(len(distanceMatrix[i]))} for i in range(len(distanceMatrix))}

# Setup distinction between delivery and fuel stations
if STAGE == 3:
    deliveryStations = {i: {j: distanceMatrix[i][j] for j in distanceMatrix[i] if j not in [20, 40, 60, 80]} for i in distanceMatrix}
    fuelStations = {i: distanceMatrix[i] for i in [20, 40, 60, 80]}

# Solution - Recursive Greedy
def nearest(history, fuel=float("inf"), refuel=False):
    currentStation = history[-1]
    targetStationDistances = ({f: fuelStations[f][currentStation] for f in fuelStations} if refuel else deliveryStations[currentStation]) if STAGE == 3 else distanceMatrix[currentStation]
    sortedTargetStationDistances = sorted(targetStationDistances.items(), key=lambda x: x[1])
    
    # with open("log.txt", "a") as log_file:
    #     log_file.write("--- \n")
    #     log_file.write(f"Visited stations: {history}\n Number of visited stations: {len(history)}\n")
    #     log_file.write(f"Remaining fuel: {fuel} \n")

    i = 0
    while i < len(sortedTargetStationDistances) and len(history) != len(distanceMatrix):
        nextStation = sortedTargetStationDistances[i][0]
        nextStationDistance = sortedTargetStationDistances[i][1]
        couldBeFuel = fuel - nextStationDistance

        # with open("log.txt", "a") as log_file:
        #     log_file.write("- \n")
        #     log_file.write(f"Next station: {nextStation}\n Distance to next station: {nextStationDistance}\n")
        
        # Refuel if we don't have enough fuel
        if couldBeFuel <= 0:
            previousStation = history[-2]
            return nearest(history[:-1], fuel+distanceMatrix[currentStation][previousStation], refuel=True)


        # Skip self-reference or already visited station
        elif nextStation == currentStation or nextStation in history:
            i += 1
            continue
        
        # Move to the next station if we have enough fuel and it's unvisited
        elif nextStation not in history and couldBeFuel > 0:
            n = nearest(history+[nextStation], 100 if refuel else couldBeFuel)
            if n:
                return n
            else:
                i += 1

    # We have visited all delivery stations (including fuel stations if applicable)
    return history + [0]

# with open("log.txt", "w") as f:
#     f.write("\n")
solution = nearest([0], 100) if STAGE == 3 else nearest([0])
if STAGE == 4:
    packagedSolution = {
        "route1": str(solution[0]),
        "route2": str(solution[1]),
        "route3": str(solution[2]),
    }
else:
    packagedSolution = {"route": str(solution)}
print(f"STAGE {STAGE} SOLUTION")
for route in packagedSolution:
    print(f"{route} = {packagedSolution[route]}")
if LIVE:
    MakeRequest(
        "POST",
        f"http://{SERVER}/answer",
        "Basic Answer",
        data=packagedSolution,
        headers=HEADER
    )
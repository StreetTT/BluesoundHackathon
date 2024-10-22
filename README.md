# Parcel Delivery Route Optimization - Coding Challenge

Welcome to my solution for the **Parcel Delivery Route Optimization** coding challenge, which was part of a Hackathon hosted by [Ultamation Limited](https://ultamation.com). 
In this [LinkedIn post](https://www.linkedin.com/posts/bowoye_hackathon-codingchallenges-softwaredevelopment-activity-7254455440367874049-Pc_E?utm_source=share&utm_medium=member_desktop), I share my experience of tackling this challenge.

## Challenge Overview

The goal of this challenge is to optimize the routes for a courier service to minimize the distance traveled while delivering parcels. The challenge progresses through four stages, each increasing in difficulty and complexity. You can find the breakdown of the stages below:

### Stage 1: 10 Destinations
- **Objective:** Find the shortest route to visit 10 delivery nodes, starting and ending at the depot (node 0).
  
### Stage 2: 100 Destinations
- **Objective:** Similar to Stage 1, but with 100 delivery nodes.
  
### Stage 3: Fuel Constraints
- **Objective:** In addition to minimizing the route for 100 delivery nodes, the vehicle now has a fuel capacity of 100 miles. 
- **Fuel Stations:** Located at nodes 20, 40, 60, and 80. The vehicle must refuel when the fuel capacity runs low.

### Stage 4: Multiple Vehicles
- **Objective:** Divide the 300 delivery nodes among 3 vehicles. Each vehicle must handle exactly 100 deliveries, and the goal is to minimize the overall distance traveled by all vehicles.

## Code Breakdown

The code leverages Python and the `requests` library to interact with the challenge's REST API. The solution implements a recursive greedy algorithm for finding the nearest delivery or fuel station. 

Key components:
- **API Communication:** The script handles GET and POST requests to the challenge server using the player’s unique ID.
- **Distance Matrix:** The code reads or retrieves a distance matrix, which contains the distances between delivery nodes.
- **Fuel Management (Stage 3):** For Stage 3, the vehicle refuels at designated fuel stations when necessary.

### How to Use

1. **Prerequisites:** Ensure you have Python installed. You can install the required dependencies using the following command:
    ```bash
    pip install requests
    ```

2. **Run the Script:**
    Modify the `LIVE` and `STAGE` variables in `main.py` based on which stage you want to test. The solution for each stage can be run by executing the following command:
    ```bash
    python main.py
    ```

3. **REST API Interaction:** If the challenge is live, the script will submit your solution to the challenge server. If not, it will simulate the process using local data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
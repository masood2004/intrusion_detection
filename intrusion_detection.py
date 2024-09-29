import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

# Initialize parameters
sensor_count = 50
detection_range = 10.0
area_size = (100, 100)
num_simulations = 1000
num_intruders = 500
grid_size = 100  # For grid-based sensor simulation

# Store results for visualization
detection_probabilities = []
false_alarm_rates = []
sensor_densities = []

# Function to simulate random intruder paths


def generate_intruder_path(area_size):
    path = np.random.rand(10, 2) * area_size
    return path

# Function to check detection by sensors


def check_detection(sensor_positions, intruder_path, detection_range):
    detected = False
    for sensor_position in sensor_positions:
        for intruder_position in intruder_path:
            distance = np.linalg.norm(sensor_position - intruder_position)
            if distance <= detection_range:
                detected = True
                break
        if detected:
            break
    return detected

# Function to simulate intruders on a grid for a Monte Carlo simulation


def simulate_intruder(grid_size):
    path = [np.random.randint(0, grid_size, 2)]
    for _ in range(9):
        direction = np.random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            new_point = path[-1] + np.array([0, 1])
        elif direction == 'down':
            new_point = path[-1] + np.array([0, -1])
        elif direction == 'left':
            new_point = path[-1] + [-1, 0]
        elif direction == 'right':
            new_point = path[-1] + [1, 0]

        if new_point[0] < 0 or new_point[0] >= grid_size or new_point[1] < 0 or new_point[1] >= grid_size:
            break
        path.append(new_point)

    return np.array(path)

# Function to check if an intruder is detected


def is_detected(sensor_positions, intruder_path, detection_range):
    for sensor in sensor_positions:
        distances = np.linalg.norm(intruder_path - sensor, axis=1)
        if np.any(distances <= detection_range):
            return True
    return False


# Random sampling of sensor positions
sensor_positions = np.random.rand(sensor_count, 2) * area_size

# Monte Carlo simulation for intrusion detection
detections = 0
for _ in tqdm(range(num_intruders), desc="Simulating intruder paths"):
    intruder_path = simulate_intruder(grid_size)
    if is_detected(sensor_positions, intruder_path, detection_range):
        detections += 1

# Calculate detection probability
detection_probability = detections / num_intruders
print(f'Detection Probability: {detection_probability:.2f}')

# Scatter Plot: Sensor Density vs. Detection Probability
plt.figure(figsize=(10, 6))
plt.scatter([sensor_count / (area_size[0] * area_size[1])] * num_intruders, [detection_probability] * num_intruders,
            c='blue', label='Sensor Density vs. Detection')
plt.title('Sensor Density vs. Detection Probability')
plt.xlabel('Sensor Density (sensors per unit area)')
plt.ylabel('Detection Probability')
plt.legend()
plt.show()

# Visualization of sensor placement and intruder paths
plt.figure(figsize=(8, 8))
plt.xlim(0, grid_size)
plt.ylim(0, grid_size)
plt.title(f'Sensor Placement and Intruder Paths, Detection Probability: {
          detection_probability:.2f}')

# Plot sensors
plt.scatter(sensor_positions[:, 0],
            sensor_positions[:, 1], c='red', label='Sensors')
for sensor in sensor_positions:
    circle = plt.Circle(sensor, detection_range, color='red', alpha=0.2)
    plt.gca().add_patch(circle)

# Plot sample intruder paths
for _ in range(10):  # Plot a few sample intruder paths
    intruder_path = simulate_intruder(grid_size)
    plt.plot(intruder_path[:, 0], intruder_path[:, 1], c='blue', alpha=0.5)

plt.legend()
plt.show()

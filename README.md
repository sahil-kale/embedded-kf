### embedded-kf Library Overview

**embedded-kf** is a lightweight C library designed to implement Kalman filters on embedded systems. While similar in technical scope to [kalman-clib](https://github.com/sunsided/kalman-clib), it introduces new capabilities while reusing its matrix utility functions. **embedded-kf** offers the following features:

- **Asynchronous measurement updates**: Supports systems with sensors that provide data at different rates.
- **Automatic C code generation**: Generates optimized `.c/.h` files from user-defined JSON configurations with user-friendly APIs.
- **Control vector support**: Direct integration of control-vector inputs during prediction steps
- **Fully statically-allocated**: No dynamic memory is required, which is ideal for resource-constrained environments.

**Key Features:**

- **Optimized for Embedded System Use**: Designed for real-time operation on embedded systems, with easy integration and API
- **Customizable and Extensible**: Easily configurable via JSON, with extensibility to add custom filters or measurement models.
- **Typical Use Cases**:
  - Sensor fusion for robotics, drones, or autonomous vehicles
  - Real-time signal processing for IoT devices 
  - Navigation systems or state estimation in constrained environments

## Usage
1. Define a filter `.json` file. See [`generator/tests/samples`](https://github.com/sahil-kale/embedded-kf/blob/main/generator/tests/samples) for example filters
2. Run `python3 kf_generator.py {path/to/filter/json} {optional: output directory, default=kf_output}`
3. Build and link the generated `.c/.h` files into the software application. A CMakeLists.txt file is generated for convenience
4. Call the filter API - see [`info/API.md`](https://github.com/sahil-kale/embedded-kf/blob/main/info/API.md)

Documentation about the core library functions are available [here](https://sahil-kale.github.io/embedded-kf/).

## Theory and References
[Kalman Filter Theory](https://github.com/sahil-kale/embedded-kf/blob/main/kalman_theory.md)

## Example Smoothing
From an IMU filtering example, the figure below shows the plot of pitch as estimated from raw accelerometer movements and the Kalman filter state estimate
![image](https://github.com/user-attachments/assets/4212b4bf-38c7-4e93-a36e-f3c80fe78a74)


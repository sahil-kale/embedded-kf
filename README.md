### embedded-kf Library Overview

**embedded-kf** is a lightweight C library designed for implementing Kalman filters on embedded systems. While similar in technical scope to [kalman-clib](https://github.com/sunsided/kalman-clib), it introduces new capabilities while reusing its matrix utility functions. **embedded-kf** offers the following features:

- **Fully statically-allocated**: No dynamic memory required, ideal for resource-constrained environments.
- **Control vector support**: Direct integration of control-vector inputs during prediction steps.
- **Asynchronous measurement updates**: Supports systems with sensors that provide data at different rates.
- **Auto code generation**: Generates optimized `.c/.h` files from user-defined JSON configurations with user-friendly APIs.

**Key Features:**

- **Memory and CPU Optimized**: Designed for real-time, low-latency operation on embedded systems.
- **Customizable and Extensible**: Easily configurable via JSON, with extensibility to add custom filters or measurement models.
- **Typical Use Cases**:
  - Sensor fusion for robotics, drones, or autonomous vehicles
  - Real-time signal processing for IoT devices 
  - Navigation systems or state estimation in constrained environments

## Usage
1. Define a filter `.json` file. See `generator/tests/samples` for example filters
2. Run `python3 kf_generator.py {path/to/filter/json} {optional: output directory, default=kf_output}`
3. Build and link the generated `.c/.h` files into the software application. A CMakeLists.txt file is generated for convinence
4. Call the filter API (See `info/API.md`)

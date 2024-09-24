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

**Example Workflow**:
1. Define the system model in JSON.
2. Generate the C code using the tool.
3. Integrate the code into the embedded project.
4. Use the API to update state estimates during runtime.

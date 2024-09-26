# Kalman Filter Theory
The Kalman Filter is a filter designed to provide an optimal state estimate for a linear dynamical system where the entering noise is uncorrelated and distributed in a gaussian manner (i.e. normally distributed).

The filter is based on Bayes Theorem, which provides a mathametical rule to determine the probability of a cause given its effect. 

## Intuition

An intuitive way to think about **Bayes' Theorem** is through the game of **Marco Polo**. In this game, one person (Marco) is blindfolded and has to locate another person (Polo) by calling out "Marco," to which Polo responds "Polo." Marco has to use Polo's responses to guess the direction and distance to Polo.

This process mirrors **Bayesian updating**. Marco starts with an initial guess (a prior) about Polo’s location. Every time Polo responds, Marco updates their estimate of Polo's position based on the new information (the likelihood of Polo being in certain directions based on the sound). As Marco continues to receive responses, their guesses become more accurate because they are constantly refining their estimates.

This mirrors **Bayesian updating** and the **Kalman Filter** process:

- **Initial Estimate (Prior)**: Like Marco's initial guess, the Kalman filter starts with an estimate of the system's state using past data.
- **New Information (Measurement)**: Each of Polo’s responses provides new information, just as sensor data refines the Kalman filter’s state estimate.
- **Updating the Estimate (Posterior)**: Marco updates their guess by combining their prior belief with new information. The Kalman filter does the same by mathematically combining the prior estimate with the new measurement.
- **Accuracy of Update**: Clear responses (low noise) help Marco quickly zero in on Polo, while faint or distorted responses (high noise) make their estimate less accurate. Similarly, the Kalman filter adjusts based on the measurement uncertainty, with less noise leading to more confident updates.

## Filter Math

Below is a definition of each matrix and its size (where **n** is the number of states, **m** is the number of measurements, and **c** is the number of control inputs). The equations are taken from [Kalman Filter - Wikipedia](https://en.wikipedia.org/wiki/Kalman_filter)


- **State Estimate Vector** ($\hat{x}_k$):  
  A vector of size **n x 1** that represents the estimated state of the system at time step **k**.

- **Control Input Vector** ($u_k$):  
  A vector of size **c x 1** that represents the control inputs applied to the system.

- **State Transition Matrix** ($F_k$):  
  A matrix of size **n x n** that models how the system state transitions from one time step to the next.

- **Control Matrix** ($B_k$):  
  A matrix of size **n x c** that models how control inputs affect the system's state.

- **Process Noise Covariance** ($Q_k$):  
  A matrix of size **n x n** that represents the uncertainty in the system model.

- **Measurement Vector** ($z_k$):  
  A vector of size **m x 1** that contains the actual measurements from sensors at time step **k**.

- **Measurement Matrix** ($H_k$):  
  A matrix of size **m x n** that relates the state of the system to the measurements.

- **Measurement Noise Covariance** ($R_k$):  
  A matrix of size **m x m** that represents the uncertainty in the measurements.

- **Estimate Covariance Matrix** ($P_k$):  
  A matrix of size **n x n** that represents the uncertainty in the state estimate at time step **k**.

- **Kalman Gain** ($K_k$):  
  A matrix of size **n x m** that determines how much the estimate should be adjusted based on the new measurements.

#### Predict

**Predicted (a priori) state estimate**

$$ \hat{x}_{k|k-1} = F_k \hat{x}_{k-1|k-1} + B_k u_k $$

**Predicted (a priori) estimate covariance**

$$ P_{k|k-1} = F_k P_{k-1|k-1} F_k^\top + Q_k $$

---

### Update

**Innovation or measurement pre-fit residual**

$$ \tilde{y}_k = z_k - H_k \hat{x}_{k|k-1} $$

**Innovation (or pre-fit residual) covariance**

$$ S_k = H_k P_{k|k-1} H_k^\top + R_k $$

**Optimal Kalman gain**

$$ K_k = P_{k|k-1} H_k^\top S_k^{-1} $$

**Updated (a posteriori) state estimate**

$$ \hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k \tilde{y}_k $$

**Updated (a posteriori) estimate covariance**

$$ P_{k|k} = (I - K_k H_k) P_{k|k-1} $$

**Measurement post-fit residual**

$$ \tilde{y}_{k|k} = z_k - H_k \hat{x}_{k|k} $$

# Time Resolution: Power vs. Energy

## Intro

> **Question:**  
> I'm moving from hourly to daily time steps in my IESopt model. How should I adjust my input data, especially capacities and costs, to ensure accurate results? Should I express capacities as energy per time step (e.g., kWh/day) instead of power (kW)?

> **Answer:**  
> When working with IESopt models, it's crucial to understand how the model interprets units of power and energy, especially when changing the duration of your time steps (snapshots). Here's how to approach this:

## Details

### Keep Capacities in Power Units

- **Unit Capacities:** Always express capacities in power units (e.g., kW), regardless of the time step duration.
- **Profiles and Connections:** Similarly, profiles (e.g., time series data) and connection bounds should remain in power units.

### Costs Are Per Unit of Energy

- **Variable Costs:** Input costs as monetary units per unit of energy (e.g., €/kWh).
- **Consistency:** This approach ensures that cost calculations remain accurate, as the model internally accounts for time step durations.

### Time Step Duration Is Handled Internally

- **Internal Calculations:** IESopt multiplies power by the duration of each time step to calculate energy.
- **Cost Formula:** The total cost is calculated using the formula:
  
  $$
  \text{Cost (€)} = \text{Power (kW)} \times \text{Duration (h)} \times \text{Cost per Energy Unit (€/kWh)}
  $$
  
- **No Manual Adjustments Needed:** You don't need to convert capacities to energy units per time step; the model does this for you.

### Specify Time Step Duration in the Configuration

- **Snapshots Configuration:** Define the duration of each time step using the `weights` parameter in your `snapshots` configuration.
  
  ```yaml
  snapshots:
    count: 365       # Number of time steps (e.g., days in a year)
    weights: 24      # Duration of each time step in hours (for daily steps)
  ```

- **Example:** If each time step represents one day, setting `weights: 24` tells the model that each snapshot spans 24 hours.

### Storage Units Are in Energy Units

- **Exception for Storage:** Capacities for storage units are specified in energy units (e.g., kWh) because they represent stored energy, not power output.

### Practical Example

Suppose you have a generator with:

- **Capacity:** 100 kW
- **Marginal Cost:** 0.10 €/kWh
- **Time Step Duration:** 24 hours (daily)

The model calculates the energy produced and the cost as follows:

- **Energy Produced per Time Step:**
  
  $$
  \text{Energy (kWh)} = \text{Power (kW)} \times \text{Duration (h)} = 100 \times 24 = 2,400 \text{ kWh}
  $$
  
- **Total Cost per Time Step:**
  
  $$
  \text{Cost (€)} = \text{Energy (kWh)} \times \text{Cost per Energy Unit (€/kWh)} = 2,400 \times 0.10 = 240 \text{ €}
  $$

## Summary

### Key Takeaways

- **No Need to Adjust Units:** Keep capacities in power units; do not convert them to energy per time step.
- **Costs Remain per Energy Unit:** Continue to provide costs in €/kWh or similar units.
- **Model Handles Duration:** The model uses the `weights` parameter to account for the duration of each time step in calculations.
- **Consistency Is Crucial:** By keeping units consistent, you ensure accurate modeling results without additional adjustments.

### Conclusion

Changing the time step duration in your IESopt model doesn't require you to alter your input units. By specifying capacities in power units and costs per unit of energy, and by correctly configuring the time step durations, IESopt will accurately compute the energy and costs internally.
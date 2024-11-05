# Time resolution & power vs. energy

## Intro

**Question:**  
> I'm moving from hourly to daily time steps in my IESopt model. How should I adjust my input data, especially capacities and costs, to ensure accurate results? Should I express capacities as energy per time step (e.g., kWh/day) instead of power (kW)?

**Answer:**  
> When working with IESopt models, it's crucial to understand how the model interprets units of power and energy, especially when changing the duration of your time steps (snapshots).

## Details

The following steps guide you through the changes:

1. Update the duration of each time step using the `weights` parameter in your `snapshots` configuration.
2. Make sure that you are using the correct power/energy convention for configuring the model's components.
3. Resample time series data, where necessary.

### Configuring snapshots

First, update your `snapshots` section of the top-level YAML config. This can be used not only to set the total number of snapshots in your model, but also how long each one is, using the `weights` parameter.

```yaml
config:
  optimization:
    # ... other settings ...
    snapshots:
      count: 365       # Number of time steps (e.g., days in a year)
      weights: 24      # Duration of each time step in hours (for daily steps)
```

> **Example:**  
> If each time step represents one day, setting `weights: 24` tells the model that each snapshot spans 24 hours.

#### Time step duration is handled internally

Accounting for the "conversion" between power and energy terms is handled internally:

- IESopt multiplies power by the duration of each time step to calculate energy.
- You don't need to convert capacities to energy units per time step; the model does this for you.

> Internally, the total cost is calculated using a formula along the lines of:
>
> $$
> \text{Cost (€)} = \text{Power (kW)} \times \text{Duration (h)} \times \text{Cost per Energy Unit (€/kWh)}
> $$

### Checking power/energy units

#### Keep capacities in power units

- **Unit Capacities:** Always express capacities in power units (e.g., kW), regardless of the time step duration.
- **Profiles and Connections:** Similarly, [Profiles](/pages/manual/yaml/core/profile.md) (e.g., time series data) and [connection](/pages/manual/yaml/core/connection.md) bounds should remain in power units.

#### Costs are per unit of energy

- **Variable Costs:** Input costs as monetary units per unit of energy (e.g., €/kWh).
- **Consistency:** This approach ensures that cost calculations remain accurate, as the model internally accounts for time step durations.

#### Storage units are in energy units

- **Exception for storage:** Capacities for storage units are specified in energy units (e.g., kWh) because they represent stored energy, not power output.

#### Practical example

Suppose you have a generator with:

- **Capacity:** 100 kW
- **Marginal cost:** 0.10 €/kWh
- **Time step duration:** 24 hours (daily)

The model calculates the energy produced and the cost as follows:

- **Energy produced per time step:**
  
  $$
  \text{Energy (kWh)} = \text{Power (kW)} \times \text{Duration (h)} = 100 \times 24 = 2,400 \text{ kWh}
  $$
  
- **Total cost per time step:**
  
  $$
  \text{Cost (€)} = \text{Energy (kWh)} \times \text{Cost per Energy Unit (€/kWh)} = 2,400 \times 0.10 = 240 \text{ €}
  $$

### Resampling time series data

Sometimes, or rather most of the time, you will need to update the input time series data. Not because a change of units happened, but because moving from hourly to daily snapshots will essentially reduce the length of your data by the factor 24. A quick "checklist" on what to use:

- Resampling a time series given in a power unit is done by taking **the mean** of all grouped time steps _(you should almost only need this)_.
- Resampling a time series given in an energy unit is done by taking **the sum** of all grouped time steps _(you most likely never need this)_.

> If you are using Python, a simple way to achieve this is using the `groupby` or `resample` functionalities that a `pandas.DataFrame` offers.

#### Example

Consider a time series of energy demand. This is used as input to configure a Profile. That means: **It's given in power units** - and if it's not then make sure it is, because the reason it worked for a "1-hourly" model was only because the numerical values mapping `kW -> kWh` are the same; however, for any other time resolution that fails.

If we now aggregate / group 24 time steps, and then the next 24 and so on, then the most common way to calculate the proper daily power is by taking the mean. Let's assume the demand is 10 kW for the first 12 hours, and 20 kW for the last 12 hours. Taking the mean would tell us to use 15 kW as value of our demand time series, when using a daily resolution.

_Let's check if that is correct ..._

1. The total energy consumption in the first 12 hours is 120 kWh, and 240 kWh for the last 12 hours, for a total of 360 kWh during the day.
2. A resampled demand time series of 15 kW would results in $15 kW \times 24h = 360 kWh$.

So, we see that the energy consumed stays the same. Note: Other methods of resampling the power time series could be valid in certain cases, but this here is the only one that preserves the total energy consumed - which is what drives costs in our model and is therefore one of the most important parameters.

## Summary

### Key takeaways

- **No need to adjust units:** Keep capacities in power units; do not convert them to energy per time step.
- **Costs remain per energy unit:** Continue to provide costs in €/kWh or similar units.
- **Model handles duration:** The model uses the `weights` parameter to account for the duration of each time step in calculations.
- **Consistency is crucial:** By keeping units consistent, you ensure accurate modeling results without additional adjustments.

### Conclusion

Changing the time step duration in your IESopt model doesn't require you to alter your input units. By specifying capacities in power units and costs per unit of energy, and by correctly configuring the time step durations, IESopt will accurately compute the energy and costs internally.
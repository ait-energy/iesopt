# Output-dependent marginal costs

**Question:**  
> How can I model a Unit where the marginal cost changes based on the level of energy output? For example, the cost is 5 €/MWh for outputs below 5 MW of power and 10 €/MWh for outputs above 5 MW of power.

**Answer:**  
> To model changing marginal costs based on output levels in IESopt, you can split the Unit into two separate Units:

## Details

### Explanation

1. **Low-output unit:**
   - Represents the output up to 5 MW.
   - Has a marginal cost of 5 €/MWh.
   - Capacity is limited to 5 MW.

2. **High-output unit:**
   - Represents any output above 5 MW.
   - Has a marginal cost of 10 €/MWh.
   - No specific capacity limit unless there's an overall maximum output.

By doing this, the model will prioritize the low-cost Unit up to its capacity before utilizing the high-cost Unit for additional demand.

### Implementation

```yaml
unit_pool_1:
  type: Unit
  inputs: {}              # fill this with the original configuration
  outputs: {}             # fill this with the original configuration
  conversion: foo -> bar  # fill this with the original configuration
  capacity: 5 out:electricity
  marginal_cost: 5 per out:electricity

unit_pool_2:
  type: Unit
  inputs: {}              # fill this with the original configuration
  outputs: {}             # fill this with the original configuration
  conversion: foo -> bar  # fill this with the original configuration
  marginal_cost: 10 per out:electricity
```

## Summary

### Notes

- **Flexibility:** This method allows you to create multiple cost bands by adding more Units with different capacities and marginal costs.
- **Intuitiveness:** Splitting Units makes the model easier to understand and maintain.
- **Accuracy:** The model will naturally favor the lower-cost Unit up to its capacity limit before using higher-cost options.

But ...

- This might be an over complicated way to represent stuff like actual cost-power curve dynamics.
- This might add too many Units, making the model hart to understand or analyse.
- If there is any reason that the model might save costs by not running the "lower price" Unit it will do so! This means the "higher price" part of your asset could be used with out running the "lower price", which in reality is not possible (where it's one asset).

Note that the last point most likely will not occur for your model, but ... it's something to keep in mind.

### Conclusion

By representing different output levels with separate Units in IESopt, you can effectively model Units with changing marginal costs based on their energy output. This approach is straightforward and leverages the existing capabilities of IESopt without the need for complex cost functions.

### Improvements

The "best" or final way to represent stuff like this will always be a custom made addon (potentially making use of SOS variables).

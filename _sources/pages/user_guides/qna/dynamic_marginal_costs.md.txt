# Output-dependent marginal costs

**Question:**  
> How can I model a [Unit](/pages/manual/yaml/core/unit.md) where the marginal cost changes based on the level of energy output? For example, the cost is 5 €/MWh for outputs below 5 MW of power and 10 €/MWh for outputs above 5 MW of power.

**Answer:**  
> To model changing marginal costs based on output levels in IESopt, you can split the [Unit](/pages/manual/yaml/core/unit.md) into two separate [Units](/pages/manual/yaml/core/unit.md):

## Details

### Explanation

1. **Low-output [Unit](/pages/manual/yaml/core/unit.md):**
   - Represents the output up to 5 MW.
   - Has a marginal cost of 5 €/MWh.
   - Capacity is limited to 5 MW.

2. **High-output [Unit](/pages/manual/yaml/core/unit.md):**
   - Represents any output above 5 MW.
   - Has a marginal cost of 10 €/MWh.
   - The capacity is given as total capacity of the "real" [Unit](/pages/manual/yaml/core/unit.md), reduced by 5 MW.

By doing this, the model will prioritize the low-cost [Unit](/pages/manual/yaml/core/unit.md) up to its capacity before utilizing the high-cost [Unit](/pages/manual/yaml/core/unit.md) for additional demand.

### Implementation

```yaml
unit_pool_1:
  type: Unit
  inputs: {}                    # fill this with the original configuration
  outputs: {}                   # fill this with the original configuration
  conversion: foo -> bar        # fill this with the original configuration
  capacity: 5 out:electricity
  marginal_cost: 5 per out:electricity

unit_pool_2:
  type: Unit
  inputs: {}                    # fill this with the original configuration
  outputs: {}                   # fill this with the original configuration
  conversion: foo -> bar        # fill this with the original configuration
  capacity: 95 out:electricity  # `100 - 5` MW, assuming 100 MW is the max.
  marginal_cost: 10 per out:electricity
```

## Summary

### Notes

- **Flexibility:** This method allows you to create multiple cost bands by adding more [Units](/pages/manual/yaml/core/unit.md) with different capacities and marginal costs.
- **Intuitiveness:** Splitting [Units](/pages/manual/yaml/core/unit.md) makes the model easier to understand and maintain.
- **Accuracy:** The model will naturally favor the lower-cost [Unit](/pages/manual/yaml/core/unit.md) up to its capacity limit before using higher-cost options.

But ...

- This might be an over complicated way to represent stuff like actual cost-power curve dynamics.
- This might add too many [Units](/pages/manual/yaml/core/unit.md), making the model hard to understand or analyse.
- If there is any reason that the model might save costs by not running the "lower price" [Unit](/pages/manual/yaml/core/unit.md) it will do so! This means the "higher price" part of your asset could be used with out running the "lower price", which in reality is not possible (where it's one asset).

Note that the last point most likely will not occur for your model, but ... it's something to keep in mind.

### Conclusion

By representing different output levels with separate [Units](/pages/manual/yaml/core/unit.md) in IESopt, you can effectively model [Units](/pages/manual/yaml/core/unit.md) with changing marginal costs based on their energy output. This approach is straightforward and leverages the existing capabilities of IESopt without the need for complex cost functions.

### Improvements

The "best" or final way to represent stuff like this will always be a custom made addon (potentially making use of SOS variables).

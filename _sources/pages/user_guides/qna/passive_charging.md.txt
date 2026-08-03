# Passive charging of an underground heat storage

## Intro

**Question:**  
> How can I represent passive charging in a borehole heat storage within my energy system optimization model?

**Answer:**  
> It's complicated ... But the only generally applicable answer is: A custom addon. The underlying idea is to separate the passive charging from the storage, into a separate "artificial" Profile, that can then accurately depict the passive behavior.

## The problem

When modeling a borehole heat storage - a deep underground heat storage surrounded by warm soil - it's important to account for passive charging from the surrounding soil. This guide explains how to represent this passive energy input in your model.

### Common misconception

You might consider using the `state_percentage_loss` parameter with a negative value to simulate passive charging:

```yaml
state_percentage_loss: -0.01  # Attempting to charge 1% per timestep
```

However, `state_percentage_loss` is designed for losses based on the **current storage level**. Using a negative value would incorrectly charge the storage by a percentage of its **existing energy content**, not the energy it lacks.

Therefore, while `-0.01` might be an allowed or in other cases even reasonable choice, it's not made for what is needed here.

## Recommended solution

Instead, model passive charging as an additional input that depends on how much energy the storage lacks. Here's how:

### Naive static charging

Create a new component using a ranged Profile:

```yaml
passive_charging:
  type: Profile
  mode: ranged
  lb: 0
  ub: MAX_PASSIVE_POWER  # Use any estimation of maximum passive charging power
```

The mode setting `ranged` transforms a basic Profile (with default `mode: fixed`), that cannot change it's value, to a more advanced one that can freely pick it's value from the interval `[0, MAX_PASSIVE_POWER]` - independently for each snapshot. This means, charging `0` is a feasible choice, resulting in no charge happening when the storage is already full. If the storage is not full, it will charge how much is economically optimal: Most of the time it will fully use it's passive charging power, but if - for any reason - getting rid of excess heat might not be possible, or very costly, it can choose to not use the passive charging (which in reality would not be possible).

### Custom constraint

Use an addon to add a constraint limiting the passive charging based on the storage's unfilled capacity. Assuming that `heat_storage` is the name of the stateful [Node](/pages/manual/yaml/core/node.md) that represents the underground storage, then:

```julia
# ... other stuff in your addon ...

function add_passive_charging(model::JuMP.Model)
    c_passive_charging = IESopt.get_component(model, "passive_charging")
    c_storage = IESopt.get_component(model, "heat_storage")

    IESopt.@constraint(model, [t in T], c_passive_charging.exp.value[t] <= 0.01 * (c_storage.state_ub - c_storage.var.state[t]))
end

# ... other stuff in your addon ...
```

This ensures the passive charging at time `t` doesn't exceed 1% of the storage's remaining capacity.

> Earlier we discussed the possibility of the model foregoing available passive charging, if economically beneficial. If that is something that you explicitly want to prevent, you can also use `=` in the above constraint, which will force the Profile to the exact value, without the possibility to charge less!

## Summary

### Steps to implement

1. **Create the storage component**: Define your underground storage [Node](/pages/manual/yaml/core/node.md) without using `state_percentage_loss` for passive charging.
2. **Add the Passive Charging Input**: Introduce a Profile to represent the passive energy inflow.
3. **Set Profile Bounds**: Use the mode `ranged` for the Profile with appropriate lower (`lb`) and upper (`ub`) bounds.
4. **Add the Constraint**: Implement the constraint to tie the passive charging rate to the storage's unfilled capacity.
5. **Refine as Needed**: Adjust the constraint for more complex behaviors if necessary. There might be a lot (!) that you might want to specialize.

### Conclusion

By modeling passive charging as a constrained input energy flow based on the storage's remaining capacity, you accurately represent the thermal interactions of an underground heat storage with its environment.

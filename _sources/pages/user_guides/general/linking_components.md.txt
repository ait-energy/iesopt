# Linking components

Sometimes, two or more components need to be linked together. While this can be achieved using addons, it can be achieved using custom functionality within a template. Consider the following (shortened) version of the `CHP` template:

```yaml
parameters:
  p_max: null
  h_max: null
  power_ratio: 0.55
  power_loss_ratio: 0.20
  efficiency: 0.40
  fuel: gas
  fuel_co2_emission_factor: 0.2
  fuel_in: null
  power_out: null
  heat_out: null
  co2_out: null

components:
  power:
    type: Unit
    inputs: {<fuel>: <fuel_in>}
    outputs: {electricity: <power_out>, co2: <co2_out>}
    conversion: 1 <fuel> -> <efficiency> electricity + <fuel_co2_emission_factor> co2
    capacity: <p_max> out:electricity

  heat:
    type: Unit
    inputs: {<fuel>: <fuel_in>}
    outputs: {heat: <heat_out>, co2: <co2_out>}
    conversion: 1 <fuel> -> <efficiency>/<power_loss_ratio> heat + <fuel_co2_emission_factor> co2
    capacity: <h_max> out:heat

functions:
  finalize: |
    # Parameters.
    cm = this.get("power_ratio")
    cv = this.get("power_loss_ratio")
    p_max = this.get("p_max")

    # Output expressions.
    out_heat = this.heat.exp.out_heat
    out_elec = this.power.exp.out_electricity

    # Add constraints.
    @constraint(this.model, cm .* out_heat .<= out_elec)
    @constraint(this.model, out_elec .<= p_max .- cv .* out_heat)
```

This makes use of the `finalize(...)` function to link the `power` and `heat` components. Using an addon can be complicated, because the components do not inherently know about each other. The `finalize(...)` function however is attached to the template itself, can access both components, and is called after both are fully constructed, which means it can freely access their variables and expressions.

> **Note:** A similar approach is possible by using the `build_priority` parameter in the component definition. This parameter allows you to specify the order in which components are built, which can be used to ensure that one component is built before another.

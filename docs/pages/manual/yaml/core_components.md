# Components

- A [Connection](./core/connection.md) is used to model arbitrary flows of energy between Nodes. It allows for limits, costs, delays, ...
- A [Decision](./core/decision.md) represents a basic decision variable in the model that can be used as input for various other core component's settings, as well as have associated costs.
- A [Node](./core/node.md) represents a basic intersection/hub for energy flows. This can for example be some sort of bus (for electrical systems). It enforces a nodal balance equation (= "energy that flows into it must flow out") for every Snapshot. Enabling the internal state of the `Node` allows it to act as energy storage, modifying the nodal balance equation. This allows using `Node`s for various storage tasks (like batteries, hydro reservoirs, heat storages, ...).
- A [Profile](./core/profile.md) allows representing "model boundaries" - parts of initial problem that are not endogenously modelled - with a support for time series data. Examples are hydro reservoir inflows, electricity demand, importing gas, and so on. Besides modelling fixed [Profiles](/pages/manual/yaml/core/profile.md)s, they also allow different ways to modify the value endogenously.
- A [Unit](./core/unit.md) allows transforming one (or many) forms of energy into another one (or many), given some constraints and costs.

:::{tip}
There exists a further type, called `Virtual`, that works almost exactly the same as any other core component - but is only a virtual placeholder for non-existing components of your model. These are ones that a user might expect to exist, but are removed due to flattening the model topology: Each template that gets instantiated is dropped from the model and replaced by the components that it actually constructs. To allow accessing these components, `Virtual` components are used.

Their usage, and various internal details, are rather advanced and currently not fully documented.
:::

## Custom config for core components

It can be useful to assign additional variables to a core component. For example, to give every unit of the same type a variable, so that you may use it in a single addon where you loop over all that units (marked by a tag).
You can see this approach applied in the [CHP core template](https://github.com/ait-energy/IESopt.jl/blob/54c36a51dc8d57e686ecfeaec42abf8114f20819/assets/templates/CHP.iesopt.template.yaml#L44-L47).

```yaml
unit:
  type: Unit
  inputs: {}                    
  outputs: {}                   
  conversion: foo -> bar        
  capacity: 5 out:electricity
  config: {my_variable: <value>}
```

## Fixed cost of core components

Although not relevant for the optimization, it can be convenient to be able to add fixed cost to a core component, e.g., the fixed operational cost of an existing unit. It will add this amount to the objective value. Look at example '46_constants_in_objective' to see it applied.

```yaml
unit:
  type: Unit
  inputs: {}                    
  outputs: {}                   
  conversion: foo -> bar        
  capacity: 5 out:electricity
  objectives: {total_cost: <cost_per_unit_per_optimization_horizon>}
```

:::{toctree}
:hidden:

core/connection.md
core/decision.md
core/node.md
core/profile.md
core/unit.md
:::

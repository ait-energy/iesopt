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

:::{toctree}
:hidden:

core/connection.md
core/decision.md
core/node.md
core/profile.md
core/unit.md
:::

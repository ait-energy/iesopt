# Best practices

## Separate energy carriers

Imagine a system where a heat pump is used to produce _heat_ for both heating and hot water. One may be tempted to use
`heat` as corresponding energy carrier for both purposes. However, this is not recommended. Instead, one could use
`heating` and `hotwater` as energy carriers (or any other naming, as long as it creates a distinction).

**Why?**

1. **Clarity:** It is easier to understand the system when energy carriers are clearly separated.
2. **Flexibility:** It is easier to change the system later on. For example, if one wants to replace the heat pump with
   a gas boiler - but just for hot water - it is easier to do so when the energy carriers are separated.
3. **Consistency:** It is easier to compare different systems when the energy carriers are consistently named.
4. **Error prevention:** It is less likely to make mistakes when the energy carriers are clearly separated. Mistkenly
   connecting two [Nodes](/pages/manual/yaml/core/node.md) with `heat`, that in reality could not be connected since they are part of two different
   systems, cannot happen when the energy carriers are separated.
5. **Plotting:** It is easier to plot the system when the energy carriers are separated. For example, one can plot the
   heat demand for heating and hot water separately, or immediately see how much energy is being spent to supply the
   different demands.

> These are just a few reasons why it is recommended to separate energy carriers. Different systems may have different
> requirements, so it is up to the user to decide how to name the energy carriers. However, it is recommended to keep
> the energy carriers as separate as reasonable.

:::{admonition} Definition: Energy carrier
:class: tip

_According to ISO 13600, an energy carrier is either a substance or a phenomenon that can be used to produce
mechanical work or heat or to operate chemical or physical processes._

This may be seen as motivation why, in this
case, the argument "both are heat" may not be valid: In the end, the actual "carrier" is most likely `water`, and not
`heat` (even if that is most commonly used as "carrier"). However, no one would argue to actually use `water` in
this example, which shows that the choice of `heat` would already be "not 100% exact"; therefore, the separation
into different two carriers does not "mis-represent" reality, but instead just makes our "abstraction" (= not using
`water` as carrier) more explicit.
:::

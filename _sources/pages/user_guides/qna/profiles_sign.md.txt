# Sign convention for time series

## Intro

**Question:**  
> How does IESopt interpret positive and negative values in a Profile connected using `node_from`?

**Answer:**  
> When modeling energy systems in IESopt, you might have a fixed Profile representing both energy demand and supply — the proper sign of generation / consumption then depends on the way it is configured and connects to other components. Understanding how to correctly connect this Profile to a [Node](/pages/manual/yaml/core/node.md) is crucial for accurate results.

## Details

### Understanding `node_from` and `node_to`

Generally the following intuition applies:

- **`node_from`:** Indicates that the component draws energy from the specified [Node](/pages/manual/yaml/core/node.md).
- **`node_to`:** Indicates that the component injects energy into the specified [Node](/pages/manual/yaml/core/node.md).

#### Example: `node_from`

If you connect your fixed Profile (`mode: fixed`, which is the default) to a [Node](/pages/manual/yaml/core/node.md) using `node_from`, here's how IESopt interprets the values:

- **Positive Values:** The Profile draws energy from the [Node](/pages/manual/yaml/core/node.md) (consumption).
- **Negative Values:** The Profile effectively injects energy into the [Node](/pages/manual/yaml/core/node.md) (generation).

### Why does this happen?

In IESopt, drawing a negative amount of energy from a [Node](/pages/manual/yaml/core/node.md) (`-x kWh`) is mathematically equivalent to injecting a positive amount of energy (`+x kWh`) into it. This means, the following are equal:

- A negative value in a `node_from`-configured Profile
- A positive value in a `node_to`-configured Profile
- Injecting `x > 0` units of energy into a [Node](/pages/manual/yaml/core/node.md)
- Withdrawing a negative amount of energy from a [Node](/pages/manual/yaml/core/node.md)

## Practical example

Suppose you have a fixed Profile connected to an electricity grid [Node](/pages/manual/yaml/core/node.md):

```yaml
myprofile:
  type: Profile
  carrier: electricity
  node_from: elec_grid_node
  value: [100, -50, 150, -75]  # in kW
```

- **At time step 1:** The [Profile](/pages/manual/yaml/core/profile.md) draws with a power of 100 kW from the [Node](/pages/manual/yaml/core/node.md) (consumption).
- **At time step 2:** The [Profile](/pages/manual/yaml/core/profile.md) injects with a power of 50 kW into the [Node](/pages/manual/yaml/core/node.md) (generation).
- **And so on.**

### Alternative approach with `node_to`

If you prefer to handle injections explicitly, you can use `node_to`:

- Connect your [Profile](/pages/manual/yaml/core/profile.md) using `node_to`.
- Positive values will inject energy into the [Node](/pages/manual/yaml/core/node.md).
- Negative values will draw energy from the [Node](/pages/manual/yaml/core/node.md).

## Summary

- **Using `node_from`:**
  - Positive values = Draw from [Node](/pages/manual/yaml/core/node.md).
  - Negative values = Inject into [Node](/pages/manual/yaml/core/node.md).
- **Using `node_to`:**
  - Positive values = Inject into [Node](/pages/manual/yaml/core/node.md).
  - Negative values = Draw from [Node](/pages/manual/yaml/core/node.md).

By correctly setting up your Profile and understanding the sign conventions, you ensure that your model accurately reflects the intended energy flows.
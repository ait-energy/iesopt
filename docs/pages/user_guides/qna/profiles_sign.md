# Sign Convention for Time Series

## Intro

> **Question:**  
> How does IESopt interpret positive and negative values in a Profile connected using `node_from`?

> **Answer:**  
> When modeling energy systems in IESopt, you might have a fixed Profile representing both energy demand and supply — the proper sign of generation / consumption then depends on the way it is configured and connects to other components. Understanding how to correctly connect this Profile to a Node is crucial for accurate results.

## Details

### Understanding `node_from` and `node_to`

Generally the following intuition applies:

- **`node_from`:** Indicates that the component draws energy from the specified Node.
- **`node_to`:** Indicates that the component injects energy into the specified Node.

#### Example: `node_from`

If you connect your fixed Profile (`mode: fixed`, which is the default) to a Node using `node_from`, here's how IESopt interprets the values:

- **Positive Values:** The Profile draws energy from the Node (consumption).
- **Negative Values:** The Profile effectively injects energy into the Node (generation).

### Why Does This Happen?

In IESopt, drawing a negative amount of energy from a Node (`-x kWh`) is mathematically equivalent to injecting a positive amount of energy (`+x kWh`) into it. This means, the following are equal:

- A negative value in a `node_from`-configured Profile
- A positive value in a `node_to`-configured Profile
- Injecting `x > 0` units of energy into a Node
- Withdrawing a negative amount of energy from a Node

## Practical Example

Suppose you have a fixed Profile connected to a heating grid Node:

```yaml
myprofile:
  type: Profile
  carrier: electricity
  node_from: elec_grid_node
  value: [100, -50, 150, -75]  # in kW
```

- **At time step 1:** The profile draws with a power of 100 kW from the node (consumption).
- **At time step 2:** The profile injects with a power of 50 kW into the node (generation).
- **And so on.**

### Alternative Approach with `node_to`

If you prefer to handle injections explicitly, you can use `node_to`:

- Connect your profile using `node_to`.
- Positive values will inject energy into the node.
- Negative values will draw energy from the node.

## Summary

- **Using `node_from`:**
  - Positive values = Draw from node.
  - Negative values = Inject into node.
- **Using `node_to`:**
  - Positive values = Inject into node.
  - Negative values = Draw from node.

By correctly setting up your Profile and understanding the sign conventions, you ensure that your model accurately reflects the intended energy flows.
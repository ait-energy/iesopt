import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider
except ImportError:
    print("ERROR: Matplotlib is required for NVP visualization. Please install it via 'uv add matplotlib'.")

try:
    from scipy.spatial import ConvexHull
except ImportError:
    print("ERROR: Scipy is required for NVP. Please install it via 'uv add scipy'.")

from ...model import Model
from ..algorithm import Algorithm
from .util import set_weighted_objective, add_obj_threshold_constraint


# Calculate the normal vector pointing inward the convex hull
def calculate_inward_normal(edge_start, edge_end, hull_vertices):
    # Calculate the edge vector
    edge_vector = edge_end - edge_start

    # Calculate the perpendicular vector (rotate 90 degrees)
    # For 2D: if edge is [dx, dy], perpendiculars are [-dy, dx] and [dy, -dx]
    normal_candidate1 = np.array([-edge_vector[1], edge_vector[0]])
    normal_candidate2 = np.array([edge_vector[1], -edge_vector[0]])

    # Find the midpoint of the edge
    edge_midpoint = (edge_start + edge_end) / 2

    # Find the centroid of the convex hull
    centroid = np.mean(hull_vertices, axis=0)

    # Vector from centroid to edge midpoint
    centroid_to_edge = edge_midpoint - centroid

    # Choose the normal that points in the same direction as centroid_to_edge
    # (i.e., away from the centroid, which means inward from the hull)
    if np.dot(normal_candidate1, centroid_to_edge) < 0:
        inward_normal = normal_candidate1
    else:
        inward_normal = normal_candidate2

    # Normalize to unit vector
    return inward_normal / np.linalg.norm(inward_normal)


class Trial:
    def __init__(self, direction: dict):
        self.direction = direction
        self.solution = None
        self.gain = -np.inf

    @property
    def redundant(self):
        return self.gain < 1e-3


class Trials:
    def __init__(self):
        self._scheduled = []
        self._completed = []

    @property
    def is_empty(self):
        return len(self._scheduled) == 0

    def schedule(self, direction):
        self._scheduled.append(Trial(direction))

    def pop(self):
        return self._scheduled.pop(0)

    def complete(self, trial, solution):
        trial.solution = solution
        self._completed.append(trial)

    def get_solutions(self):
        return [t.solution for t in self._completed]

    def get_visited_directions(self):
        return [t.direction for t in self._completed if all(v is not None for v in t.direction.values())]


class Domain:
    def __init__(self, solutions):
        self._solutions = solutions
        self._points = np.array([[s[dim] for dim in list(solutions[0].keys())[1:]] for s in solutions])

        try:
            self._calculate_convex_hull()
            self.valid = True
        except Exception as _:
            self.valid = False

    def _calculate_convex_hull(self):
        hull = ConvexHull(self._points)
        vertices = self._points[hull.vertices]
        edges = []
        for simplex in hull.simplices:
            edges.append((self._points[simplex[0]], self._points[simplex[1]]))
        self.vertices = vertices
        self.edges = edges
        self.hull = hull

        self._calculate_edge_normals()
        self._calculate_edge_lengths()

    def get_edge(self, index):
        return self.edges[index], self._edge_lengths[index], self._normals[index]

    def plot(self, ax=None):
        # TODO: plot current "max domain" (and "direction"; but that not in the "domain")
        create_fig = ax is None
        if create_fig:
            fig, ax = plt.subplots(figsize=(10, 8))
        ax.scatter(self._points[:, 0], self._points[:, 1], c="lightblue", s=50, alpha=0.6, label="All Solutions")
        ax.scatter(self.vertices[:, 0], self.vertices[:, 1], c="red", s=50, label="Hull Vertices", zorder=5)
        for simplex in self.hull.simplices:
            ax.plot(self._points[simplex, 0], self._points[simplex, 1], "r-", linewidth=2)
        ax.fill(self.vertices[:, 0], self.vertices[:, 1], alpha=0.2, color="red")
        ax.legend()
        ax.grid(True, alpha=0.3)
        if create_fig:
            plt.tight_layout()
            return fig, ax
        return None

    def _calculate_edge_lengths(self):
        self._edge_lengths = [np.linalg.norm(edge_end - edge_start) for edge_start, edge_end in self.edges]

    def _calculate_edge_normals(self):
        self._normals = []
        for edge_start, edge_end in self.edges:
            normal = calculate_inward_normal(edge_start, edge_end, self.vertices)
            self._normals.append(normal)


class Domains:
    def __init__(self):
        self._domains = []

    def append(self, domain):
        self._domains.append(domain)

    def __len__(self):
        return len(self._domains)

    def __getitem__(self, index):
        return self._domains[index]

    def plot(self):
        objectives = list(self._domains[0]._solutions[0].keys())
        valid = [domain for domain in self._domains if domain.valid]

        xvals = [val for d in valid for val in d._points[:, 0]]
        yvals = [val for d in valid for val in d._points[:, 1]]
        xrange = min(xvals) * 0.95, max(xvals) * 1.05
        yrange = min(yvals) * 0.95, max(yvals) * 1.05

        fig, ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.25)

        # Create a slider for navigating through the plots
        ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])
        self._plot_slider = Slider(ax_slider, "Plot Index", 0, len(valid) - 1, valinit=0, valstep=1)

        def update(val):
            ax.cla()
            valid[int(val)].plot(ax=ax)
            fig.canvas.draw_idle()
            ax.set_xlabel(objectives[1])
            ax.set_ylabel(objectives[2])
            ax.set_xlim(xrange)
            ax.set_ylim(yrange)

        self._plot_slider.on_changed(update)
        update(0)
        return fig, ax


# NOTE on specific solver choice:
# dual: constraints change
# primal: objective change
# iesopt.JuMP.set_attribute(model.core, "Method", -1)
# iesopt.JuMP.set_attribute(model.core, "Method", 1)  # dual (to change constraints)
# iesopt.JuMP.set_attribute(model.core, "Method", 0)  # primal (to change objective)


class NVP(Algorithm):
    """
    Normal Vector Pushing (like the most basic HSJ MGA algorithm).

    This requires the following additional dependencies:

    - scipy
    - matplotlib (for plotting)
    - pyqt6 (for plotting if necessary to show the interactive windows)

    Example usage:
        ```python
        import iesopt
        import iesopt.alg.mga as mga

        # Consider setting `verbosity.core: error` and `verbosity.solver: off` in the config!
        model = iesopt.Model("config.iesopt.yaml")

        nvp = mga.NVP(model, ["total_cost", "other_objective_A", "other_objective_B"], eps=0.05)
        nvp.run(maxiter=25)
        fig, ax = nvp.visualize()
        fig.show()
        # ... or save the figure!
        ```

        where the objectives could be defined like this in the config:

        ```yaml
        other_objective_A: [heatpump.exp.out_heat, hp_cool.heatpump.exp.out_heat]
        other_objective_B: [hwk_ne2.exp.out_heat, hwk_ne3.boiler.exp.out_heat]
        ```
    """

    def __init__(self, model: Model, objectives: list[str], eps: float):
        assert len(objectives) == 3, "NVP currently only supports 3 objectives (1 primary + 2 secondary)."

        self.model = model
        self.objectives = objectives
        self.eps = eps

        self.domains = Domains()
        self.trials = Trials()

    def run(self, maxiter: int = -1):
        iter = 0

        # TODO: check model status for "ModelStatus.EMPTY"
        print("Initial optimization...")
        self.model.generate()
        self.model.optimize()
        iter += 1

        self.trials.schedule({dim: None for dim in self.objectives[1:]})
        trial = self.trials.pop()
        self.trials.complete(trial, {dim: self.model.results.objectives[dim] for dim in self.objectives})

        add_obj_threshold_constraint(
            self.model.core,
            self.objectives[0],
            (1 + self.eps) * self.trials.get_solutions()[0][self.objectives[0]],
        )
        self.model.optimize()

        for d in self.objectives[1:]:
            self.trials.schedule({dim: (+1.0 if dim == d else 0.0) for dim in self.objectives[1:]})
            self.trials.schedule({dim: (-1.0 if dim == d else 0.0) for dim in self.objectives[1:]})

        # TODO: this is not really efficient, it just prevents "line"-like domains from "stalling" the algorithm
        self.trials.schedule({dim: (1 / len(self.objectives[1:])) ** 0.5 for dim in self.objectives[1:]})
        self.trials.schedule({dim: -((1 / len(self.objectives[1:])) ** 0.5) for dim in self.objectives[1:]})

        print("Starting NVP iterations ", end="", flush=True)
        while not self.trials.is_empty:
            print(".", end="", flush=True)
            if (maxiter > 0) and (iter >= maxiter):
                print("\nMaximum iterations reached.")
                break

            trial = self.trials.pop()
            set_weighted_objective(self.model.core, trial.direction)
            self.model.optimize()
            iter += 1
            self.trials.complete(trial, {dim: self.model.results.objectives[dim] for dim in self.objectives})

            domain = Domain(self.trials.get_solutions())
            self.domains.append(domain)

            if domain.valid:
                visited = self.trials.get_visited_directions()
                best = (None, -np.inf, None)
                for i in range(len(domain.edges)):
                    edge, length, nv = domain.get_edge(i)
                    nv = dict(zip(self.objectives[1:], nv))
                    dist = min(sum((nv[obj] - v[obj]) ** 2 for obj in self.objectives[1:]) for v in visited)
                    if (dist > 1e-3) and (length > best[1]):
                        best = (edge, length, nv)

                if best[0] is None:
                    print("\nNo new direction found, terminating.")
                    break

                self.trials.schedule(best[2])

        print("\nNVP completed.")

    def iterate(self):
        pass

    def visualize(self):
        return self.domains.plot()

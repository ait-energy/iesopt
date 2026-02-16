import iesopt


add_obj_threshold_constraint = iesopt.IESopt.seval("""
function (model, obj, ub)
    JuMP.@constraint(model, internal(model).model.objectives[obj].expr <= ub)
    return nothing
end
""")

set_weighted_objective = iesopt.IESopt.seval("""
function (model, objs)
    objectives = internal(model).model.objectives
    JuMP.@objective(model, Min, sum(
        objectives[name].expr * weight for (name, weight) in objs
    ))
    return nothing
end
""")

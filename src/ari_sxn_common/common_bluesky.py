from bluesky import plans
from bluesky import plan_stubs

# Note that the dict has the structure {'plan_stub':[alias1, alias2, ...], ...}
_plan_stubs_to_import = {'mv': ['move', 'mv'], 'mvr': ['relative_move', 'mv']}

# Note that the dict has the structure {'plan':[alias1, alias2, ...], ...}
_plans_to_import = {'count': ['count'],
                    'scan': ['scan'],
                    'rel_scan': ['relative_scan', 'rel_scan'],
                    'grid_scan': ['grid_scan'],
                    'rel_grid_scan': ['relative_grid_scan', 'rel_grid_scan'],
                    'list_scan': ['list_scan'],
                    'rel_list_scan': ['relative_list_scan', 'rel_list_scan'],
                    'list_grid_scan': ['list_grid_scan'],
                    'rel_list_grid_scan': ['relative_list_grid_scan',
                                           'rel_list_grid_scan'],
                    'log_scan': ['log_scan'],
                    'rel_log_scan': ['relative_log_scan', 'rel_log_scan'],
                    'spiral': ['spiral'],
                    'rel_spiral': ['relative_spiral', 'rel_spiral'],
                    'spiral_fermat': ['spiral_fermat'],
                    'rel_spiral_fermat': ['relative_spiral_fermat',
                                          'rel_spiral_fermat'],
                    'spiral_square': ['spiral_square'],
                    'rel_spiral_square': ['relative_spiral_square',
                                          'rel_spiral_square']}


class PlanCollectorSubClass:
    """
    A class used to initialize child attributes with methods

    Parameters
    ----------
    methods_to_import : {str: func}
        A dictionary mapping method names to methods for the sub class.
    Attributes
    ----------
    methods : many
        All of the methods specified in methods_to_import
    """
    def __init__(self, methods_to_import):
        for name, function in methods_to_import.items():
            setattr(self, name, function)


class PlanCollector:
    """
    A class used to collect together the plans to be used at ARI and SXN,

    This is a 'collector' class that is designed to hold together the plans that
    are used at both ARI and SXN. It will include all of the builtin
    `bluesky.plans` (but only one alias of each) as well as the builtin
    `bluesky.plan_stubs` mv (as `plan.move`) and mvr (as `plan.relative.move`).
    Note that 'relative' plans that move relative to the current location will
    be grouped in a child `self.relative` object.

    Additional, ARI & SXN specific, plans can/will also be added (see attribute
    list below).

    Parameters
    ----------
    plans_to_import : {str:[str,str,...]}
        The `bluesky.plans` plans to add as methods, has the structure:
            {'plan_name': ['alias 1', 'alias 2', ...]}
        for example:
            {'rel_scan': ['relative_scan', 'rel_scan']}
        Note: only the first alias above will be added to avoid to many options,
        all aliases are in this dict as the same dict is used to populate the
        global namespace versions of these.
    plan_stubs_to_import : {str:[str,str,...]}
        The `bluesky.plan_stubs` plan_stubs to add as methods, has the
        structure:
            {'plan_stub_name': ['alias 1', 'alias 2', ...]}
        for example:
            {'mv': ['move', 'mv']}
        Note: only the first alias above will be added to avoid to many options,
        all aliases are in this dict as the same dict is used to populate the
        global namespace versions of these.


    Attributes
    ----------
    built-ins : many
        All of the built-in plans from `bluesky.plans` (but not aliases) as
        given in plans_to_import and plan_stubs_to_import.

    """
    def __init__(self, plans_to_import, plan_stubs_to_import):
        """
        Initializes the methods from plans_to_import and sub_plans_to_import

        Parameters
        ----------
        plans_to_import : {str:[str,str,...]}
            The `bluesky.plans` plans to add as methods, has the structure:
                {'plan_name': ['alias 1', 'alias 2', ...]}
            for example:
                {'rel_scan': ['relative_scan', 'rel_scan']}
            Note: only the first alias above will be added to avoid to many
            options, all aliases are in this dict as the same dict is used to
            populate the global namespace versions of these.
        plan_stubs_to_import : {str:[str,str,...]}
            The `bluesky.plan_stubs` plan_stubs to add as methods, has the
            structure:
                {'plan_stub_name': ['alias 1', 'alias 2', ...]}
            for example:
                {'mv': ['move', 'mv']}
            Note: only the first alias above will be added to avoid to many
            options, all aliases are in this dict as the same dict is used to
            populate the global namespace versions of these.
        """
        # create the plan methods
        relative_plans_to_import = {}
        for plan, aliases in plans_to_import.items():
            if plan.startswith('rel_'):
                name = aliases[0].split('_', 1)[1]
                relative_plans_to_import[name] = getattr(plans, plan)
            else:
                setattr(self, aliases[0], getattr(plans, plan))

        # create the plan_stub methods
        for plan_stub, aliases in plan_stubs_to_import.items():
            if plan_stub.startswith('rel_'):
                name = aliases[0].split('_', 1)[1]
                relative_plans_to_import[name] = getattr(plan_stubs, plan_stub)
            else:
                setattr(self, aliases[0], getattr(plan_stubs, plan_stub))

        # add the relative scan subclass
        self.relative = PlanCollectorSubClass(relative_plans_to_import)

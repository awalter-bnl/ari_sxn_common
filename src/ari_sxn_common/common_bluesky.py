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


class PlanCollectorSub:
    """
    A class used to initialize child attributes with methods for PlanCollector's

    This class is to be used with the `PlanCollector` class when you want to add
    an extra level of plans that contain no child collections, only child plans.

    Parameters
    ----------
    methods_to_import : {str: func}
        A dictionary mapping method names to methods for the sub class.
    name : str
        The name of the sub-class, usually matches this instances attribute name
    parent : PlanCollector
        The plan collector object that is this instances parent.

    Attributes
    ----------
    name : str
        The name of this instance
    parent : PlanCollector
        The plan collector object that is this instances parent.

    Methods
    _______
    methods : many
        All of the methods specified in methods_to_import
    __str__() :
        Returns a user friendly formatted string showing the structure of the
        instance including all of the methods from methods_to_import but not
        the 'name' or 'parent' attributes.
    __dir__() :
        Returns a list of attribute name strings to be used to define what
        options are available when doing tab-to-complete.
    """
    def __init__(self, methods_to_import, name, parent):
        for plan_name, function in methods_to_import.items():
            setattr(self, plan_name, function)

        self.name = f'{parent.name}_{name}'
        self.parent = parent

    def __str__(self):
        """
        A custom __str__ method that prints a formatted list of plans.

        This method is designed to print a formatted list of plans associated  with
        this sub-class that has no lower subclasses.

        Returns
        -------
        output: str
            A formatted string that should be printed when using print(self)
        """
        output = f'\n{self.name}:'
        for name, plan in self.__dict__.items():
            if name not in ['name', 'parent']:
                description = plan.__doc__.split('\n')[0].strip() \
                    if plan.__doc__.split('\n')[0] else (
                    plan.__doc__.split('\n')[1].strip())

                output += f'\n    {name}:    {description}'

        return output

    def __dir__(self):
        """
        Used to limit the number of options when using tab to complete.

        This method is used to give the list of options when using pythons tab
        to complete process. It gives all of the method attributes but not the
        'name' and 'parent' attributes.

        Returns
        -------
        attribute_list : list[str]
            A list of attribute names to be included when using tab-to-complete
        """
        attribute_list = [plan for plan in self.__dict__.keys()
                          if plan not in ['name', 'parent']]

        return attribute_list



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
     name : str
        The name of the sub-class, usually matches this instances attribute name

    Attributes
    ----------
    built-ins : many
        All of the built-in plans from `bluesky.plans` (but not aliases) as
        given in plans_to_import and plan_stubs_to_import.
     name : str
        The name of the sub-class, usually matches this instances attribute name

    Methods
    _______
    methods : many
        All of the built-in plans from `bluesky.plans` (but not aliases) as
        given in plans_to_import and plan_stubs_to_import.
    __str__() :
        Returns a user friendly formatted string showing the structure of the
        instance including all of the methods from plans_to_import,
        plan_stubs_to_import and any PlanCollectorSub attributes but not the
        'name' attribute.
    __dir__() :
        Returns a list of attribute name strings to be used to define what
        options are available when doing tab-to-complete.
    """
    def __init__(self, plans_to_import, plan_stubs_to_import, name):
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
        self.name = name

        relative_plans_to_import = {}  # used to separate out relative plans

        # create the plan_stub methods
        for plan_stub, aliases in plan_stubs_to_import.items():
            if plan_stub.startswith('rel_') or plan_stub == 'mvr':
                plan_stub_name = aliases[0].split('_', 1)[1]
                relative_plans_to_import[plan_stub_name] = getattr(plan_stubs,
                                                                   plan_stub)
            else:
                setattr(self, aliases[0], getattr(plan_stubs, plan_stub))

        # create the plan methods
        for plan, aliases in plans_to_import.items():
            if plan.startswith('rel_'):
                plan_name = aliases[0].split('_', 1)[1]
                relative_plans_to_import[plan_name] = getattr(plans, plan)
            else:
                setattr(self, aliases[0], getattr(plans, plan))

        # add the relative scan subclass
        self.relative = PlanCollectorSub(relative_plans_to_import,
                                         name='relative', parent=self)

    def __str__(self):
        """
        A custom __str__ method that prints a formatted list of plans.

        This method is designed to print a formatted list of plans and any
        sub-classes that have plans.

        Returns
        -------
        output: str
            A formatted string that should be printed when using print(self)
        """
        output = f'\n{self.name}:'
        for name, plan in self.__dict__.items():
            if name not in ['name', 'parent']:
                if plan.__dict__:  #if plan has attributes
                    output += f'\n    {plan.__str__().replace(
                        '\n', '\n    ').replace(
                        f'{self.name}_', '')}'
                else:
                    description = plan.__doc__.split('\n')[0].strip() \
                        if plan.__doc__.split('\n')[0] else (
                        plan.__doc__.split('\n')[1].strip())

                    output += f'\n    {name}:    {description}'

        return output

    def __dir__(self):
        """
        Used to limit the number of options when using tab to complete.

        This method is used to give the list of options when using pythons tab
        to complete process. It gives all of the method attributes and any
        PlanCollectorSun attributes but not the 'name' attribute.

        Returns
        -------
        attribute_list : list[str]
            A list of attribute names to be included when using tab-to-complete
        """
        attribute_list = [plan for plan in self.__dict__.keys()
                          if plan not in ['name']]

        return attribute_list
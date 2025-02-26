from hopp.dispatch import (OneCycleBatteryDispatchHeuristic,
                             SimpleBatteryDispatchHeuristic,
                             SimpleBatteryDispatch,
                             NonConvexLinearVoltageBatteryDispatch,
                             ConvexLinearVoltageBatteryDispatch)


class HybridDispatchOptions:
    """

    """
    def __init__(self, dispatch_options: dict = None):
        """
        Class for setting dispatch options through HybridSimulation class.

        Parameters
        ----------
        dispatch_options :
            Contains attribute key, value pairs to change default options.

            dict: {
                'battery_dispatch': str (default='simple'), sets the battery dispatch model to use for dispatch
                    options: ('simple', 'one_cycle_heuristic', 'heuristic', 'non_convex_LV', 'convex_LV'),
                'grid_charging': bool (default=True), can the battery charge from the grid,
                'pv_charging_only': bool (default=False), whether restricted to only charge from PV (ITC qualification)
                'include_lifecycle_count': bool (default=True), should battery lifecycle counting be included,
                'n_look_ahead_periods': int (default=48), number of time periods dispatch looks ahead
                'n_roll_periods': int (default=24), number of time periods simulation rolls forward after each dispatch,
                'log_name': str (default=''), dispatch log file name,
                'is_test' : bool (default=False), if True, simulation stops after solving 10 days for development
                }
        """
        self.battery_dispatch: str = 'simple'
        self.include_lifecycle_count: bool = True
        self.grid_charging: bool = True
        self.pv_charging_only: bool = False
        self.n_look_ahead_periods: int = 48
        self.n_roll_periods: int = 24
        self.log_name: str = ''
        self.is_test: bool = False

        if dispatch_options is not None:
            for key, value in dispatch_options.items():
                if hasattr(self, key):
                    if type(getattr(self, key)) == type(value):
                        setattr(self, key, value)
                    else:
                        raise ValueError("'{}' is the wrong data type.".format(key))
                else:
                    raise NameError("'{}' is not an attribute in {}".format(key, type(self).__name__))

        if self.pv_charging_only and self.grid_charging:
            raise ValueError("Battery cannot be restricted to charge from PV only if grid_charging is enabled")

        self._battery_dispatch_model_options = {
            'one_cycle_heuristic': OneCycleBatteryDispatchHeuristic,
            'heuristic': SimpleBatteryDispatchHeuristic,
            'simple': SimpleBatteryDispatch,
            'non_convex_LV': NonConvexLinearVoltageBatteryDispatch,
            'convex_LV': ConvexLinearVoltageBatteryDispatch}
        if self.battery_dispatch in self._battery_dispatch_model_options:
            self.battery_dispatch_class = self._battery_dispatch_model_options[self.battery_dispatch]
            if 'heuristic' in self.battery_dispatch:
                # FIXME: This should be set to the number of time steps within a day.
                #  Dispatch time duration is not set as of now...
                self.n_roll_periods = 24
                self.n_look_ahead_periods = self.n_roll_periods
        else:
            raise ValueError("'{}' is not currently a battery dispatch class.".format(self.battery_dispatch))

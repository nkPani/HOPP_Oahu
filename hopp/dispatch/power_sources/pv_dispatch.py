from typing import Union
from pyomo.environ import ConcreteModel, Set

import PySAM.Pvsamv1 as Pvsam
import PySAM.Pvwattsv8 as Pvwatts
import PySAM.Singleowner as Singleowner

from hopp.dispatch.power_sources.power_source_dispatch import PowerSourceDispatch


class PvDispatch(PowerSourceDispatch):
    _system_model: Union[Pvsam.Pvsamv1, Pvwatts.Pvwattsv8]
    _financial_model: Singleowner.Singleowner
    """

    """
    def __init__(self,
                 pyomo_model: ConcreteModel,
                 indexed_set: Set,
                 system_model: Union[Pvsam.Pvsamv1, Pvwatts.Pvwattsv8],
                 financial_model: Singleowner.Singleowner,
                 block_set_name: str = 'pv'):
        super().__init__(pyomo_model, indexed_set, system_model, financial_model, block_set_name=block_set_name)


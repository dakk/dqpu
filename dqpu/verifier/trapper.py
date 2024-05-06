# Copyright 2024 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Tuple, List, Optional
from ..q import Circuit, ExperimentResult

class TrapInfo:
    def __init__(self):
        raise Exception('Abstract')

class Trapper:
    """ Trapper class """
    def __init__(self):
        raise Exception('Abstract')
    
    def trap(self, qc: Circuit, level: Optional[int]=None) -> Tuple[Circuit, List[TrapInfo]]:
        """ Add traps to the quantum circuits `qc` """
        raise Exception('Abstract')
    
    def untrap_results(self, traps: List[TrapInfo], results: ExperimentResult) -> ExperimentResult:
        """ Get the results for the original circuit, stripping away trap qubits """
        raise Exception('Abstract')        
    
    def verify(self, traps: List[TrapInfo], results: ExperimentResult) -> bool:
        raise Exception('Abstract')
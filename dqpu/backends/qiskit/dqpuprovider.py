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

from qiskit.providers import ProviderV1 as Provider

from .dqpubackend import DQPUBackend

# from qiskit.providers.providerutils import filter_backends


class DQPUProvider(Provider):
    def __init__(self):
        super().__init__()
        self.backend_list = [DQPUBackend(network="testnet", provider=self)]

    def backends(self, name=None, **kwargs):
        backends = self.backend_list
        if name:
            backends = [backend for backend in backends if backend.name() == name]
        return backends  # filter_backends(backends, filters=filters, **kwargs)

    def __str__(self):
        return "DQPUProvider"

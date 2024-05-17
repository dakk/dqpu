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


from setuptools import find_packages, setup

setup(
    name="dqpu",
    version="0.1",
    description="",
    author="Davide Gessa",
    setup_requires="setuptools",
    author_email="gessadavide@gmail.com",
    packages=["dqpu", "dqpu.q"],
    entry_points={
        "console_scripts": [
            "dqpu=dqpu.main:main",
        ],
    },
    zip_safe=False,
    install_requires=["numpy"],
)


# Copyright 2023-2024 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

import dqpu

setup(
    name="dqpu",
    version=dqpu.__version__,
    python_requires=">= 3.9.2",
    description="",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Davide Gessa",
    setup_requires="setuptools",
    author_email="gessadavide@gmail.com",
    license="Apache 2.0",
    packages=[
        "dqpu",
        "dqpu.q",
        "dqpu.sampler",
        "dqpu.verifier",
        "dqpu.blockchain",
        "dqpu.backends",
        "dqpu.backends.qiskit",
    ],
    zip_safe=False,
    install_requires=open("requirements.txt", "r").read().split("\n"),
    extras_require={},
    entry_points={
        "console_scripts": [
            "dqpu-sim_trap_test_main = dqpu.sim_trap_test_main:main",
            "dqpu-verifier = dqpu.verifiernode:verifier_node",
            "dqpu-sampler = dqpu.samplernode:sampler_node",
            "dqpu-cli = dqpu.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Physics",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/dakk/dqpu",
    project_urls={
        "Bug Tracker": "https://github.com/dakk/dqpu/issues/",
        "Documentation": "https://dakk.github.io/dqpu",
        "Source": "https://github.com/dakk/dqpu",
    },
)

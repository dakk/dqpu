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

import os
import time


def repeat_until_done(f, n_iterations=10, wait_time=5):
    try:
        return f()
    except Exception as e:
        print(e)
        print(f"Function call failed, retrying in {wait_time} seconds ({n_iterations})")
        time.sleep(wait_time)
        return repeat_until_done(f, n_iterations - 1, wait_time)


def create_dqpu_dirs():  # noqa: C901
    try:
        os.mkdir(os.path.expanduser("~/.dqpu/"))
    except FileExistsError:
        pass

    try:
        os.mkdir(os.path.expanduser("~/.dqpu/cache"))
    except FileExistsError:
        pass

    try:
        os.mkdir(os.path.expanduser("~/.dqpu/verifier"))
    except FileExistsError:
        pass

    try:
        os.mkdir(os.path.expanduser("~/.dqpu/verifier/cache/"))
    except FileExistsError:
        pass

    try:
        os.mkdir(os.path.expanduser("~/.dqpu/sampler"))
    except FileExistsError:
        pass

    try:
        os.mkdir(os.path.expanduser("~/.dqpu/sampler/cache"))
    except FileExistsError:
        pass

    return os.path.expanduser("~/.dqpu/")

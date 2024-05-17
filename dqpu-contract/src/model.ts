// Copyright 2024 Davide Gessa
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
import { AccountId } from 'near-sdk-js/lib/types';

export type JobStatus = 'pending-validation' | 'waiting' | 'validating-result' | 'executed' | 'invalid';

export class Job {
    id: string;
    owner_id: AccountId;
    reward_amount: bigint;
    sampler_deposit: bigint;
    status: JobStatus;

    qubits: number;
    depth: number;
    shots: number;

    job_file: string;
    result_file: string;
    trap_file: string;

    verifier_id: AccountId;
    sampler_id: AccountId;
}
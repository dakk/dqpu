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

import { NearBindgen, near, call, view } from 'near-sdk-js';
import { AccountId } from 'near-sdk-js/lib/types';
import { Job, JobStatus } from './model';

@NearBindgen({})
class DQPU {
  // Submit a new quantum job
  @call({payableFunction: true})
  submit_job(){
  }

  // Called by validators, set the validity of a pending job
  @call({})
  set_job_validity(){
  }

  // Submit a result for a waiting job, with the caution
  @call({payableFunction: true})
  submit_job_result(){
  }

  // Called by validators, set the validity of a job result
  @call({})
  set_result_validity(){
  }


  // Get latest quantum job list
  @view({}) 
  get_jobs(): string {
    return '';
  }

  // Get a single quantum job by its id
  @view({}) 
  get_job(): string {
    return '';
  }

  // Get a quantum job status by its id
  @view({}) 
  get_job_status(): JobStatus {
    return 'invalid';
  }

  // Add a verifier
  @call({privateFunction: true})
  add_verifier() {

  }

  // Remove a verifier
  @call({privateFunction: true})
  remove_verifier() {

  }

  // Change contract owner
  @call({privateFunction: true})
  set_owner() {

  }
}
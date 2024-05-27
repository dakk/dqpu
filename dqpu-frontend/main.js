// import * as nearApi from './near-api-js.min.js';

const { createApp } = Vue;
const { createVuetify } = Vuetify;

const NODE_URL = 'https://rpc.testnet.near.org';
const CONTRACT_ID = 'dqpu_7.testnet';

function max(a, b) {
    return a > b ? a : b;
}

async function viewMethod(method, args = {}) {
    const provider = new window.nearApi.providers.JsonRpcProvider({ url: NODE_URL });

    let res = await provider.query({
        request_type: 'call_function',
        account_id: CONTRACT_ID,
        method_name: method,
        args_base64: Buffer.from(JSON.stringify(args)).toString('base64'),
        finality: 'optimistic',
    });
    return JSON.parse(Buffer.from(res.result).toString());
};

async function get_all_jobs(slice, total) {
    let jobs = [];
    for (let i = 0; i < total; i) {
        console.log('getting',i,total,slice)
        const nj = (await viewMethod('get_jobs', { from_index: i, limit: slice }));
        i += nj.length;
        jobs = jobs.concat(nj);
    }
    console.log('All jobs are '+(jobs.length));
    return jobs.reverse();
}


const app = Vue.createApp({
    data() {
        return {
            ipfs_gateway: 'http://51.77.230.39:8080/ipfs/',
            tab: 'joblist',
            jobs: [],
            job_stats: {},
            n_verifiers: 0,
            n_jobs: 0,
            amount_handled: 0,
            verifiers: [],
            samplers: [],
            max_qubits: [[0, 0]],

            loading: false,
            itemsPerPage: 25,
        };
    },
    async mounted() {
        console.log('APP mounted');

        await this.updateData();

        this.timer_table = setInterval(async () => { await this.loadJobs({ page: 0, itemsPerPage: this.itemsPerPage, sortBy: ''}) }, 10000);
        this.timer_stats = setInterval(async () => { await this.updateData() }, 9000);

        await this.updateLeaderboards();
        this.timer_leaderboard = setInterval(async () => { await this.updateLeaderboards() }, 60000);


    },
    methods: {
        async updateLeaderboards() {
            all_jobs = await get_all_jobs(50, this.n_jobs);
    
            const samplers = {};
            const verifiers = {};
            const max_qubits = {};
    
            all_jobs.forEach(element => {
                if (element.sampler_id != '') {
                    if (!(element.sampler_id in samplers))
                        samplers[element.sampler_id] = {
                            sampler_id: element.sampler_id,
                            max_qubits: 0,
                            jobs: 0,
                            reward: 0
                        }
    
                    samplers[element.sampler_id].jobs += 1;
                    samplers[element.sampler_id].reward += parseInt(element.reward_amount);
                    samplers[element.sampler_id].max_qubits = max(element.qubits, samplers[element.sampler_id].max_qubits);
                }
    
                if (element.sampler_id != '') {
                    if (!(element.sampler_id in max_qubits))
                        max_qubits[element.sampler_id] = element.qubits;
                    max_qubits[element.sampler_id] = max(element.qubits, max_qubits[element.sampler_id]);
                }
    
                if (element.verifier_id != '') {
                    if (!(element.verifier_id in verifiers))
                        verifiers[element.verifier_id] = {
                            verifier_id: element.verifier_id,
                            jobs: 0,
                            reward: 0
                        }
    
                    verifiers[element.verifier_id].jobs += 1
                    verifiers[element.verifier_id].reward += parseInt(element.reward_amount) / 10;
                }
            });
    
            this.verifiers = Object.entries(verifiers).map(a => { return a[1]; }).sort((a, b) => { return b.jobs - a.jobs; });
            this.samplers = Object.entries(samplers).map(a => { return a[1]; }).sort((a, b) => { return b.jobs - a.jobs; });
            this.max_qubits = Object.entries(max_qubits).sort((a, b) => { return b[1] - a[1]; });
        },
        async updateData() {
            console.log('Updating data...');
            this.n_jobs = await viewMethod('get_number_of_jobs');
            this.n_verifiers = await viewMethod('get_number_of_verifiers');
            this.amount_handled = await viewMethod('get_handled_amount');
            this.job_stats = await viewMethod('get_jobs_stats');
            console.log('Updated.');
        },
        async loadJobs({ page, itemsPerPage, sortBy }) {
            this.itemsPerPage = itemsPerPage;
            console.log(`loadJobs(${page}, ${itemsPerPage}, ${sortBy})`);

            this.loading = true;
            let nj = [];
            if (itemsPerPage == -1) {
                nj = (await get_all_jobs(50, this.n_jobs));
            } else {
                nj = (await viewMethod('get_latest_jobs', { limit: itemsPerPage })).reverse();
            }
            this.jobs = nj;

            this.loading = false;
        },
        statusIcon(status) {
            switch (status) {
                case 'pending-validation':
                    return { color: 'orange-darken-2', icon: 'fa fa-spell-check' };

                case 'waiting':
                    return { color: 'orange-darken-1', icon: 'fa fa-clock' };

                case 'validating-result':
                    return { color: 'yellow-darken-2', icon: 'fa fa-check' };

                case 'executed':
                    return { color: 'green-darken-2', icon: 'fa fa-check' };

                case 'invalid':
                    return { color: 'red-darken-2', icon: 'fa fa-times' };
            }
        }
    }
});

const vuetify = createVuetify({
    theme: {
        defaultTheme: 'dark'
    }
});
app.use(vuetify).mount('#app');

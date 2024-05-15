// import * as nearApi from './near-api-js.min.js';

const { createApp } = Vue;
const { createVuetify } = Vuetify;

const NODE_URL = 'https://rpc.testnet.near.org';
const CONTRACT_ID = 'dqpu_4.testnet';

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

const app = Vue.createApp({
    data() {
        return {
            tab: 'joblist',
            jobs: [],
            job_stats: {},
            n_verifiers: 0,
            n_jobs: 0,
            amount_handled: 0,
            verifiers: [],
            samplers: [],
            max_qubits: [[0,0]]
        };
    },
    async mounted() {
        console.log('APP mounted');

        console.log('Updating data...');
        this.n_jobs = await viewMethod('get_number_of_jobs');
        this.n_verifiers = await viewMethod('get_number_of_verifiers');
        this.amount_handled = await viewMethod('get_handled_amount');
        this.job_stats = await viewMethod('get_jobs_stats');
        this.jobs = await viewMethod('get_latest_jobs', {limit:1000});

        const samplers = {};
        const verifiers = {};
        const max_qubits = {};

        this.jobs.forEach(element => {
            if (! (element.sampler_id in samplers))
                samplers[element.sampler_id] = 0
            samplers[element.sampler_id] += 1

            if (! (element.sampler_id in max_qubits))
                max_qubits[element.sampler_id] = element.qubits;
            max_qubits[element.sampler_id] = max(element.qubits, max_qubits[element.sampler_id]);

            if (! (element.verifier_id in verifiers))
                verifiers[element.verifier_id] = 0
            verifiers[element.verifier_id] += 1
        });

        this.verifiers = Object.entries(verifiers).sort((a, b) => { return b[1] - a[1]; });
        this.samplers = Object.entries(samplers).sort((a, b) => { return b[1] - a[1]; });
        this.max_qubits = Object.entries(max_qubits).sort((a, b) => { return b[1] - a[1]; });

        this.samplers = this.samplers.map(function(a) {
            return { sampler_id: a[0], jobs: a[1], max_qubits: max_qubits[a[0]] }
        });

        this.verifiers = this.verifiers.map(function(a) {
            return { verifier_id: a[0], jobs: a[1] }
        });

        // console.log(this.verifiers, this.samplers, this.max_qubits)

        console.log('Updated.');
    },
    methods: {
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

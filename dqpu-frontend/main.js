// import * as nearApi from './near-api-js.min.js';

const { createApp } = Vue;
const { createVuetify } = Vuetify;

const NODE_URL = 'https://rpc.testnet.near.org';
const CONTRACT_ID = 'dqpu_4.testnet';

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
            jobs: []

        };
    },
    async mounted() {
        console.log('APP mounted');

        this.jobs = await viewMethod('get_jobs');
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

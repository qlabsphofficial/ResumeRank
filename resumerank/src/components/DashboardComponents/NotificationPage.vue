<template>
    <div id="info-modal-container" v-if="this.modal_visible">
        <div id="info-modal">
            <h1>Congratulations!</h1>
            
            <p><span>Dear {{ this.user_data.firstname }} {{ this.user_data.middlename }} {{ this.user_data.lastname }}</span>,</p>
            <p>We hope this message finds you well.</p>

            <p>
                We are pleased to inform you that we have reviewed your application for the {{ this.job_title }} position at Anvaya Cove Beach and Nature Club. 
                After careful consideration, we are excited to move forward with your application.
            </p>

            <p>
                To proceed with the next steps, please contact our recruitment team using any of the following channels:
            </p>

            <ul>
                <li><h4>Email: members@anvayacove.com</h4></li>
                <li><h4>Phone: 793-9000</h4></li>
            </ul>

            <p>
                We look forward to discussing your application further and answering any questions you might have.
            </p>

            <p>Thank you for your interest in joining our team at Anvaya Cove Beach and Nature Club.</p>
            <p>Best regards,</p>

            <h4 class="recruiter-info">Justine Mae S. Payot</h4>
            <h4 class="recruiter-info">Human Resource Assistant</h4>
            <h4 class="recruiter-info">Anvaya Cove Beach and Nature Club</h4>

            <button @click="closeInfoModal()" id="modal-close-button">Close</button>
        </div>
    </div>

    <div id="container" class="fade-in-top">
        <h1>Notifications</h1>

        <div id="notifications">
            <h2>Recent Notifications</h2>

            <h3 v-if="all_notifs.length == 0">No Notifications.</h3>

            <div id="all-notifs" v-else>
                <div v-for="notif in all_notifs" :key="notif" class="notif" @click="showNotifInfo(notif.job_title, notif.message)">
                    <h3>{{ notif.message }}</h3>

                    <div class="notif-info">
                        <p class="date-posted">{{ notif.date_posted }}</p>
                        <p v-if="notif.message === 'Application Reviewed'">The recruiter wants to move forward with your application.</p>
                        <p v-else>The recruiter has decided not to push through with your application.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'NotificationPage',
    props: {
        user_data: {}
    },
    methods: {
        async getNotifications(){
            const notifs_response = await fetch(`${ current_address }/show_notifications?id=${ this.$route.params.user_id }`);
            const notifs_data = await notifs_response.json();

            console.log(notifs_data);

            if (notifs_response.ok) {
                this.all_notifs = notifs_data.notifications;
            }
            else {
                console.log('Retrieval of Notifications Failed.');
            }
        },

        async readNotifications(){
            await fetch(`${ current_address }/read_notifications?id=${ this.$route.params.user_id }`);
        },

        async showNotifInfo(job_title, notif_message) {
            if (notif_message == "Application Reviewed"){
                this.modal_visible = true;
                this.job_title = job_title;
            }
        },

        closeInfoModal() {
            this.modal_header = '';
            this.modal_message = '';
            this.modal_visible = false;
        }
    },
    data (){
        return {
            all_notifs: [],

            job_title: '',
            modal_header: '',
            modal_message: '',
            modal_visible: ''
        }
    },
    mounted() {
        this.getNotifications();
        this.readNotifications();
    }
}
</script>

<style scoped lang="scss">
@import '@/assets/global/styles.scss';

#info-modal-container {
    height: 100vh;
    width: 100vw;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, .4);
    z-index: 3;
}

#info-modal {
    height: 90vh;
    width: 50vw;
    overflow-y: scroll;
    padding-top: 2.5vh;
    padding-bottom: 2.5vh;
    padding-left: 5vw;
    padding-right: 5vw;
    display: flex;
    flex-direction: column;
    text-align: left;
    border-radius: 15px;
    background-color: white;

    h4 {
        line-height: 0;
    }
}

#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#notifications {
    height: 85%;
    width: 100%;
    margin-top: 3%;
}

#all-notifs {
    height: 100%;
    width: 96%;
    margin-top: 3%;
    overflow-y: scroll;
}

.notif {
    height: 15%;
    width: 90%;
    display: block;
    background-color: white;
    margin-top: 2%;
    margin-bottom: 2%;
    padding: 1%;
    padding-left: 3%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px #AEAEAE;
    transition: .4s;
    cursor: pointer;

    h3 {
        line-height: 0;
    }
}

.notif:hover {
    transform: translateY(-5%);
}

.notif-info {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
}

#all-notifs::-webkit-scrollbar {
    width: 8px;
    border-radius: 15px;
    background-color: #EEE;
    scroll-behavior: smooth;
}

#all-notifs::-webkit-scrollbar-thumb {
    background-color: #B8C3C6;
    border-radius: 15px;
}

#modal-close-button {
    margin-top: 5%;
}
</style>
<template>
    <div id="container">
        <h2>Users</h2>

        <table>
            <th>Username</th>
            <th>First Name</th>
            <th>Middle Name</th>
            <th>Last Name</th>
            <th>Contact Number</th>
            <th>E-mail</th>
            <th></th>

            <tr v-for="user in users" :key="user">
                <td>{{ user.username }}</td>
                <td>{{ user.first_name }}</td>
                <td>{{ user.middle_name }}</td>
                <td>{{ user.last_name }}</td>
                <td>{{ user.contact }}</td>
                <td>{{ user.email }}</td>
                <td><button>View Profile</button></td>
            </tr>
        </table>
    </div>
</template>

<script>
import current_address from '@/address';

export default {
    name: 'UserReports',
    props: {
        user_data: {}
    },
    methods: {
        async retrieve_users(){
            
        }
    },
    data (){
        return {
            users: [],

            modal_header: '',
            modal_message: '',
            modal_visible: ''
        }
    },
    mounted() {
        this.retrieve_users();
    }
}
</script>

<style scoped lang="scss">
@import '@/assets/global/styles.scss';


</style>
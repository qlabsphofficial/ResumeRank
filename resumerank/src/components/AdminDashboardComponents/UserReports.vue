<template>
    <div id="container">
        <h1>Users</h1>
        <hr>

        <div id="users-container">
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
            const response = await fetch(`${current_address}/show_users`);
            const data = await response.json();

            if (data.response == 'User Retrieval Success'){
                
                this.users = data.users;
                console.log(this.users);
            }
            else{
                console.log(`Request failed with status ${response.status}`);
            }
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
#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#users-container {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: row;
    overflow-y: scroll;
}
</style>
<template>
    <div id="container">
        <h1>Notifications</h1>

        <div id="notifications">
            <h2>Recent Notifications</h2>

            <h3 v-if="all_notifs.length == 0">No Notifications.</h3>

            <div id="all-notifs" v-else>
                <div v-for="notif in all_notifs" :key="notif" class="notif">
                    <h1></h1>
                    <p></p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'NotificationPage',
    data (){
        return {
            all_notifs: []
        }
    }
}
</script>

<style scoped lang="scss">
#container {
    height: 100%;
    width: 100%;
    text-align: left;
}

#notifications {
    height: 70%;
    width: 100%;
    margin-top: 3%;
}

#all-notifs {
    height: 96%;
    width: 96%;
    margin-top: 1%;
    overflow-y: scroll;
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
</style>
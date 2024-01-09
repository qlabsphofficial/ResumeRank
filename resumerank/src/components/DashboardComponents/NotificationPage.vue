<template>
    <div id="container">
        <h1>Notifications</h1>
        <p>Alerts at a Glance: Your Notification Nexus.</p>

        <div id="notifications">
            <h2>Recent Notifications</h2>

            <div id="all-notifs">
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
                <p>Sample Notification</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'NotificationPage',
    data (){

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
    padding: 2%;
    border-radius: 15px;
    box-shadow: 2px 2px 2px 2px #AEAEAE;
    overflow-y: scroll;
}
</style>
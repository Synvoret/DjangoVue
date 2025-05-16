
<script setup>
    import { ref, onMounted } from 'vue';

    const users = ref([]);

    onMounted(async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/api/users/');
            if (!response.ok) throw new Error('Network response was not ok');
            users.value = await response.json();
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    });
    // console.log(users)
</script>

<template>
    <ol>
        <li v-for="user in users" :key="user.id">
            <p>/ {{ user.username }} </p>
            <p>/ {{ user.email }}</p>
            <p>/ {{ user.date_joined }}</p>
        </li>
    </ol>
</template>

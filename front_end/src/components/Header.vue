<script setup>
    import NavBar from './NavBar.vue';
</script>

<template>
    <header>
        <div class="wrapper">
            <h1>App</h1>
            <NavBar />
        </div>
    </header>
</template>

<style scoped>
    h1 {
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    header {
        border-bottom: 1px solid #ccc;
    }
    .wrapper {
        padding: 1rem;
    }
</style>

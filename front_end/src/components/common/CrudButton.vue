<template>
    <button :class="buttonClass" @click="handleClick">{{ label }}</button>
</template>

<script setup>
    import { defineProps } from 'vue';

    const props = defineProps({
        label: String,
        buttonClass: String,
        action: Function,
    });

    const handleClick = () => {
        if (props.action) {
            props.action();
        }
    };
</script>

<style scoped>
    :hover {
        font-weight: bold;
        font-style: italic;
        text-decoration: underline;
    }
    .create:hover {
        color: green;
    }
    .edit:hover {
        color: blue;
    }
    .edited:hover {
        color: cyan;
    }
    .cancel:hover {
        color: orange;
    }
    .delete:hover {
        color: red;
    }
    .login:hover {
        color: yellow;
    }
    .register:hover {
        color: darkkhaki;
    }
</style>
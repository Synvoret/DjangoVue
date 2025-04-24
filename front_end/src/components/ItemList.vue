<script setup>
    import { ref } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag"; 

    const props = defineProps({
        items: {
            type: Array,
        },
        refetch: {
            type: Function,
            required: false,
        }
    });

    const localItems = ref([...props.items]);
    const isCreating = ref(false);
    const newItem = ref({ name: '', description: '' });
    const { mutate: createItem } = useMutation(
        gql`
            mutation CreateItem($name: String!, $description: String!) {
                createItem(name: $name, description: $description) {
                    item {
                        id
                        name
                        description
                    }
                }
            }
        `);
    function creatingItem() {
        isCreating.value = true;
    }
    async function saveNewItem() {
        if (!newItem.value.name || !newItem.value.description ) return;
        try {
            const response = await createItem({
                name: newItem.value.name,
                description: newItem.value.description,
            });
            if (props.refetch) {
                await props.refetch();
            };
            const createdItem = response.data.createItem.item;
            localItems.value.push(createdItem);
            newItem.value = { name: '', description: ''};
            isCreating.value = false;
        } catch (error) {
            console.error("GraphQL Error:", error)
        }
    }
</script>

<template>
    <!-- <ol class="item-list">
        <li class="item" v-for="item in items" :key="item.id">
            {{ item.name }} {{ item.description }}
        </li>
    </ol> -->
    <table class="item-list">
        <thead>
            <tr>
                <th>Poz.</th>
                <th>Name</th>
                <th>Description</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr class="item" v-for="(item, index) in items" :key="item.id">
                <td>{{ index + 1 }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.description }}</td>
                <td>
                    <button class="edit">E</button>
                    <button class="delete">D</button>
                </td>
            </tr>
            <tr class="item" v-if="isCreating">
                <td>{{ items.length + 1 }}</td>
                <td><input v-model="newItem.name" placeholder="name" autofocus/></td>
                <td><input v-model="newItem.description" placeholder="decription" /></td>
                <td>
                    <button class="create" @click="saveNewItem">V</button>
                </td>
            </tr>
            <tr class="item" v-else>
                <td>{{ items.length + 1 }}</td>
                <td></td>
                <td></td>
                <td>
                    <button class="create" @click="creatingItem">C</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>

    table, th, td {
        border: 1px dotted black;
        border-collapse: collapse;
        text-align: center;
    }

    button.edit:hover {
        color: blue;
    }
    button.delete:hover {
        color: red;
    }
    button.create:hover {
        color: green;
    }
    button:hover {
        font-weight: bold;
        font-style: italic;
        text-decoration: underline;
    }

    input {
        width: 80px;
        box-sizing: border-box;
        cursor: text;
    }

</style>
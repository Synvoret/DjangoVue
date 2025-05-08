<script setup>
    import { ref, inject } from 'vue';
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
    const editingItem = ref(null);
    const editedItem = ref({ name: '', description: ''});
    const currentUser = inject('currentUser');
    const isAuthenticated = inject('isAuthenticated');
    
    const { mutate: createItem } = useMutation(
        gql`
            mutation CreateItem($name: String!, $description: String!) {
                createItem(name: $name, description: $description) {
                    item {
                        id
                        name
                        description
                        author {
                            user {
                                username
                            }
                        }
                    }
                }
            }
        `);
    const { mutate: updateItem } = useMutation(
        gql`
            mutation UpdateItem($id: ID!, $name: String!, $description: String!) {
                updateItem(id: $id, name: $name, description: $description) {
                    item {
                        id
                        name
                        description
                    }
                }
            }
        `);
    const { mutate: deleteItem } = useMutation(
        gql`
            mutation DeleteItem($id: ID!) {
                deleteItem(id: $id) {
                    success
                }
            }
        `);
    function creatingItem() {
        isCreating.value = true;
    };
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
            console.error("GraphQL Error:", error);
        }
    };
    function cancelCreating() {
        isCreating.value = false;
        newItem.value = { name: '', description: ''};
    };
    function startEditing(item) {
        editingItem.value = item.id;
        editedItem.value = { ...item };
    }
    async function saveEditedItem() {
        if (!editedItem.value.name || !editedItem.value.description) return;
        try {
            const response = await updateItem({
                id: editingItem.value,
                name: editedItem.value.name,
                description: editedItem.value.description,
            });
            if (props.refetch) {
                await props.refetch();
            };
            const updatedItem = response.data.updateItem.item;
            const index = localItems.value.findIndex(item => item.id === updateItem.id);
            localItems.value[index] = updatedItem;
            editingItem.value = null;
            editedItem.value = { name: '', description: ''};
        } catch (error) {
            console.error("GraphQL error:", error);
        }
    }
    function cancelEditing() {
        editingItem.value = null;
        editedItem.value = { name: '', description: ''};
    }
    async function removeItem(itemId) {
        try {
            const response = await deleteItem({ id: itemId });
            if (response.data.deleteItem.success && props.refetch) {
                await props.refetch();
                localItems.value = localItems.value.filter(item => item.id !== itemId);
            } else {
                console.error("GraphQL Error:");
            }
        } catch (error) {
            console.error("GraphQL Error:", error);
        }
    }
</script>

<template>
    <table class="item-list">
        <thead>
            <tr>
                <th>Poz.</th>
                <th>Name</th>
                <th>Description</th>
                <th>Author</th>
                <th v-if="isAuthenticated">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr class="item" v-for="(item, index) in items" :key="item.id">
                <td>{{ index + 1 }}</td>
                <td v-if="editingItem === item.id"><input v-model="editedItem.name"/></td>
                <td v-else>{{ item.name }}</td>
                <td v-if="editingItem === item.id"><input v-model="editedItem.description"/></td>
                <td v-else>{{ item.description }}</td>
                <td>{{ item.author.user.username }}</td>
                <td v-if="isAuthenticated">
                    <button class="edited" v-if="editingItem === item.id" @click="saveEditedItem">A</button>
                    <button class="cancel" v-if="editingItem === item.id" @click="cancelEditing">X</button>
                    <button class="edit" v-else @click="startEditing(item)">E</button>
                    <button class="delete" @click="removeItem(item.id)">D</button>
                </td>
            </tr>
            <tr class="item" v-if="isCreating">
                <td>{{ items.length + 1 }}</td>
                <td><input v-model="newItem.name" placeholder="*name" autofocus/></td>
                <td><input v-model="newItem.description" placeholder="*decription"/></td>
                <td style="color: orange;">{{ currentUser }}</td>
                <td v-if="isAuthenticated">
                    <button class="create" @click="saveNewItem">A</button>
                    <button class="cancel" @click="cancelCreating">X</button>
                </td>
            </tr>
            <tr class="item" v-else-if="isAuthenticated">
                <td>{{ items.length + 1 }}</td>
                <td></td>
                <td></td>
                <td></td>
                <td>
                    <button class="create" @click="creatingItem">C</button>
                </td>
            </tr>
        </tbody>
    </table>
    <div><label class="required" v-if="!isAuthenticated">  If You want edit table, please login...</label></div>
    <div v-if="isAuthenticated">
        <label class="required">A - Accept </label>
        <label class="required">C - Create </label>
        <label class="required">D - Delete </label>
        <label class="required">E - Edit </label>
        <label class="required">X - Cancel</label>
    </div>
    <div><label class="required" v-if="isCreating">* - required</label></div>
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
    button.edited:hover {
        color: cyan;
    }
    button.cancel:hover {
        color: orange;
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

    label.required {
        font-size: 12px;
        font-style: italic;
    }

</style>

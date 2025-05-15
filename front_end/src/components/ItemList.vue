<script setup>
    import { ref, inject, computed, watch } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag";
    import CrudButton from './common/CrudButton.vue';

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
    watch(() => props.items, (newItems) => {
        localItems.value = [...newItems];
    });
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
                        author {
                            user {
                                username
                            }
                        }
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
        editingItem.value = null;
    };
    async function saveNewItem() {
        if (!newItem.value.name || !newItem.value.description ) return;
        try {
            const response = await createItem({
                name: newItem.value.name,
                description: newItem.value.description,
            });
            const createdItem = response.data.createItem.item;
            localItems.value.push(createdItem);
            newItem.value = { name: '', description: ''};
            isCreating.value = false;
            // set last page pagination after save item
            if (itemsPerPage.value === 'all') {
                currentPage.value = Math.ceil(localItems.value.length / itemsPerPage.value);
            } else {
                currentPage.value = Math.ceil(localItems.value.length / itemsPerPage.value);
            }
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
        isCreating.value = false;
    }
    async function saveEditedItem() {
        if (!editedItem.value.name || !editedItem.value.description) return;
        try {
            const response = await updateItem({
                id: editingItem.value,
                name: editedItem.value.name,
                description: editedItem.value.description,
            });
            const updatedItem = response.data.updateItem.item;
            const index = localItems.value.findIndex(item => item.id === editingItem.value);
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
                // await props.refetch();
                localItems.value = localItems.value.filter(item => item.id !== itemId);
                if ((currentPage.value - 1) * itemsPerPage.value >= localItems.value.length && currentPage.value > 1) {
                    currentPage.value -= 1;
                }
            } else {
                console.error("GraphQL Error:");
            }
        } catch (error) {
            console.error("GraphQL Error:", error);
        }
    }

    // PAGINATION
    const currentPage = ref(1);
    const itemsPerPage = ref(5);
    const paginatedItems = computed(() => {
        if (itemsPerPage.value === 'all') {
            return localItems.value;
        };
        const start = (currentPage.value - 1) * itemsPerPage.value;
        const end = start + itemsPerPage.value;
        return localItems.value.slice(start, end);
    });
    const totalPages = computed(() => {
        return Math.ceil(localItems.value.length / itemsPerPage.value);
    })

    function goToPage(page) {
        if (page >= 1 && page <= totalPages.value) {
            currentPage.value = page;
        }
    }
    function displayPosition(index) {
        if (typeof itemsPerPage.value === 'number') {
            return (currentPage.value - 1) * itemsPerPage.value + index + 1;
        } else {
            return index + 1;
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
            <tr class="item" v-for="(item, index) in paginatedItems" :key="item.id">
                <td>{{ displayPosition(index) }}</td>
                <td v-if="editingItem === item.id"><input v-model="editedItem.name"/></td>
                <td v-else>{{ item.name }}</td>
                <td v-if="editingItem === item.id"><input v-model="editedItem.description"/></td>
                <td v-else>{{ item.description }}</td>
                <td>{{ item.author.user.username }}</td>
                <td v-if="isAuthenticated" class="button-container">
                    <CrudButton v-if="editingItem === item.id" label="A" buttonClass="edited" @click="saveEditedItem"/>
                    <CrudButton v-if="editingItem === item.id" label="X" buttonClass="cancel" @click="cancelEditing"/>
                    <CrudButton v-else label="E" buttonClass="edit" @click="startEditing(item)"/>
                    <CrudButton label="D" buttonClass="delete" @click="removeItem(item.id)"/>
                </td>
            </tr>
            <tr class="item" v-if="isCreating">
                <td>{{ localItems.length + 1  }}</td>
                <td><input v-model="newItem.name" placeholder="*name" autofocus/></td>
                <td><input v-model="newItem.description" placeholder="*description"/></td>
                <td style="color: orange;">{{ currentUser }}</td>
                <td v-if="isAuthenticated" class="button-container">
                    <CrudButton label="A" buttonClass="create" @click="saveNewItem"/>
                    <CrudButton label="X" buttonClass="cancel" @click="cancelCreating"/>
                </td>
            </tr>

            <tr class="item" v-else-if="isAuthenticated">
                <td>{{ localItems.length + 1 }}</td>
                <td></td>
                <td></td>
                <td></td>
                <td class="button-container">
                    <CrudButton label="C" buttonClass="create" @click="creatingItem"/>
                </td>
            </tr>

        </tbody>
    </table>
    <div>
        <label class="required" v-if="!isAuthenticated">  If You want edit table, please login...</label>
    </div>
    <div v-if="isAuthenticated">
        <label class="required">A - Accept </label>
        <label class="required">C - Create </label>
        <label class="required">D - Delete </label>
        <label class="required">E - Edit </label>
        <label class="required">X - Cancel</label>
    </div>
    <div>
        <label class="required" v-if="isCreating">* - required</label>
    </div>

    <div class="button-container" v-if="totalPages > 1">
        <CrudButton label="Previous" buttonClass="first" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1"/>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <CrudButton label="Next" buttonClass="last" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages"/>
    </div>

    <div class="button-container">
        <label for="itemsPerPage">Items per page </label>
        <select id="itemsPerPage" v-model="itemsPerPage">
            <option v-for="n in [5, 10, 15, 20]" :key="n" :value="n">{{ n }}</option>
            <option value="all">All</option>
        </select>
    </div>

</template>

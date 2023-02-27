<template>
  <div>
    <div>
        <v-data-table :headers="headers" :items="items" :loading="tableloader" :items-per-page="itemsperpage" class="elevation-1"></v-data-table>
    </div>
  </div>
</template>

<script>
export default {
    props: {
        headers: { default: [] },
        items: { default: [] },
        itemsperpage: { default: 10 },
        tableloader : { default: false },
    },
}
</script>
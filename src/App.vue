<template>
    <div id="app">
        <ul>
            <li v-for="area in areas" v-bind:key="area.name">
                {{ area.name }}
                <ul>
                    <li v-for="drop in area.drops" v-bind:key="drop.id">
                        {{ itemIDToItemName(drop.id) }}
                    </li>
                </ul>
            </li>
        </ul>
    </div>
</template>

<script>
import Areas from "./components/areas.json";
import Items from "./components/items.json";

export default {
    name: "app",
    data: function() {
        return {
            areas: Areas.areas,
            items: Items.items
        };
    },
    methods: {
        itemIDToItemName: function(itemID) {
            for (let item of this.items) {
                if (itemID === item.id) {
                    return item.name;
                }
            }
        }
    }
};
</script>

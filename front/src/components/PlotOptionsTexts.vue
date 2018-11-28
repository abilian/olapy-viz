<template>
  <div>

    <v-expansion-panel>
      <v-expansion-panel-content>
        <div slot="header">
          <b>
            <span>Plot Options Texts</span>
          </b>
        </div>
        <v-card>
          <v-card-text>


            <div>
              <label>
                <input placeholder="Title" class="form-control" @input="$emit('plotLegend', $event.target.value)"/>
              </label>
              <br>
              <label>
                <input placeholder="X axis title" class="form-control"
                       @input="$emit('XAxisLabel', $event.target.value)"/>
              </label>
              <br>
              <label>
                <input placeholder="Y axis title" class="form-control"
                       @input="$emit('YAxisLabel', $event.target.value)"/>
              </label>

            </div>

            <div>
              <div>
                <span class="badge badge-secondary">Orientation</span>
                <!--<span>Orientation: </span>-->
              </div>
              <div v-for="y_location in YAxisLocations" class="form-check form-check-inline">
                <input class="form-check-input" type="radio" :id="y_location" :value="y_location" v-model="YLocation">
                <label class="form-check-label" :for="y_location">{{y_location}}</label>
              </div>
            </div>


          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>

</template>

<script>

  import "vue-swatches/dist/vue-swatches.min.css"


  export default {
    name: "PlotOptions",
    data() {
      return {
        YAxisLocations: ['left', 'right'],
        YLocation: 'left'
      }
    },
    watch: {
      YLocation(value) {
        this.$emit('YAxisLocation', value)
      }
    }
  }

</script>

<style scoped>
</style>

<template>
  <div>
    <v-expansion-panel>
      <v-expansion-panel-content>
        <div slot="header">
          <b>
            <span>Plot Options Data</span>
          </b>
        </div>
        <v-card>
          <v-card-text>
            <v-container fluid grid-list-lg>
              <v-layout row wrap>
                <v-flex xs12>
                  <v-slider
                    label="Line size"
                    v-model="circleSize"
                    :max="100"
                    :min="2"
                    :step="10"
                    @change="$emit('circleSize', circleSize)"
                  ></v-slider>
                </v-flex>
              </v-layout>
            </v-container>


            <div>
              <table v-if="Object.keys(pickedColor).length > 0">
                <tr>
                  <td>

                    <h6>
                      <label for="FormControlSelect">
                        <span class="badge badge-secondary">Colors : </span>
                      </label>
                    </h6>

                  </td>
                  <td>
                  </td>
                </tr>
                <tr v-for="(value, key, index) in pickedColor">
                  <td style="width: 80%; padding: 0 10%;">
                    {{key}}
                  </td>
                  <td>
                    <swatches style="float: right" v-model="pickedColor[key]" shapes="circles" popover-to="right"/>
                  </td>
                </tr>

              </table>

            </div>


            <div class="form-group">
              <h6 style="margin: 5% 0">
                <label for="FormControlSelect">
                  <span class="badge badge-secondary">Line style : </span>
                </label>
                <select style="float: right; width: 50%;" class="form-control" v-model="lineStyle"
                        id="FormControlSelect">
                  <option>Solid</option>
                  <option>Dashed</option>
                  <option>Dotted</option>
                  <option>Dotdash</option>
                  <option>Dashdot</option>
                </select>
              </h6>

            </div>


          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>

</template>

<script>

  import Swatches from 'vue-swatches'
  import "vue-swatches/dist/vue-swatches.min.css"
  import axios from 'axios';

  export default {
    name: "PlotOptions",
    props: {
      plotProps: Object
    },
    data() {
      return {
        circleSize: 2,
        lineStyle: 'solid',
        color_elements: []
      }
    },
    computed: {
      pickedColor() {
        let colors = {};
        let color_element = [];
        if (this.plotProps.ColorByColumn.length > 0) {
          color_element = this.color_elements[0];
        } else {
          for (let idx in this.plotProps.Y_axis) {
            color_element.push(Object.keys(this.plotProps.Y_axis[idx])[0])
          }
        }

        for (let idx in color_element) {
          colors[color_element[idx]] = this.generator_random_color()
        }
        return colors
      }
    },
    methods: {
      generator_random_color: function (event) {
        return '#' + (Math.random() * 0xFFFFFF << 0).toString(16);
      }
    },
    components: {
      Swatches
    },
    watch: {
      pickedColor(color) {
        this.$emit('pickedColor', color)
      },
      lineStyle(style) {
        this.$emit('lineStyle', style)
      },
      'plotProps.ColorByColumn': function (val) {
        axios.post("api/get_unique_rows", {'column': val}).then(x => {
          this.color_elements = [x.data];
        });
      },
    }
  }

</script>

<style scoped>
</style>

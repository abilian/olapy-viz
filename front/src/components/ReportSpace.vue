<template>
  <div>
    <div class="toolbox">
      <div class="datasource">

        <button class="btn-add-file" @click="show_import_files=true">
          <i class="fa fa-plus-circle"></i>
        </button>

        <div class="form-group chartType">
          <label>
            <select class="form-control fontawesome" v-model="plotProps.chartType">
              <option value="">Auto</option>
              <option value="vbar">&#xf080;</option>
              <option value="circle">&#xf2a1;</option>
              <option value="line">&#xf201;</option>
              <option value="hex">&#xf1fe;</option>

            </select>
          </label>
        </div>

      </div>

      <div class="all-columns">
        <draggable class="df-columns" v-model="uploadedFilesColumns" :options="{group:'people'}" @start="drag=true"
                   @end="drag=false">
          <div v-for="element in uploadedFilesColumns" :key="Object.keys(element)[0]">

          <span v-if="Object.values(element)[0] === 'object'" class="badge badge-pill badge-warning">
            {{Object.keys(element)[0]}}
          </span>

            <span v-else class="badge badge-pill badge-success">
            {{Object.keys(element)[0]}}
          </span>

          </div>
        </draggable>


        <div class="axis">

          <draggable v-model="plotProps.X_axis" class="dragArea dragAreaX" :options="{group:'people'}">


            <div v-for="element in plotProps.X_axis">
            <span class="badge badge-pill badge-warning">
              {{Object.keys(element)[0]}}
            </span>
            </div>

          </draggable>

          <draggable v-model="plotProps.Y_axis" class="dragArea dragAreaY" :options="{group:'people'}">
            <div v-for="element in plotProps.Y_axis">

            <span class="badge badge-pill badge-success">
              {{Object.keys(element)[0]}}
            </span>

            </div>

          </draggable>

          <draggable v-model="plotProps.ColorByColumn" class="dragArea dragAreaX"
                     :options="{group:'people'}">
            <div v-for="element in plotProps.ColorByColumn">
            <span class="badge badge-pill badge-warning">
              {{Object.keys(element)[0]}}
            </span>
            </div>
          </draggable>


          <draggable v-model="plotProps.SizeByColumn" class="dragArea dragAreaX"
                     :options="{group:'people'}">
            <div v-for="element in plotProps.SizeByColumn">
            <span class="badge badge-pill badge-warning">
              {{Object.keys(element)[0]}}
            </span>
            </div>
          </draggable>


        </div>
      </div>


    </div>

    <files-uploader @uploadedFilesColumns="uploadedFilesColumns = $event"
                    v-show="show_import_files"></files-uploader>

    <div class="workspace">
      <bokeh-plot :plot="plot"></bokeh-plot>
    </div>


    <div v-show="plot && Object.values(plot)[0]" class="chartsProperties">

      <plot-options-texts class="plotoptions"
                          @plotLegend="plotProps.plotLegend = $event"
                          @XAxisLabel="plotProps.x_axis_label = $event"
                          @YAxisLabel="plotProps.y_axis_label = $event"
                          @YAxisLocation="plotProps.YAxisLocation = $event">

      </plot-options-texts>


      <plot-options-data class="plotoptions"
                         :plotProps="plotProps"
                         @lineStyle="plotProps.lineStyle = $event"
                         @circleSize="plotProps.circleSize = $event"
                         @pickedColor="plotProps.pickedColor = $event">

      </plot-options-data>


    </div>

  </div>
</template>

<script>
  import draggable from 'vuedraggable'
  import filesUploader from "./files-uploader.vue";
  import PlotOptionsTexts from './PlotOptionsTexts'
  import PlotOptionsData from './PlotOptionsData'
  import BokehPlot from './BokehPlot'
  import axios from 'axios';

  export default {
    data() {
      return {
        show_import_files: false,
        uploadedFilesColumns: [],
        plot: {},
        plotProps: {
          X_axis: [],
          Y_axis: [],
          ColorByColumn: [],
          SizeByColumn: [],
          chartType: '',
          circleSize: 2,
          pickedColor: {},
          plotLegend: '',
          lineStyle: 'solid',
          x_axis_label: '',
          y_axis_label: '',
          YAxisLocation: 'left'
        },
      }
    },
    components: {
      filesUploader,
      draggable,
      BokehPlot,
      PlotOptionsTexts,
      PlotOptionsData
    },
    watch: {
      plotProps: {
        handler(val) {
          axios.post("api/get-plot", val).then(x => {
            this.plot = x.data;
          })
        },
        deep: true
      }
    },
    mounted() {
      axios.get("api/get-plot").then(x => {
        this.plot = x.data;
      })
    }
  }
</script>

<style scoped>
  .toolbox {
    margin: 2% 1%;
    width: 97%;
    height: 125px;
    border: inset;
  }

  .toolbox div {
    float: left;
    position: relative;
  }

  .datasource {
    position: relative;
    margin: 1% 1%;
    height: 75%;
    border: inset;
    width: 64px;
  }

  .df-columns {
    margin: 1% 1%;
    width: 90%;
    height: 30%;
    border: inset;
  }

  .df-columns div {
    float: left;
    margin-left: 10px;
    margin-top: 8px;
    line-height: 0;
  }

  .axis {
    padding: 4px 2px;
    margin: 0 1%;
    width: 90%;
    height: 29%;
    border: inset;
    float: left;
  }

  .axis div {
    margin: 0 2px;
  }

  .workspace {
    position: relative;
    margin: 1%;
    width: 97%;
    height: 370px;
    top: 35%;

  }

  .dragArea {
    width: 24%;
    border: inset;
    height: 100%;
    float: left;
    border-radius: 5px;
    margin: 0 5px;
    line-height: 0;
  }

  .dragAreaX {
    background: rgba(255, 178, 19, 0.1);
  }

  .dragAreaY {
    background: rgba(53, 211, 27, 0.07);
  }

  .chartsProperties {
    position: absolute;
    top: 110px;
    width: 100%;
    margin: 4% 1%;
  }

  .chartsProperties .plotoptions {
    float: left;
    width: 30%;
    padding: 0 1%;
  }

  .chartType {
    margin-left: 2px;
  }


  /* Style buttons */
  .btn-add-file {
    background-color: rgba(0, 214, 68, 0.4); /* Blue background */
    color: white; /* White text */
    cursor: pointer; /* Mouse pointer on hover */
    border-radius: 100%;
    margin: 3px 9px;
    width: 40px;
    height: 40px;
  }

  .btn-add-file:hover {
    background-color: rgba(43, 227, 91, 0.88);
  }

  .fontawesome {
    font-family: FontAwesome, sans-serif;
    cursor: pointer;
  }

  .fontawesome option {
    font-size: 24px
  }

  .all-columns {
    width: 90%;
    height: 100%;
  }
</style>

<template>
  <div>
    <div id="mychart" v-html="plotDiv">
    </div>
  </div>

</template>

<script>
  export default {
    props: {
      plot: Object,
    },
    data() {
      return {
        plotDiv: ''
      }

    },
    watch: {
      plot(new_plot) {
        if (new_plot) {
          this.plotDiv = new_plot.div;
          let div = document.getElementById('mychart');
          let innerDiv = document.createElement('script');
          innerDiv.text = new_plot.script;
          div.insertAdjacentElement("afterend", innerDiv);
        }

      }
    },
  }
</script>

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["<= 1", "1-3", "3-6", "6-12", "12-24", "24-48", "> 48"],
    datasets: [{
      label: "Hours",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: [2, 14, 34, 55, 28, 12, 13],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'hours'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 9
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 60,
          maxTicksLimit: 5
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: false
    }
  }
});

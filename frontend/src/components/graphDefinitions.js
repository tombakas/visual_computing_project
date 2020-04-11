import axios from "axios"

// -- Variables --
const monthMap = {
  1: "Jan",
  2: "Feb",
  3: "Mar",
  4: "Apr",
  5: "May",
  6: "Jun",
  7: "Jul",
  8: "Aug",
  9: "Sep",
  10: "Oct",
  11: "Nov",
  12: "Dec",
}

let chart = null;
let color = Chart.helpers.color;
export let prevStack = [];

let chartData = {
  labels: [],
  datasets: [{
    label: 'Police',
    backgroundColor: Color("#0000FF").alpha(0.5).rgbString(),
    borderColor: Color("#0000FF").alpha(0.8).rgbString(),
    borderWidth: 1,
    data: []
  }, 
  {
    label: 'Ambulance',
    backgroundColor: Color("#FF4400").alpha(0.5).rgbString(),
    borderColor: Color("#FF4400").alpha(0.8).rgbString(),
    borderWidth: 1,
    data: []
  },
  {
    label: 'Fire brigade',
    backgroundColor: Color("#FF0000").alpha(0.5).rgbString(),
    borderColor: Color("#FF0000").alpha(0.5).rgbString(),
    borderWidth: 1,
    data: []
  },
  {
    label: 'Helicopter',
    backgroundColor: Color("#00FF00").alpha(0.5).rgbString(),
    borderColor: Color("#00FF00").alpha(0.8).rgbString(),
    borderWidth: 1,
    data: []
  }
  ]
};

// -- Functions --
export let getCounts = function(url, title) {
  axios
    .get(url)
    .then(result => {
      clearData()
      populate(result)
      if (chart){
        chart.clear()
        chart.destroy()
      }
      create_chart(title)
    })
}

let populate = function(result) {
  for(let entry of result.data) {
    if (!chartData.labels.includes(entry["date"])) {
      chartData.labels.push(entry["date"])
    }
    switch(entry["service"]) {
      case "police":
        chartData.datasets[0].data.push(entry.count);
        break;
      case "ambulance":
        chartData.datasets[1].data.push(entry.count);
        break;
      case "fire-brigade":
        chartData.datasets[2].data.push(entry.count);
        break;
      case "helicopter":
        chartData.datasets[3].data.push(entry.count);
        break;
    }
  }
}

let create_chart = function(title) {
  let ctx = document.getElementById("barChart")
  chart = new Chart(ctx, {
    type: 'bar',
    data: chartData,
    options: get_options(title)
  })
}

let clearData = function() {
  chartData.labels = []
  for(let entry of chartData.datasets) {
    entry.data = []
  }
  if (chart) chart.update();
}

let navigateChart = function (query) {
  if (!query) {
    getCounts(
      "http://localhost:5000/api/calls/count?interval=year", 
      "Yearly call counts of all data points"
    );
  }
  if (/^[0-9]{4}$/.test(query)) {
    let year = query.split(" ")[0]
    getCounts(
      `http://localhost:5000/api/calls/count?interval=month&year=${year}`, 
      `Monthly call counts of ${year}`
    );
  }
  if (/^[0-9]{4} [0-9]{2}$/.test(query)) {
    let year = query.split(" ")[0]
    let month = query.split(" ")[1]
    getCounts(
      `http://localhost:5000/api/calls/count?interval=day&year=${year}&month=${month}`, 
      `Daily call counts of ${monthMap[Number(month)]} of ${year}`
    );
  }
  if (/^[0-9]{4} [0-9]{2} [0-9]{2}$/.test(query)) {
    let year = query.split(" ")[0]
    let month = query.split(" ")[1]
    let day = query.split(" ")[2]
    getCounts(
      `http://localhost:5000/api/calls/count?interval=micro&year=${year}&month=${month}&day=${day}`, 
      `Total call counts for ${day} ${monthMap[Number(month)]} ${year}`
    );
  }
}

export let handleGoBack = function() {
  if (prevStack.length > 0) {
    prevStack.pop()
    navigateChart(prevStack[prevStack.length - 1])
  }
}

let get_options = function (title_text) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    events: ['click', 'mousemove'],
    legend: {
      position: 'top',
    },
    onClick: function(x) {
      if (chart.getElementAtEvent(x).length) {
        let clicked = chartData.labels[chart.getElementAtEvent(x)[0]._index]
        prevStack.push(clicked)
        navigateChart(clicked)
      }
    },
    title: {
      display: true,
      text: title_text
    }
  }
}

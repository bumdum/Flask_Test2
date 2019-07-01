function buildMetadata() {

    // @TODO: Complete the following function that builds the metadata panel
    let url = `/data`;
  
    // Use `d3.json` to fetch the metadata for a sample
    d3.json(url).then(function (response) {
        console.log(response);
      let panel = d3.select('#sample').html("");
  
      Object.entries(response).forEach(([key, value]) => {
        let cell = panel.append('p')
        cell.text(`${key}: ${value}`);
      })
    })
};

function buildLapData() {

  // @TODO: Complete the following function that builds the metadata panel
  let url = `/lap_data`;

  // Use `d3.json` to fetch the metadata for a sample
  d3.json(url).then(function (response) {
      console.log(response);
    let panel = d3.select('#lap').html("");

    Object.entries(response).forEach(([key, value]) => {
      let cell = panel.append('p')
      cell.text(`${key}: ${value}`);
    })
  })
};

    console.log("test")
    buildMetadata()
    buildLapData()
    console.log("ran")
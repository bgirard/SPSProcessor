function enterMainUI() {
  var stats = computeStats(jsonData);
  document.body.appendChild(createHeader("Startup"));
  document.body.appendChild(displayFunctions(stats, jsonData));
}

function createHeader(titleStr) {
  var container = document.createElement("div");
  
  var title = document.createElement("h1");
  title.textContent = titleStr;
  container.appendChild(title);

  return container;

}

function computeStats(data) {
  var min = null;
  var max = null;
  for (var funcName in data) {
    data[funcName].sort(function(a,b) {
      return b.duration - a.duration;
    });
    for (var profileName in data[funcName]) {
      var duration = data[funcName][profileName]["duration"];
      if (min == null) {
        min = duration;
        max = duration;
      }
      min = Math.min(min, duration);
      max = Math.max(max, duration);
    }
  }
  return {
    minTime: min,
    maxTime: max,
  };
}

function displayFunctions(stats, data) {
  var container = document.createElement("div");
  container.className = "functionsDiv";

  for (var funcName in data) {
    var elem = displayFunction(stats, data[funcName], funcName);
    container.appendChild(elem);
  }

  return container;
}

function displayFunction(stats, data, funcName) {
  var container = document.createElement("div");
  
  var title = document.createElement("h2");
  title.textContent = funcName;
  container.appendChild(title);

  var funcContainer = document.createElement("div");
  funcContainer.className = "functionDiv";
  funcContainer.appendChild(createCanvas(stats, data, funcName));
  for (var profileName in data) {
    var profileDiv = document.createElement("div");
    profileDiv.textContent = data[profileName].file + " -> " + data[profileName].duration + "ms";
    //profileDiv.textContent = JSON.stringify(data);
    funcContainer.appendChild(profileDiv);
  }
  container.appendChild(funcContainer);

  return container;
}

function createCanvas(stats, data, funcName) {
  var container = document.createElement("div");

  var lblMin = document.createTextNode("0 ms");
  var lblMax = document.createTextNode(stats.maxTime + " ms");
  var canvas = document.createElement("canvas");
  canvas.width = 300;
  canvas.height = 15;

  var ctx = canvas.getContext("2d");
  ctx.lineWidth = 1;
  for (var i = 0; i < stats.maxTime; i += 10) {
    ctx.beginPath();
    ctx.moveTo(i, 0);
    ctx.lineTo(i, canvas.height);
    ctx.stroke();
  }
  for (var profileName in data) {
    var duration = data[profileName].duration;
    var radius = 3;
    ctx.beginPath();
    ctx.arc(duration, canvas.height/2, radius, 0, 2 * Math.PI, false);
    ctx.closePath();
    ctx.fillStyle = 'black';
    ctx.stroke();
    ctx.fillStyle = 'green';
    ctx.fill();
  }

  container.appendChild(lblMin);
  container.appendChild(canvas);
  container.appendChild(lblMax);
  return container;
}

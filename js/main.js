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
  var canvasData = createCanvas(stats, data, funcName);
  funcContainer.appendChild(canvasData.container);
  for (var profileName in data) {
    var profileDiv = document.createElement("div");
    profileDiv.profileName = profileName;
    profileDiv.data = data[profileName];
    profileDiv.textContent = profileDiv.data.file + " -> " + profileDiv.data.duration + "ms";
    profileDiv.onmouseover = function() {
      updateCanvas(canvasData.canvas, stats, data, funcName, this.profileName);
    }
    profileDiv.onmouseout = function() {
      updateCanvas(canvasData.canvas, stats, data, funcName);
    }
    funcContainer.appendChild(profileDiv);
  }
  container.appendChild(funcContainer);

  return container;
}

function updateCanvas(canvas, stats, data, funcName, selected) {
  canvas.width = 300;
  canvas.height = 30;

  var labelsHeight = 10;
  var ctx = canvas.getContext("2d");
  ctx.lineWidth = 1;
  ctx.strokeStyle = 'black';
  ctx.fillStyle = 'green';
  var radius = 2;
  for (var profileName in data) {
    var duration = data[profileName].duration;
    ctx.beginPath();
    ctx.arc(duration, canvas.height/2 + labelsHeight/2, radius, 0, 2 * Math.PI, false);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();
  }
  ctx.fillStyle = 'blue';
  if (selected != null) {
    var duration = data[selected].duration;
    ctx.beginPath();
    ctx.arc(duration, canvas.height/2 + labelsHeight/2, radius, 0, 2 * Math.PI, false);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();

  }
  ctx.strokeStyle = '#cccccc';
  ctx.fillStyle = 'black';
  for (var i = 0; i < stats.maxTime; i += 25) {
    ctx.fillText(i, i-5, labelsHeight);
    ctx.beginPath();
    ctx.moveTo(i, 10);
    ctx.lineTo(i, canvas.height);
    ctx.stroke();
  }
}

function createCanvas(stats, data, funcName) {
  var container = document.createElement("div");

  var lblMin = document.createTextNode("0 ms");
  var lblMax = document.createTextNode(stats.maxTime + " ms");
  var canvas = document.createElement("canvas");
  updateCanvas(canvas, stats, data, funcName);

  container.appendChild(lblMin);
  container.appendChild(canvas);
  container.appendChild(lblMax);
  return {
    container: container,
    canvas: canvas,
  };
}


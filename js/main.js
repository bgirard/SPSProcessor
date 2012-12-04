var gPreviewIFrame = null;

function enterMainUI() {
  var container = document.createElement("div");
  document.body.appendChild(container);
  container.id = "leftSide";
  container.appendChild(createDataContainer(jsonData));
  var container = document.createElement("div");
  document.body.appendChild(container);
  container.id = "rightSide";
  gPreviewIFrame = document.createElement("iframe");
  gPreviewIFrame.frameBorder = 0;
  gPreviewIFrame.src = "http://people.mozilla.com/~bgirard/cleopatra/"
  container.appendChild(gPreviewIFrame);
}

function createDataContainer(jsonData) {
  var container = document.createElement("div");
  // TODO sort by sequence
  for (var i in jsonData) {
    var data = jsonData[i];
    var stats = computeStats(data.data);
    container.appendChild(createHeader(data.name));
    container.appendChild(displayFunctions(stats, data.data));
  }
  return container;
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
    data[funcName].stats.sort(function(a,b) {
      return b.duration - a.duration;
    });
    for (var profileName in data[funcName].stats) {
      var duration = data[funcName].stats[profileName]["duration"];
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

  var functionOrder = []
  for (var functionName in data) {
    functionOrder[functionOrder.length] = {functionName:functionName, sequence:data[functionName].sequence};
  }
  functionOrder.sort(function(a,b) {
    console.log(a.sequence + " " + b.sequence);
    return a.sequence - b.sequence;
  });
  for (var funcId in functionOrder) {
    var funcName = functionOrder[funcId].functionName;
    var elem = displayFunction(stats, data[funcName].stats, funcName);
    container.appendChild(elem);
  }

  return container;
}

function displayFunction(stats, data, funcName) {
  var container = document.createElement("div");
  
  var title = document.createElement("h2");
  var titleLink = document.createElement("a");
  titleLink.textContent = funcName;
  titleLink.id = funcName
  titleLink.href = "#" + funcName;
  title.appendChild(titleLink);
  container.appendChild(title);

  var funcContainer = document.createElement("div");
  funcContainer.className = "functionDiv";
  var canvasData = createCanvas(stats, data, funcName);
  funcContainer.appendChild(canvasData.container);
  for (var profileName in data) {
    var profileDiv = document.createElement("div");
    profileDiv.data = data[profileName];
    var profileLink = document.createElement("a");
    profileDiv.profileLink = profileLink;
    profileLink.textContent = cleanUpName(profileDiv.data.file) + " -> " + profileDiv.data.duration + "ms";
    profileLink.href = "http://people.mozilla.com/~bgirard/cleopatra/?search=" + profileDiv.data.symbolName + "&customProfile=http://people.mozilla.com/~bgirard/startup_report/" + cleanUpName(profileDiv.data.file);
    profileDiv.appendChild(profileLink);
    profileDiv.profileName = profileName;
    profileDiv.onmouseover = function() {
      updateCanvas(canvasData.canvas, stats, data, funcName, this.profileName);
    }
    profileDiv.onmouseout = function() {
      updateCanvas(canvasData.canvas, stats, data, funcName);
    }
    profileDiv.onclick = function() {
      gPreviewIFrame.src = this.profileLink.href;
      return false;
    }
    funcContainer.appendChild(profileDiv);
  }
  container.appendChild(funcContainer);

  return container;
}

function cleanUpName(name) {
  if (name.indexOf("../") == 0) {
    name = name.substring(3);
  }
    
  return name;
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
  var totalTime = Math.ceil(stats.maxTime / 100) * 100;
  for (var profileName in data) {
    var duration = data[profileName].duration *canvas.width/totalTime;
    ctx.beginPath();
    ctx.arc(duration, canvas.height/2 + labelsHeight/2, radius, 0, 2 * Math.PI, false);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();
  }
  ctx.fillStyle = 'blue';
  if (selected != null) {
    var duration = data[selected].duration *canvas.width/totalTime;
    ctx.beginPath();
    ctx.arc(duration, canvas.height/2 + labelsHeight/2, radius, 0, 2 * Math.PI, false);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();
  }
  ctx.strokeStyle = '#cccccc';
  ctx.fillStyle = 'black';
  for (var i = 0; i < totalTime; i += 100) {
    var x = i*canvas.width/totalTime;
    ctx.fillText(i, x-5, labelsHeight);
    ctx.beginPath();
    ctx.moveTo(x, 10);
    ctx.lineTo(x, canvas.height);
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


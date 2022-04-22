let resp;
let ethrank = [];
let volrank = [];
let gasrank = [];

//make as many rows as we need for incoming data
for(i=0; i<10; i++){
let rowTemplate = "<tr class='block'" + "id=" + (i+1) +  "><td>" +(i+1) + ".</td><td>14543575</td><td>1,531.87 M (12.7 TPS)</td><td>21,828,566 (72.69%, +45%)</td><td><button>View more</button></td></tr>";
document.querySelector("tbody").innerHTML += rowTemplate;
}

fetch('https://backend-xgbqg5tkzq-uw.a.run.app/api/ethelementfiltered?startblock=14623760&endblock=14623960&numresults=10')
.then(response =>{
  return response.json();
}).then(addresses =>{
  console.log(addresses);
  parseData(addresses);
})


document.getElementById("tv").addEventListener("click", function(){sortData(0)});
document.getElementById("ev").addEventListener("click", function(){sortData(1)});
document.getElementById("gas").addEventListener("click", function(){sortData(2)});


document.getElementById("start").addEventListener("focus", focused);
document.getElementById("end").addEventListener("focus", focused);
document.getElementById("start").addEventListener("blur", blurred);
document.getElementById("end").addEventListener("blur", blurred);

document.getElementById("results").addEventListener("click", function(){searchBlock()});

function parseData(resp){
for(i=0; i<resp.Data.length; i++){
  console.log(resp.Data[i].Eth.Rank);
  if(resp.Data[i].Eth.Rank<10){
    ethrank.push([resp.Data[i].address, resp.Data[i].Eth.Rank, resp.Data[i].Eth, resp.Data[i].GasUsed, resp.Data[i].Volume]);
  }
  if(resp.Data[i].Volume.Rank<10){
    volrank.push([resp.Data[i].address, resp.Data[i].Volume.Rank, resp.Data[i].Eth, resp.Data[i].GasUsed, resp.Data[i].Volume]);
  }
  if(resp.Data[i].GasUsed.Rank<10){
    gasrank.push([resp.Data[i].address, resp.Data[i].GasUsed.Rank, resp.Data[i].Eth, resp.Data[i].GasUsed, resp.Data[i].Volume]);
  }
}
console.log(ethrank);
populatePage();
}

function populatePage(){
  ethrank.sort(function(a, b) {
  return a[1] - b[1];
  })
  console.log(ethrank);
  volrank.sort(function(a, b) {
  return a[1] - b[1];
  })
  console.log(volrank);
  gasrank.sort(function(a, b) {
  return a[1] - b[1];
  })
  console.log(gasrank);

  for(i=0; i<10; i++){
    document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + ethrank[i][0] + "</td><td>" + ethrank[i][2].Magnitude + "</td><td>" + ethrank[i][3].Magnitude + "</td><td>" + ethrank[i][4].Magnitude + "</td>"
  }

}

function sortData(t){
  if(t == 0){
    console.log("sort by volume");
    for(i=0; i<10; i++){
      document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + volrank[i][0] + "</td><td>" + volrank[i][2].Magnitude + "</td><td>" + volrank[i][3].Magnitude + "</td><td>" + volrank[i][4].Magnitude + "</td>"
    }
  }else if(t == 1){
    console.log("sort by eth");
    for(i=0; i<10; i++){
      document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + ethrank[i][0] + "</td><td>" + ethrank[i][2].Magnitude + "</td><td>" + ethrank[i][3].Magnitude + "</td><td>" + ethrank[i][4].Magnitude + "</td>"
    }
  }else if(t == 2){
    console.log("sort by gas");
    for(i=0; i<10; i++){
      document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + gasrank[i][0] + "</td><td>" + gasrank[i][2].Magnitude + "</td><td>" + gasrank[i][3].Magnitude + "</td><td>" + gasrank[i][4].Magnitude + "</td>"
    }
  }
}

function searchBlock(){
  if(parseInt(document.getElementById("start").value) >0 && parseInt(document.getElementById("end").value) > 0){

    let startblock = parseInt(document.getElementById("start").value);
    let endblock = parseInt(document.getElementById("end").value);
    fetch('https://backend-xgbqg5tkzq-uw.a.run.app/api/ethelementfiltered?startblock=' + startblock + '&' + 'endblock=' +endblock + '&numresults=10')
    .then(response =>{
      return response.json();
    }).then(addresses =>{
      console.log(addresses);
      parseData(addresses);
    })
    console.log("searching");
  }else{
    console.log("not searching");
  }

}

function focused(event){
  console.log(event.target.value);
  if(event.target.value == "Start Block" || event.target.value == "End Block"){
    event.target.value = "";
  }
  event.target.style.color = "#FFFFFF";
}

function blurred(event){
  console.log(event.target.value);
  if(event.target.value =="" || event.target.value == " "){
    event.target.style.color = "rgba(255,255,255, .4)";
    if(event.target.id == "start"){
      event.target.value = "Start Block";
    }
    if(event.target.id == "end"){
      event.target.value = "End Block";
    }
  }
}

//change the value of these rows in
//accordance with the data sent from our API
// for(i=0; i<document.querySelectorAll(".block td").length; i++){
// document.querySelectorAll(".block td")[i].innerHTML = "blue";
// }

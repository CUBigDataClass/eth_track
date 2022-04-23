let resp;
let ethrank = [];
let volrank = [];
let gasrank = [];

//make as many rows as we need for incoming data
for(i=0; i<10; i++){
let rowTemplate = "<tr class='block'" + "id=" + (i+1) +  "><td>" +(i+1) + ".</td><td></td><td></td><td></td><td></td></tr>";
document.querySelector("tbody").innerHTML += rowTemplate;
}

//add default json data
fetch('data.json')
       .then(function (response) {
           return response.json();
       })
       .then(addresses =>{
         console.log(addresses);
         parseData(addresses);
       })
       .catch(function (err) {
           console.log('error: ' + err);
       });


//add event listeners for sort
document.getElementById("tv").addEventListener("click", function(){sortData(0)});
document.getElementById("ev").addEventListener("click", function(){sortData(1)});
document.getElementById("gas").addEventListener("click", function(){sortData(2)});

//add event listeners for search (this makes it so search remembers what is in the field)
document.getElementById("start").addEventListener("focus", focused);
document.getElementById("end").addEventListener("focus", focused);
document.getElementById("start").addEventListener("blur", blurred);
document.getElementById("end").addEventListener("blur", blurred);

//add event listener for results button (to make api call)
document.getElementById("results").addEventListener("click", function(){searchBlock()});

//parse the response.json file to create three arrays (one for each sort option)
//then, populate the page
function parseData(resp){
  ethrank = [];
  volrank = [];
  gasrank = [];
for(i=0; i<resp.Data.length; i++){
  resp.Data[i].Eth.Magnitude = convertToWords(resp.Data[i].Eth.Magnitude);
  resp.Data[i].GasUsed.Magnitude = resp.Data[i].GasUsed.Magnitude.toLocaleString("en-US");
  resp.Data[i].Volume.Magnitude = resp.Data[i].Volume.Magnitude.toLocaleString("en-US");
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

//sort the arrays and then populate the populate page
//sorts using etherium volume by default
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
    document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + ethrank[i][0] + "</td><td>" + ethrank[i][2].Magnitude + "</td><td>" + ethrank[i][3].Magnitude + "</td><td>" + ethrank[i][4].Magnitude + "<div id='rheight2'></div></td>"
  }

}

//function to change what data is displayed based on sort dropdown
function sortData(t){
  if(t == 0){
    console.log("sort by volume");
    for(i=0; i<10; i++){
      document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + volrank[i][0] + "</td><td>" + volrank[i][2].Magnitude + "</td><td>" + volrank[i][3].Magnitude + "</td><td>" + volrank[i][4].Magnitude + "<div id='rheight2'></div></td>"
    }
  }else if(t == 1){
    console.log("sort by eth");
    for(i=0; i<10; i++){
      document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + ethrank[i][0] + "</td><td>" + ethrank[i][2].Magnitude + "</td><td>" + ethrank[i][3].Magnitude + "</td><td>" + ethrank[i][4].Magnitude + "<div id='rheight2'></div></td>"
    }
  }else if(t == 2){
    console.log("sort by gas");
    for(i=0; i<10; i++){
      document.getElementById(i+1).innerHTML = "<td>" +(i+1) + ".</td><td>" + gasrank[i][0] + "</td><td>" + gasrank[i][2].Magnitude + "</td><td>" + gasrank[i][3].Magnitude + "</td><td>" + gasrank[i][4].Magnitude + "<div id='rheight2'></div></td>"
    }
  }
}


//function that makes api call when "results" is pressed
function searchBlock(){
  if(parseInt(document.getElementById("start").value) >=14623760 && parseInt(document.getElementById("end").value) <= 14623960){
    showloading(true);
    let startblock = parseInt(document.getElementById("start").value);
    let endblock = parseInt(document.getElementById("end").value);
    fetch('https://backend-xgbqg5tkzq-uw.a.run.app/api/ethelementfiltered?startblock=' + startblock + '&' + 'endblock=' +endblock + '&numresults=10')
    .then(response =>{
      return response.json();
    }).then(addresses =>{
      console.log(addresses);
      parseData(addresses);
      showloading(false);
    })
    console.log("searching");
  }else if(document.getElementById("start").value > parseInt(document.getElementById("end").value)){
    alert("please make sure your end value is greater than your start value");
  }    else{
    alert("please input a block range between 14623760 and 14623960");
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

function showloading(test){
  if(test){
    console.log("loading");
    document.getElementById("loading").style.display = "block";
  }else{
    console.log("not loading");
    document.getElementById("loading").style.display = "none";
  }
}

function convertToWords(num){
  num = num.toString();
  if(num.indexOf('e') != -1){
    let pos_e = num.indexOf('e');
    let exp = parseInt(num.substring(pos_e+2, num.length));

    // if(exp<=15){
      if(exp>=12){
        let multip = exp-12;
        num = num.slice(0,[pos_e]);
        num = Math.round(parseFloat(num)*(10**multip)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Trillion"
      }else if(exp>=9){
        let multip = exp-9;
        num = num.slice(0,[pos_e]);
        num = Math.round(parseFloat(num)*(10**multip)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Billion"
      }else if(exp>=6){
        let multip = exp-6;
        num = num.slice(0,[pos_e]);
        num = Math.round(parseFloat(num)*(10**multip)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Million"
      }else{
        let multip = exp-15;
        num = num.slice(0,[pos_e]);
        num = Math.round(parseFloat(num)*(10**multip)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Quadrillion"
      }
    // }else{
    //   if(exp<=18){
    //     let multip = exp-18;
    //     num = num.slice(0,[pos_e]);
    //     num = Math.round(parseFloat(num)*(10**multip)*100)/100;
    //     num = num.toLocaleString("en-US");
    //     num += " Quintillion"
    //   }else if(exp>18 && exp<=23){
    //     let multip = exp-21;
    //     num = num.slice(0,[pos_e]);
    //     num = Math.round(parseFloat(num)*(10**multip)*100)/100;
    //     num = num.toLocaleString("en-US");
    //     num += " Sextillion"
    //   }else if(exp>23 && exp<=24){
    //     let multip = exp-24;
    //     num = num.slice(0,[pos_e]);
    //     num = Math.round(parseFloat(num)*(10**multip)*100)/100;
    //     num = num.toLocaleString("en-US");
    //     num += " Septillion"
    //   }else{
    //     let multip = exp-27;
    //     num = num.slice(0,[pos_e]);
    //     num = Math.round(parseFloat(num)*(10**multip)*100)/100;
    //     num = num.toLocaleString("en-US");
    //     num += " Octillion"
    //   }
    // }
  }else{
    num = parseInt(num);
    let numlen = toString(num).length;
    if(numlen <2 || num == 0){
      num = num;
    }else if(numlen>3){
      // if(numlen>=18){
      //   num = Math.round(num*(10**-15)*100)/100;
      //   num = num.toLocaleString("en-US");
      //   num += " Quintillion"
      // }
      // else if(numlen>=15){
      //   num = Math.round(num*(10**-15)*100)/100;
      //   num = num.toLocaleString("en-US");
      //   num += " Quadrillion"
      // }
      if(numlen>=12){
        num = Math.round(num*(10**-12)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Trillion"
      }else if(numlen>=9){
        num = Math.round(num*(10**-9)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Billion"
      }else if(numlen>=6){
        num = Math.round(num*(10**-6)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Million"
      }else{
        num = Math.round(num*(10**-3)*100)/100;
        num = num.toLocaleString("en-US");
        num += " Thousand"
      }

    }
    num = num.toLocaleString("en-US");
  }
  return num;
}

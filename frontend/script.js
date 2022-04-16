//make as many rows as we need for incoming data
for(i=0; i<10; i++){
let rowTemplate = "<tr class='block'><td>" +(i+1) + ".</td><td>14543575</td><td>1,531.87 M (12.7 TPS)</td><td>21,828,566 (72.69%, +45%)</td><td><button>View more</button></td></tr>";
document.querySelector("tbody").innerHTML += rowTemplate;
}

//change the value of these rows in
//accordance with the data sent from our API
// for(i=0; i<document.querySelectorAll(".block td").length; i++){
// document.querySelectorAll(".block td")[i].innerHTML = "blue";
// }

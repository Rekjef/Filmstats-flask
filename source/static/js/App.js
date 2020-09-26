import React from 'react';

var apiKey = 'f3b1d27d';
var movieTitle = "Dom z papieru";

function drawCard() {
  var data = getData()
}

function getData(){
  var link = "http://www.omdbapi.com/?apikey=" + apiKey +"&" + movieTitle;
  console.log(link)
  fetch("http://www.omdbapi.com/?apikey=" + apiKey +"&t" + movieTitle)
  .then(response => response.json)
  .then(data => console.log(data));
}

function calc(){
  return 222222;
}

export default drawCard;

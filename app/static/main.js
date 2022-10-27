'use strict'
$(document).ready(function() {
    const queryDetails = document.getElementById("query-details")
    queryDetails.addEventListener("submit", function () {
    let userName = document.forms["queryDetails"]["username"].value;
    let password = document.forms["queryDetails"]["password"].value;
    var missingInfo = [];
    if (userName == "") {
      missingInfo.push("username");
      $("#user-name").addClass("error");
    }
    else {
      $("#user-name").removeClass("error");
    }

    if (password == "") {
      missingInfo.push("password");
      $("#password").addClass("error");
    }
    else {
      $("#password").removeClass("error");
    }
    console.log(missingInfo);

    if (missingInfo.length != 0) {
      let errorString = "Missing required fields. Please enter your ";
      for (let idx = 0; idx < missingInfo.length; idx++) {
        errorString += missingInfo[idx];
        if (idx != missingInfo.length - 1) {
          errorString += ", ";
        }
      }
      alert(errorString);
      return false;
    }
    else {
      alert("Querying now");
    }
  });
});
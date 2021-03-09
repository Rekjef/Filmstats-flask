function buttonClick(){
    var url = document.getElementById("searchValue").value;
    alert("/search/" + url);
    window.location.replace("/search/" + url);
}
var form = document.getElementById("search-bar");

form.addEventListener("submit", function (e) {
  e.preventDefault();
  var search = form.querySelector("input[type=search]");
  search.value = "site:css-tricks.com " + search.value;
  form.submit();
});
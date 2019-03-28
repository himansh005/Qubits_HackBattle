$(document).ready(function(){
  console.log("mad");
$("#submit").click(function(){
  var a = $("#fname").text;
  console.log(a);

  if(a == '1'){
    console.log("asdasadsdasd");
    $("#root").append("<img src='{{url_for('static',filename='images/a.png')}}' style='height:400px;width:400px;'>");
  }
  else if(a=='2')
  {
    $("#root").append("<img src='{{url_for('static',filename='images/b.png')}}' style='height:400px;width:400px;'>");

  }
});});

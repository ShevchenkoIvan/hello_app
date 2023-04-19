$(document).ready(function () {
let clicks = 0;

$('#ClickButton').on('click', function () {
        clicks += 1;
        document.getElementById("ClickView").innerHTML = clicks;
});

});

var recepie_content = []; //javascript won't let me allocate memory for it for some reason
var max_recepie = 50;

function img_preview(event) {
    var input = event.target;
    var preview = document.getElementById("preview_img");

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(event) {
            preview.innerHTML = '<img src="' + event.target.result + '" width="300" width="300">'
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function add_list() {
    var list = document.getElementById("ingrediants_list");
    var list_input = document.getElementById("list_input");

    let buffer = document.createElement("li");
    buffer.textContent = list_input.value;
    list.appendChild(buffer);    
    recepie_content.push(list_input.value);
    console.log(recepie_content);
}

document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("content_form");
    var result = document.getElementById("result");

    const success = "Packet succesfully sent\n";
    const failure = "Unable to send packet\n";

    function upload(event) {
    event.preventDefault();

    let content_buffer = new FormData(form);
    if (recepie_content.length > max_recepie) {
        result.innerHTML = failure;
        return ;
    }
    content_buffer.append("ingrediants_list", JSON.stringify(recepie_content));

    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/post", true);

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status == 200) {
            result.innerHTML = success;
        } else {
            result.innerHTML = failure;
        }
    }

    console.log("sent");
    xhr.send(content_buffer);
    }

    form.addEventListener("submit", upload);
});
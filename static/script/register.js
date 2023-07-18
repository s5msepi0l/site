document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("client_register");
  const client_res = document.getElementById("result");

  const success = "Wassaaaa";
  const failure = "Fogedaaabout it\n";

  form.addEventListener("submit", function(event) {
    event.preventDefault();

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/register", true);

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const response = xhr.responseText;

        if (response.localeCompare(success) == 0) {
          client_res.innerHTML = success;
        } else {
          client_res.innerHTML = failure;
        }
        console.log(response);
      }
    };

    xhr.send(new FormData(form)); //email does fucking nothing hahahahahahha
  });
});

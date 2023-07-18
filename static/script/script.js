var logout_btn = document.getElementById("logout_btn");
var login_btn = document.getElementById("Login_button");

document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('client_register');
  const login_result = document.getElementById('result');

  function login(event) {
    event.preventDefault();
    console.log('login');

    const success = 'Wassaaaa';
    const failure = 'Fogedaaabout it';

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/login', true);

    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        const response = xhr.responseText;

        if (response.localeCompare(success) === 0) {
          login_result.innerHTML = success;
          
          logout_btn.style.color = "black";
          logout_btn.style.border = "solid black"; 


          login_btn.style.color = "green";
          login_btn.style.border = "solid green";

        } else {
          login_result.innerHTML = failure;
        }
        console.log(response);
      }
    };

    xhr.send(new FormData(loginForm));
  }

  loginForm.addEventListener('submit', login);
});

function logout() {
  console.log("fuck2");
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/api/logout", true);
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {       
      logout_btn.style.color = "red";
      logout_btn.style.border = "solid red"; 

      console.log("test");
      login_btn.style.color = "black";
      login_btn.style.border = "solid black";
      return ;
    }
  }
  xhr.send("fuck");
}

const content_col = 12;
const img_x = 300;
const img_y = 300;

function append_img(imageURL) {
  const ul = document.getElementById('image_buffer');
  const li = document.createElement('li');
  li.innerHTML = `
    <div>
      <a>
        <img src="${imageURL}" width="${img_x}" height="${img_y}">
      </a>
    </div>
  `;
  ul.appendChild(li);
}

for (let i = 0; i < content_col; i++) {
  const p_route = "/api/content_preview";

  const xhr = new XMLHttpRequest();

  xhr.open("GET", "/api/content_preview?offset=0", true);
  xhr.onload = function() {
    const response = JSON.parse(xhr.responseText);

    const content_img = URL.createObjectURL(response.thumbnail);
    const content_name = response.name;
    const content_id = response.id;

  };
  xhr.send();
}
const password = document.getElementById("password");
const confirm = document.getElementById("confirmpassword");
const submit = document.getElementById("submit");

function checkPassword() {
    if (confirm.value === password.value) {
        password.classList.remove("border-red-400");
        confirm.classList.remove("border-red-400");
        password.classList.add("border-green-400");
        confirm.classList.add("border-green-400");
        submit.disabled = false;
    } else {
        password.classList.remove("border-green-400");
        confirm.classList.remove("border-green-400");
        password.classList.add("border-red-400");
        confirm.classList.add("border-red-400");
        submit.disabled = true;
    }
}
password.addEventListener("keyup", checkPassword);
confirm.addEventListener("keyup", checkPassword);
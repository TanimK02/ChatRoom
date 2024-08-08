const accNameInput = document.getElementById("new-acc-name");
const accNameBtn = document.getElementById("acc-name-btn");
const accDelBtn = document.getElementById("acc-delete-btn");
const alerts = document.getElementById("alerts");
const currentName = document.getElementById("username");
const delDiv = document.getElementById("del-div");
const delX = document.getElementById("del-x");
const password = document.getElementById("password");
const delConfirm = document.getElementById("delete-confirm");

const getCSRFToken = () => {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
};

const editAccName = async() => {
    const csrfToken = getCSRFToken();
    const new_name = accNameInput.value;
    const response = await fetch('/edit_account', {
        method: "PUT",
        headers: {
            "Content-Type": "application/json", 
            "X-CSRFTOKEN": csrfToken,
        },
        body: JSON.stringify({"new_name": new_name})
    });
    const result = await response.json();
    if (response.status == 200) {
        alerts.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Name change successful.";
        alerts.appendChild(el);
        if (currentName){
            currentName.textContent = "Username: " + result.new_name};
    } else {
        alerts.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Name change failed.";
        console.log(response.message)
        alerts.appendChild(el);
    };
};

const deleteAccount = async () => {
    const csrfToken = getCSRFToken();
    const response = await fetch('/edit_account', {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({"old_pass": password.value})
    
    });
    console.log(response)
    if (response.ok) {
        window.location.href = "/login";
    } else {
        alerts.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Failed to delete account.";
        alerts.appendChild(el);
        delDiv.style.display = "none";
    }
};

accNameBtn.addEventListener("click", editAccName);
accDelBtn.addEventListener("click", () => {
    delDiv.style.display = "flex";
});
delX.addEventListener("click", () => {
    delDiv.style.display = "none";
});
delConfirm.addEventListener("click", deleteAccount)
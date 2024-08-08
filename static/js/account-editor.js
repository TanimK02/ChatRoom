const accNameInput = document.getElementById("new-acc-name");
const accNameBtn = document.getElementById("acc-name-btn");
const accDelBtn = document.getElementById("acc-delete-btn");
const currentName = document.getElementById("username");
const delDiv = document.getElementById("del-div");
const delX = document.getElementById("del-x");
const password = document.getElementById("password");
const delConfirm = document.getElementById("delete-confirm");
const changePassBtn = document.getElementById("change-password-btn");
const passDiv = document.getElementById("change-pass");
const passX = document.getElementById("pass-x");
const alerts1 = document.querySelector(".alerts1");
const alerts2 = document.querySelector(".alerts2");
const alerts3 = document.querySelector(".alerts3");
const passConf = document.getElementById("password-confirm");
const getCSRFToken = () => {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
};

const editAccName = async() => {
    const csrfToken = getCSRFToken();
    const new_name = accNameInput.value;
    if (new_name.length < 6 || new_name.length > 20) {
        alerts1.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Username must be 6-20 chars long.";
        alerts1.appendChild(el);
        return
    };
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
        alerts1.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Name change successful.";
        alerts1.appendChild(el);
        if (currentName){
            currentName.textContent = "Username: " + result.new_name};
    } else {
        alerts1.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Name change failed.";
        console.log(response.message)
        alerts1.appendChild(el);
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
        alerts2.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Failed to delete account.";
        alerts2.appendChild(el);
    }
};

const changePass = async () => {
    const csrfToken = getCSRFToken();
    const old_pass = document.getElementById("old_password");
    const new_pass = document.getElementById("new_password");
    if (new_pass.value.length < 8 || new_pass.value.length > 60) {
        alerts3.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Password must be 8-60 chars long.";
        alerts3.appendChild(el);
        return
    };
    const response = await fetch('/edit_account', {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({"old_pass": old_pass.value,
            "new_pass": new_pass.value
        })
    
    });
    console.log(response)
    if (response.ok) {
        alerts3.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Password change success.";
        alerts3.appendChild(el);
    } else {
        alerts3.innerHTML = "";
        const el = document.createElement("li");
        el.textContent = "Failed to change password.";
        alerts3.appendChild(el);
    }
};

accNameBtn.addEventListener("click", editAccName);
accDelBtn.addEventListener("click", () => {
    delDiv.style.display = delDiv.style.display == "flex" ? "none" : "flex";
});
delX.addEventListener("click", () => {
    delDiv.style.display = "none";
});
delConfirm.addEventListener("click", deleteAccount);
changePassBtn.addEventListener("click", () => {
    passDiv.style.display = passDiv.style.display == "flex" ? "none" : "flex";
})
passX.addEventListener("click", () => {
    passDiv.style.display = "none";
})
passConf.addEventListener("click", changePass)
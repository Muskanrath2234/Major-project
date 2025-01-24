// // Initial References
let totalAmount = document.getElementById("total-amount");
let userAmount = document.getElementById("user-amount");

const checkAmountButton = document.getElementById("check-amount");
const totalAmountButton = document.getElementById("total-button");

const productTitle = document.getElementById("product-title");

const errorMessage = document.getElementById("budget-error");
const productTitleError = document.getElementById("product-title-error");
const productCostError = document.getElementById("product-cost-error"); 

const amount = document.getElementById("amount");
const expenditureValue = document.getElementById("expenditure-value");
const balanceValue = document.getElementById("balance-amount");

const list = document.getElementById("list");

let tempAmount = 0;

// Step 1: Add references to the popup and buttons
const budgetPopup = document.getElementById("budget-popup");
const acceptChangeButton = document.getElementById("accept-change");
const cancelChangeButton = document.getElementById("cancel-change");
// Flag to check if the budget is already set
let isBudgetSet = false;
// Step 2: Modify the budget set function
totalAmountButton.addEventListener('click', () => {
    const newTempAmount = Number(totalAmount.value);

    // Check for empty or negative input
    if (isNaN(newTempAmount) || newTempAmount <= 0) {
        errorMessage.classList.remove("hide");
    } else {
        errorMessage.classList.add("hide");

        // Check if the budget is already set and prompt for confirmation
        if (isBudgetSet) {
            budgetPopup.classList.remove("hide");

            // Accept button logic
            acceptChangeButton.onclick = () => {
                resetBudget(newTempAmount);
                budgetPopup.classList.add("hide");
            };

            // Cancel button logic
            cancelChangeButton.onclick = () => {
                budgetPopup.classList.add("hide");
                totalAmount.value = ""; // Clear the input
            };
        } else {
            resetBudget(newTempAmount);
        }
    }
});




// Step 3: Function to reset the budget
function resetBudget(newAmount) {
    amount.innerText = newAmount;
    balanceValue.innerText = newAmount;
    expenditureValue.innerText = 0;
    list.innerHTML = ""; // Clear the expenses list
    tempAmount = newAmount;
    isBudgetSet = true;
    totalAmount.value = ""; // Clear the input
}

// Disable 'Edit' & 'Delete' Button
const disableButtons = (bool) => {
    let editButtons = document.getElementsByClassName("edit");
    Array.from(editButtons).forEach(element => {
        element.disabled = bool;
    });
};

// Modify List Elements
const modifyElement = (element, edit = false) => {
    let parentDiv = element.parentElement;
    let currentBalance = balanceValue.innerText;
    let currentExpense = expenditureValue.innerText;
    let parentAmount = parentDiv.querySelector(".amount").innerText;
    if (edit) {
        let parentText = parentDiv.querySelector(".product").innerText;
        productTitle.value = parentText;
        userAmount.value = parentAmount;
        disableButtons(true);
    }
    balanceValue.innerText = parseInt(currentBalance) + parseInt(parentAmount);
    expenditureValue.innerText = parseInt(currentExpense) - parseInt(parentAmount);
    parentDiv.remove();
};

// Create Expense List
const listCreator = (expenseName, expenseValue) => {
    let sublistContent = document.createElement("div");
    sublistContent.classList.add("sublist-content", "flex-space");
    list.appendChild(sublistContent);
    sublistContent.innerHTML = `<p class="product">${expenseName}</p><p class="amount">${expenseValue}</p>`;
    let editButton = document.createElement("button");
    editButton.classList.add("fa-solid", "fa-pen-to-square", "edit");
    editButton.style.fontSize = "26px";
    editButton.addEventListener("click", () => {
        modifyElement(editButton, true);
    });
    let deleteButton = document.createElement("button");
    deleteButton.classList.add("fa-solid", "fa-trash-can", "delete");
    deleteButton.style.fontSize = "26px";
    deleteButton.addEventListener("click", () => {
        modifyElement(deleteButton);
    });
    sublistContent.appendChild(editButton);
    sublistContent.appendChild(deleteButton);
    document.getElementById("list").appendChild(sublistContent);
};

// Function to Add Expenses
checkAmountButton.addEventListener("click", () => {
    if (!userAmount.value || !productTitle.value) {
        productTitleError.classList.remove("hide");
        return false;
    }

    // Negative Value Check
    if (parseInt(userAmount.value) <= 0) {
        productTitleError.innerText = "Expense value cannot be zero or negative";
        productTitleError.classList.remove("hide");
        return false;
    } else {
        productTitleError.classList.add("hide");
    }

    // Enable buttons
    disableButtons(false);

    // Expense
    let expenditure = parseInt(userAmount.value);

    // Total expense (existing + new)
    let sum = parseInt(expenditureValue.innerText) + expenditure;
    expenditureValue.innerText = sum;

    // Total balance (budget - total expense)
    const totalBalance = tempAmount - sum;
    balanceValue.innerText = totalBalance;

    // Create list
    listCreator(productTitle.value, userAmount.value);

    // Empty inputs
    productTitle.value = "";
    userAmount.value = "";
});



document.addEventListener("DOMContentLoaded", loadTransactions);

document.getElementById("transactionForm").addEventListener("submit", function(e) {
    e.preventDefault();
    let type = document.getElementById("type").value;
    let amount = parseFloat(document.getElementById("amount").value);
    let description = document.getElementById("description").value;

    fetch("/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type, amount, description })
    }).then(res => res.json())
      .then(data => {
          loadTransactions();
          document.getElementById("transactionForm").reset();
      });
});

function loadTransactions() {
    fetch("/transactions")
        .then(res => res.json())
        .then(data => {
            document.getElementById("balance").textContent = data.balance.toFixed(2);
            document.getElementById("income").textContent = data.total_income.toFixed(2);
            document.getElementById("expense").textContent = data.total_expense.toFixed(2);

            let list = document.getElementById("transactionList");
            list.innerHTML = "";
            data.transactions.forEach(tx => {
                let li = document.createElement("li");
                li.textContent = `${tx.type.toUpperCase()} ₹${tx.amount} - ${tx.description} (${tx.date})`;
                list.appendChild(li);
            });
        });
}

function bookNowForm(pricingPlan, pricingSum) {
    const checkboxes = document.querySelector("#checkbox-id");
    if (checkboxes) {
        checkboxes.style.display = "none";
    }
    const oldPricing = document.querySelector(".current-plan");
    if (oldPricing) {
        oldPricing.remove();
    }

    let pricing = document.createElement("div");
    pricing.className = "input-group current-plan";
    pricing.innerHTML = `
        <label for="name">Your current plan:</label>
        <input id="name" type="text" value="${pricingPlan} - ${pricingSum}" readonly/>
    `;

    const formContainer = document.querySelector("#appointment-form form");
    if (formContainer) {
        formContainer.insertBefore(pricing, formContainer.firstChild);
    }
}

function bookAppointmentForm() {
    const checkboxes = document.querySelector("#checkbox-id");
    checkboxes.style.display = "flex";
}

function clearForm() {
    event.preventDefault();
    document.querySelectorAll(".current-plan").forEach(el => el.remove());
    const checkboxes = document.querySelector("#checkbox-id");
    checkboxes.style.display = "flex";
}

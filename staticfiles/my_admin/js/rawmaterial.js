document.addEventListener("DOMContentLoaded", function () {
    const commodityField = document.getElementById("id_commodity");
    const inputUnitField = document.getElementById("id_input_unit");
    const outputUnitField = document.getElementById("id_output_unit");
    const amountField = document.getElementById("id_amount");
    const outputAmountField = document.getElementById("id_output_amount");

    const ternalSelect = document.getElementById("id_ternal");
    const categorySelect = document.getElementById("id_filter_category");
    const commoditySelect = document.getElementById("id_commodity");

    function updateCommodities() {
        const ternal = ternalSelect ? ternalSelect.value : "";
        const categoryId = categorySelect ? categorySelect.value : "";

        if (!ternal && !categoryId) {
            commoditySelect.innerHTML = '<option value="">---------</option>';
            return;
        }

        const params = new URLSearchParams();
        if (ternal) params.append("ternal", ternal);
        if (categoryId) params.append("category_id", categoryId);

        fetch(`/get-filtered-commodities/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                commoditySelect.innerHTML = '<option value="">---------</option>';
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = item.name;
                    commoditySelect.appendChild(option);
                });
            });
    }

    if (ternalSelect) ternalSelect.addEventListener("change", updateCommodities);
    if (categorySelect) categorySelect.addEventListener("change", updateCommodities);

    const units = {
        'کیلو': 1000,
        'سانتی': 0.01,
        'میلی': 0.001,
    };

    if (commodityField) {
        commodityField.addEventListener("change", function () {
            const commodityId = this.value;
            if (!commodityId) return;

            fetch(`/get-commodity-unit/${commodityId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.unit_id) {
                        inputUnitField.value = data.unit_id;
                        checkUnits();
                    }
                });
        });
    }

    function checkUnits() {
        if (inputUnitField.value && outputUnitField.value) {
            amountField.readOnly = false;
        } else {
            amountField.readOnly = true;
            amountField.value = "";
            outputAmountField.value = "";
        }
    }

    inputUnitField.addEventListener("change", checkUnits);
    outputUnitField.addEventListener("change", checkUnits);

    amountField.addEventListener("input", function () {
        const amount = parseFloat(this.value);        

        if (!amount || !inputUnitField.value || !outputUnitField.value) {
            outputAmountField.value = "";
            return;
        }

        const inputText = inputUnitField.selectedOptions[0].innerText;
        const outputText = outputUnitField.selectedOptions[0].innerText;

        let inputPower = 1;
        let outputPower = 1;

        for (const key in units) {
            if (inputText.includes(key)) inputPower = units[key];
            if (outputText.includes(key)) outputPower = units[key];
        }

        const converted = (amount * inputPower) / outputPower;
        outputAmountField.value = converted;
    });

    checkUnits();
});

function getSuggestions() {
    console.log("Button clicked");

    const electricity = document.getElementById("electricity").value;
    const water = document.getElementById("water").value;
    const transport = document.getElementById("transport").value;

    if (!electricity || !water) {
        document.getElementById("result").innerText =
            "Please enter all values before analyzing.";
        return;
    }

    fetch("http://127.0.0.1:5000/ai-test", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            electricity: electricity,
            water: water,
            transport: transport
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.suggestion;
    })
    .catch(err => {
        console.error(err);
        document.getElementById("result").innerText =
            "Error connecting to AI backend";
    });
}

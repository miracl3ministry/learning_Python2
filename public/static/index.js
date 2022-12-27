"use strict";

// (人 •ᴗ•) □✧~

document.addEventListener("DOMContentLoaded", () => {
    console.log("Hello world");
    document.getElementById("btn-check-spam").addEventListener("click", () => {
        fetchData("./checkforspam", { command: "check for spam" }, (err, data) => {
            console.log(err, data);
            if (err) {
                console.error(err);
                document.getElementById("info").innerText = "";
                document.getElementById("info").innerText = err?.toString();
            } else {
                if (data?.status === "OK") {
                    // window.location.reload();
                } else {
                    document.getElementById("info").innerText = "";
                    document.getElementById("info").innerText = data?.message?.toString();
                }
            }
        });
    });
});

function fetchData(path, data, callback) {
    fetch(path, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        cache: "no-cache",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        body: JSON.stringify(data),
    })
        .catch((err) => callback(err))
        .then(async (resolve) => {
            try {
                if (resolve.status === 200) {
                    let ans = await resolve.json();
                    callback(null, ans);
                } else {
                    throw new Error("Ответ сети был не ok.");
                }
            } catch (error) {
                console.error("Ошибка HTTP: ", resolve.status, error.message);
                console.log(error.message);
                callback(error);
            }
        });
}
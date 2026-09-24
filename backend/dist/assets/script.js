url_form = document.getElementById("shortening-url-form");


url_form.addEventListener('submit', async (e) => {
    e.preventDefault();
    original_url = url_form.querySelector("#url").value;
    short_alias = url_form.querySelector("#short-alias").value;
    response = await fetch("/api/link", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"original_url": original_url, "short_alias": short_alias})
    })
    res = await response.json()
    
    if (res.status_code != 201) {
        alert("URL isn't correct!")
        return;
    } else alert("URL успешно сокращен!")
    window.location.reload()
})

document.addEventListener("DOMContentLoaded", async () => {
    res = await fetch("/api/link");
    data = await res.json();
    if (data != "") {
        links_table = document.getElementById("redirecting-links-table");
        links_table.innerHTML += `
            <tr>
                <th>ID</th>
                <th>Original URL</th>
                <th>Short alias</th>
                <th>Shortened URL</th>
                <th>Clicks</th>
            </tr>
        `
        data.forEach(l => {
            links_table.innerHTML += `
                <tr>
                    <td>${l.id}</td>
                    <td>${l.original_url}</td>
                    <td>${l.short_alias}</td>
                    <td><a href="/r/${l.short_alias}">http://localhost:8000/r/${l.short_alias}</a></td>
                    <td>${l.clicks}</td>
                    <td class="link-del-td" data-id="${l.id}" onclick="del_l(this)"><button class="link-del-btn">Удалить</button></td>
                </tr>
            `
        })
    } else {
        document.getElementById("redirecting-container").innerHTML = "<p style='display: flex; justify-content: center; width: 100%'>В данный момент нет никаких ссылок</p>"
    } 
})

async function del_l(btn) {
    l_id = btn.getAttribute("data-id");
    await fetch(`/api/link/${l_id}`, {method: "DELETE"});
    window.location.reload();
}
function sendPOST() {
    let formData = { location: $("#location").val() };

    $.post("/MIX", formData)
    .done(function (data) {
      $("#content").html(`<hr><h3>Result</h3><pre>${JSON.stringify(data, null, 2)}</pre>`);
    })
    .fail(function (data) {
      $("#content").html(`<hr><h3>Error - ${data.status}</h3><pre>${JSON.stringify(data, null, 2)}</pre>`);
    })
}
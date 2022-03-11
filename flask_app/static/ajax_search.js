search_events_form.onsubmit = function (e) {
  e.preventDefault();
  console.log("made it here");
  let form = new FormData(search_events_form);

  fetch("http://127.0.0.1:5000/search_results", { method: "POST", body: form })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      console.log(typeof data);
      console.log(data.length);
      results = document.getElementById("results");
      results.innerHTML = "";
      for (i = 0; i < data.length; i++) {
        results.innerHTML += `<tr>
          <td><a href= "/event_details/${data[i].id}">${data[i].event_name}</a></td>
          <td>${data[i].date}</td>
          <td>${data[i].location}, ${data[i].city}, ${data[i].state}</td>
        </tr>`;
      }
    });
};
// <td>${data.event[i].date}  ${events[i].start_time} to ${events[i].end_time}</td>
// <td>${events[i].location}, ${events[i].city}, ${events[i].state}</td>
// <td>${events[i].host.first_name} ${events[i].host.last_name} </td>

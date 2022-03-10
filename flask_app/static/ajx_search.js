search_events_form.onsubmit = function (e) {
  e.preventDefault();
  console.log("made it here");
  let form = new FormData(new_book_form);

  fetch("http://127.0.0.1:5000/search_results", { method: "POST", body: form })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      for (i = 0; i < events.length; i++) {
        results.innerHTML += results.innerHTML = `<tr>
        <td>${events[i].event_name}</td>
        <td>${events[i].date}  ${events[i].start_time} to ${events[i].end_time}</td>
        <td>${events[i].location}, ${events[i].city}, ${events[i].state}</td>
        <td>${events[i].host.first_name} ${events[i].host.last_name} </td>
      </tr>`;
        //   a tag with route to profile/<int:user_id>
      }
    });
};

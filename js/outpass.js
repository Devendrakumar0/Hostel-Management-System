function validateDate() {
  var currentDate = new Date();
  var selectedDate = new Date(document.getElementById("myDateInput").value);
  // Set currentDate to the start of the day (midnight)
  currentDate.setHours(0, 0, 0, 0);
  // Set selectedDate to the start of the day (midnight)
  selectedDate.setHours(0, 0, 0, 0);
  if (selectedDate < currentDate) {
    alert("Please select a future date.");
    document.getElementById("myDateInput").value = ""; // Clear the input field
  } else {
    var tomorrow = new Date(currentDate);
    tomorrow.setDate(currentDate.getDate() + 1);
    tomorrow.setHours(0, 0, 0, 0); // Set to the start of the day (midnight)
    if (selectedDate > tomorrow) {
      alert("Please select only today or tomorrow's date.");
      document.getElementById("myDateInput").value = "";
    }
  }
}

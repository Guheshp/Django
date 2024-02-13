var message_timeout = document.getElementById("message-timer")

setTimeout(function()

{
    message_timeout.style.display="none";

}, 5000);


document.addEventListener('DOMContentLoaded', function() {
  const dropdownIcon = document.getElementById('dropdownIcon');
  dropdownIcon.addEventListener('click', function() {
      const dropdownContent = document.querySelector('.dropdowncontent');
      dropdownContent.classList.toggle('show');
  });
});
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

// slide functionality

const slides = document.querySelectorAll(".slide")
let counter = 0;
const totalSlides = slides.length;

console.log(slides)

slides.forEach(
  (slides,index) => {
    slides.style.left = `${index * 100}%`
  }
)
// goback 
const goPrev = () => {
  if (counter > 0) {
    counter--;
    slideImage();
  }
}
// goforward 
const goNext = () => {
  if (counter < totalSlides - 1) {
    counter++;
    slideImage();
  }
}

const slideImage = () => {
  slides.forEach(
    (slide) => {
      slide.style.transform = `translateX(-${counter * 100}%)`
    }
  )
}

// about content 

document.addEventListener('DOMContentLoaded', function() {
  var truncatedContent = document.getElementById('truncated-content');
  var fullContent = document.getElementById('full-content');
  var toggleButton = document.getElementById('toggle-button');
  var toggleButtonLess = document.getElementById('toggle-button-less');

  toggleButton.addEventListener('click', function(event) {
      event.preventDefault();
      if (truncatedContent.style.display === 'none') {
          truncatedContent.style.display = 'block';
          fullContent.style.display = 'none';
          toggleButton.innerText = 'read more';
          toggleButtonLess.style.display = 'none';
      } else {
          truncatedContent.style.display = 'none';
          fullContent.style.display = 'block';
          toggleButton.style.display = 'none';  // Hide "read more"
          toggleButtonLess.style.display = 'inline';
      }
  });

  toggleButtonLess.addEventListener('click', function(event) {
      event.preventDefault();
      truncatedContent.style.display = 'block';
      fullContent.style.display = 'none';
      toggleButton.style.display = 'inline';  // Show "read more"
      toggleButtonLess.style.display = 'none';
  });
});

// side navbar active link ---------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function() {
  var currentUrl = window.location.pathname;
  var navbarLinks = document.querySelectorAll('.sidenav-links a');

  navbarLinks.forEach(function(link) {
    var href = link.getAttribute('href');
    if (currentUrl === href) {
      link.classList.add('active');
    }
  });
});


// search functionality ---------------------------------------------------------------------
document.getElementById('search_form').addEventListener('submit', function(event) {
  var searchInput = document.getElementById('search_input').value.trim();
  if (searchInput === '') {
      document.getElementById('search_error').innerText = 'Please enter a Location.';
      setTimeout(function() {
        document.getElementById('search_error').innerText = '';
      }, 3000);
      event.preventDefault(); // Prevent form submission
  }
});


document.addEventListener('DOMContentLoaded', function() {
  const bookBtn = document.querySelector('.book-btn');
  const bookingForm = document.getElementById('bookingForm');
  
  bookBtn.addEventListener('click', function(event) {
      event.preventDefault();
      bookingForm.style.display = 'block';
  });

  const bookSubmitBtn = document.getElementById('bookSubmitBtn');
  bookSubmitBtn.addEventListener('click', function(event) {
      // Optionally, you can add validation logic here before submitting the form
      // If validation fails, prevent the default behavior of form submission using event.preventDefault()
  });
});




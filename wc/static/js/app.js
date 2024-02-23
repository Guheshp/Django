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
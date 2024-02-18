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
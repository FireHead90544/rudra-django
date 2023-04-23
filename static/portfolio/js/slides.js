let slides = document.getElementsByClassName("slide");
let prevSlide = document.getElementById("prevSlide");
let nextSlide = document.getElementById("nextSlide");

let slide = 0;
document.getElementsByClassName("slide")[slide].classList.toggle("hidden"); // Show the first slide

function changeSlide(n) {
    slide += n;
    if (slide < 0) {
        slides[slide + 1].classList.toggle("hidden");
        slide = slides.length - 1;
        slides[slide].classList.toggle("hidden");
    } else if (slide > slides.length - 1) {
        slides[slide - 1].classList.toggle("hidden");
        slide = 0;
        slides[slide].classList.toggle("hidden");
    } else {
        slides[slide - n].classList.toggle("hidden");
        slides[slide].classList.toggle("hidden");
    }
}

prevSlide.addEventListener("click", function() {
    changeSlide(-1);
});

nextSlide.addEventListener("click", function() {
    changeSlide(1);
});
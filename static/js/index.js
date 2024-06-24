import * as THREE from 'three';
import { OBJLoader } from 'OBJLoader';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const video = document.querySelector("video");

let tl = gsap.timeline({
  scrollTrigger: {
    trigger: "video",
    start: "top top",
    end: "bottom+=200% bottom",
    scrub: true,
    markers: true
  }
});

video.onloadedmetadata = function () {
  tl.to(video, { currentTime: video.duration });
};

// Dealing with devices
function isTouchDevice() {
  return (
    "ontouchstart" in window ||
    navigator.maxTouchPoints > 0 ||
    navigator.msMaxTouchPoints > 0
  );
}
if (isTouchDevice()) {
  video.play();
  video.pause();
}

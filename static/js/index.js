// static/js/index.js
import * as THREE from 'three';
import { OBJLoader } from 'OBJLoader';
import { gsap } from 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js';
import { ScrollTrigger } from 'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js';

gsap.registerPlugin(ScrollTrigger);

// Initialize the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('scene-container').appendChild(renderer.domElement);

// Load the OBJ model
const objLoader = new OBJLoader();
objLoader.load('/static/assets/macbook.obj', (object) => {
    object.scale.set(2, 2, 2); // Scale the model if necessary
    scene.add(object);

    // Animation for OBJ model rotation based on scroll
    gsap.to(object.rotation, {
        scrollTrigger: {
            trigger: ".content",
            start: "top top",
            end: "bottom bottom",
            scrub: true
        },
        x: Math.PI * 2,
        y: Math.PI * 2,
        duration: 1
    });
});

camera.position.z = 5;

// Render loop
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
